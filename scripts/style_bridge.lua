-- Generic Pandoc Lua filter: maps Markdown Div classes to DOCX custom styles via YAML metadata.
--
-- Usage in Markdown YAML front matter:
--   style_bridge:
--     remove_horizontal_rules: true
--     preserve_div_line_breaks: true
--     list_block_spacing:
--       enabled: true
--       before_pt: 6
--       after_pt: 6
--   style_map:
--     learn: "Div Label Learn"
--     write: "Div Label Write"
--     ...
--   div_content_style_map:
--     example: "AW Example"
--     example-good: "AW Example Good"
--     example-bad: "AW Example Bad"
--
-- "Div Label *" styles: first Para gets the label style; remaining blocks get
-- the matching div_content_style_map style when configured.
-- All other styles: applied to every paragraph in the Div.
--
-- Two-pass approach: Meta is read first, then Div/HorizontalRule use the loaded values.

local stringify = pandoc.utils.stringify

local style_map = {}
local content_style_map = {}
local remove_hr = false
local preserve_lb = true
local list_block_spacing = false
local list_space_before_pt = 6
local list_space_after_pt = 6

local function bool_from_meta(val, default)
  if val == nil then return default end
  local s = stringify(val)
  return s == "true" or s == "1" or s == "yes"
end

local function number_from_meta(val, default)
  if val == nil then return default end
  local n = tonumber(stringify(val))
  if n == nil then return default end
  return n
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

local function wrap_block(block, custom_style)
  local inner = pandoc.Div(pandoc.Blocks { block })
  inner.attributes["custom-style"] = custom_style
  if preserve_lb then
    inner = softbreak_to_linebreak(inner)
  end
  return inner
end

local function spacing_paragraph(before_pt, after_pt)
  local before_twips = math.floor((before_pt or 0) * 20 + 0.5)
  local after_twips = math.floor((after_pt or 0) * 20 + 0.5)
  local xml = '<w:p><w:pPr><w:spacing w:before="' ..
    tostring(before_twips) .. '" w:after="' .. tostring(after_twips) ..
    '"/></w:pPr></w:p>'
  return pandoc.RawBlock('openxml', xml)
end

local function add_list_block_spacing(el)
  if FORMAT ~= "docx" or not list_block_spacing then return el end
  return pandoc.Blocks({
    spacing_paragraph(list_space_before_pt, 0),
    el,
    spacing_paragraph(0, list_space_after_pt)
  })
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
      if meta.div_content_style_map and type(meta.div_content_style_map) == "table" then
        for k, v in pairs(meta.div_content_style_map) do
          content_style_map[k] = stringify(v)
        end
      end
      if meta.style_bridge and type(meta.style_bridge) == "table" then
        remove_hr = bool_from_meta(meta.style_bridge.remove_horizontal_rules, false)
        preserve_lb = bool_from_meta(meta.style_bridge.preserve_div_line_breaks, true)
        if meta.style_bridge.list_block_spacing and type(meta.style_bridge.list_block_spacing) == "table" then
          local cfg = meta.style_bridge.list_block_spacing
          list_block_spacing = bool_from_meta(cfg.enabled, false)
          list_space_before_pt = number_from_meta(cfg.before_pt, 6)
          list_space_after_pt = number_from_meta(cfg.after_pt, 6)
        end
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

    BulletList = function(el)
      return add_list_block_spacing(el)
    end,

    OrderedList = function(el)
      return add_list_block_spacing(el)
    end,

    Div = function(el)
      if FORMAT ~= "docx" then return el end

      for _, class in ipairs(el.classes) do
        local style = style_map[class]
        if style and style ~= "" then

          if not is_div_label_style(style) then
            -- Content styles: apply to all paragraphs in the Div
            el.attributes["custom-style"] = style
            if preserve_lb then
              el = softbreak_to_linebreak(el)
            end
            return el
          end

          -- "Div Label *" styles: first Para/Plain → label style; rest gets an
          -- explicit content style only when the source YAML says so.
          local content_style = content_style_map[class]
          local result = {}
          local label_done = false
          for _, block in ipairs(el.content) do
            if block.t == "Para" or block.t == "Plain" then
              if not label_done then
                table.insert(result, wrap_para(block, style))
                label_done = true
              else
                if content_style and content_style ~= "" then
                  table.insert(result, wrap_para(block, content_style))
                else
                  table.insert(result, block)
                end
              end
            else
              if content_style and content_style ~= "" then
                table.insert(result, wrap_block(block, content_style))
              else
                -- Lists and other block elements: leave unstyled so list formatting survives
                table.insert(result, block)
              end
            end
          end
          return pandoc.Blocks(result)
        end
      end

      return el
    end
  }
}
