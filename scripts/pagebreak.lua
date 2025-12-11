-- Convert \pagebreak / \newpage markers into real page breaks for common outputs.
local function pagebreak()
  if FORMAT:match('docx') then
    return pandoc.RawBlock('openxml', '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
  elseif FORMAT:match('latex') then
    return pandoc.RawBlock('latex', '\\newpage')
  elseif FORMAT:match('html') or FORMAT:match('epub') then
    return pandoc.RawBlock('html', '<div style="page-break-after: always;"></div>')
  else
    return pandoc.Null()
  end
end

function Para(el)
  if #el.content == 1 and el.content[1].t == 'Str' then
    local txt = el.content[1].text
    if txt == '\\pagebreak' or txt == '\\newpage' or txt == '\\clearpage' then
      return pagebreak()
    end
  end
end

function RawBlock(el)
  if el.text:match('^%s*\\pagebreak') or el.text:match('^%s*\\newpage') or el.text:match('^%s*\\clearpage') then
    return pagebreak()
  end
end

function HorizontalRule(el)
  return pagebreak()
end
