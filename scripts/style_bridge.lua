-- Generic Pandoc Lua filter: maps Markdown Div classes to DOCX custom styles via YAML metadata.
-- This replaces hard-wired class-to-style mappings.
--
-- Usage in Markdown YAML front matter:
--   style_bridge:
--     remove_horizontal_rules: true
--     preserve_div_line_breaks: true
--   style_map:
--     activity-input: "Activity Input"
--     learn-process: "Learn Process"
--     model: "Model"
--     ...

local stringify = pandoc.utils.stringify

local style_map = nil

local function get_meta_bool(section_name, key, default)
  local section = PANDOC_STATE.meta[section_name]
  if section and section[key] ~= nil then
    local value = stringify(section[key])
    return value == "true" or value == "1" or value == "yes"
  end
  return default
end

local function load_style_map()
  local map = {}
  local meta_map = PANDOC_STATE.meta["style_map"]

  if type(meta_map) ~= "table" then
    return map
  end

  for k, v in pairs(meta_map) do
    map[k] = stringify(v)
  end

  return map
end

local function preserve_line_breaks(el)
  if not get_meta_bool("style_bridge", "preserve_div_line_breaks", true) then
    return el
  end

  return pandoc.walk_block(el, {
    SoftBreak = function(_)
      return pandoc.LineBreak()
    end
  })
end

function HorizontalRule(el)
  if get_meta_bool("style_bridge", "remove_horizontal_rules", false) then
    return {}
  end
  return el
end

function Div(el)
  if FORMAT ~= "docx" then
    return el
  end

  if style_map == nil then
    style_map = load_style_map()
  end

  for _, class in ipairs(el.classes) do
    local style = style_map[class]
    if style and style ~= "" then
      el.attributes["custom-style"] = style
      return preserve_line_breaks(el)
    end
  end

  return el
end
