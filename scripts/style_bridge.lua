-- Generic Pandoc Lua filter: maps Markdown Div classes to DOCX custom styles via YAML metadata.
--
-- Usage in Markdown YAML front matter:
--   style_bridge:
--     remove_horizontal_rules: true
--     preserve_div_line_breaks: true
--   style_map:
--     activity-analysis: "Div Label Activity Analysis"
--     learn-process: "Div Label Process"
--     model: "Model"
--     ...
--
-- "Div Label *" styles: first Para gets the label style; subsequent Paras get "Div Content".
-- All other styles (Model, Model Bad, Model Good, etc.): applied to every paragraph in the Div.
--
-- Two-pass approach: Meta is read first, then Div/HorizontalRule use the loaded values.

local stringify = pandoc.utils.stringify

local style_map = {}
local remove_hr = false
local preserve_lb = true

local function bool_from_meta(val, default)
  if val == nil then return default end
  local s = stringify(val)
  return s == "true" or s == "1" or s == "yes"
end

local function is_div_label_style(style_name)
  return style_name:sub(1, 10) == "Div Label "
end

local function softbreak_to_linebreak(block)
  return pandoc.walk_block(block, {
    SoftBreak = function(_) return pandoc.LineBreak() end
  })
end

local function wrap_para(block, custom_style)
  local inner = pandoc.Div(pandoc.Blocks { block })
  inner.attributes["custom-style"] = custom_style
  if preserve_lb then
    inner = softbreak_to_linebreak(inner)
  end
  return inner
end

return {
  -- Pass 1: load configuration from document metadata
  {
    Meta = function(meta)
      if meta.style_map and type(meta.style_map) == "table" then
        for k, v in pairs(meta.style_map) do
          style_map[k] = stringify(v)
        end
      end
      if meta.style_bridge and type(meta.style_bridge) == "table" then
        remove_hr = bool_from_meta(meta.style_bridge.remove_horizontal_rules, false)
        preserve_lb = bool_from_meta(meta.style_bridge.preserve_div_line_breaks, true)
      end
      return meta
    end
  },
  -- Pass 2: apply style mappings
  {
    HorizontalRule = function(el)
      if remove_hr then return {} end
      return el
    end,

    Div = function(el)
      if FORMAT ~= "docx" then return el end

      for _, class in ipairs(el.classes) do
        local style = style_map[class]
        if style and style ~= "" then

          if not is_div_label_style(style) then
            -- Content styles (Model, Model Bad, etc.): apply to all paragraphs
            el.attributes["custom-style"] = style
            if preserve_lb then
              el = softbreak_to_linebreak(el)
            end
            return el
          end

          -- "Div Label *" styles: first Para/Plain → label style; rest left unstyled
          local result = {}
          local label_done = false
          for _, block in ipairs(el.content) do
            if block.t == "Para" or block.t == "Plain" then
              if not label_done then
                table.insert(result, wrap_para(block, style))
                label_done = true
              else
                table.insert(result, block)
              end
            else
              -- Lists and other block elements: leave unstyled so list formatting survives
              table.insert(result, block)
            end
          end
          return pandoc.Blocks(result)
        end
      end

      return el
    end
  }
}
