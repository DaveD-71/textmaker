$ErrorActionPreference = 'Stop'

$outDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$out = Join-Path $outDir 'process-business-standard-template-v2.pptx'

# Native PowerPoint layout constants. This deck intentionally uses only
# standard PowerPoint layouts/placeholders so Designer can work with it.
$ppLayoutTitle = 1
$ppLayoutText = 2
$ppLayoutComparison = 34

function Set-PlaceholderText($slide, [int]$idx, [string]$text) {
  $shape = $slide.Shapes.Placeholders($idx)
  $shape.TextFrame.TextRange.Text = $text
  return $shape
}

function Try-SetText($slide, [int]$idx, [string]$text) {
  try {
    Set-PlaceholderText $slide $idx $text | Out-Null
    return $true
  } catch {
    return $false
  }
}

$pp = $null
$pres = $null
try {
$pp = New-Object -ComObject PowerPoint.Application
$pp.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
$pres = $pp.Presentations.Add([Microsoft.Office.Core.MsoTriState]::msoTrue)
$pres.PageSetup.SlideWidth = 960
$pres.PageSetup.SlideHeight = 540

# Slide 1. Emphasis: decision request and limited pilot.
$s = $pres.Slides.Add(1, $ppLayoutTitle)
Set-PlaceholderText $s 1 'Approve a Four-Week Workflow Pilot' | Out-Null
Set-PlaceholderText $s 2 "Reducing import document handoff delays`nDecision today: pilot, owner, review measures" | Out-Null

# Slide 2. Emphasis: fragmented ownership.
$s = $pres.Slides.Add(2, $ppLayoutText)
Set-PlaceholderText $s 1 'Handoff Notes Are Spread Across Three Places' | Out-Null
Set-PlaceholderText $s 2 "Ownership is unclear before the cutoff window`nEmail: messages split`nSpreadsheet: copied details`nShort messages: owner unclear" | Out-Null

# Slide 3. Emphasis: main preventable cause plus scale.
$s = $pres.Slides.Add(3, $ppLayoutText)
Set-PlaceholderText $s 1 'Most Delays Involve Unclear Handoff Notes' | Out-Null
Set-PlaceholderText $s 2 "61% linked to unclear notes`n38 late handoffs`n22 minutes average rework" | Out-Null

# Slide 4. Emphasis: current versus pilot change.
$s = $pres.Slides.Add(4, $ppLayoutComparison)
Try-SetText $s 1 'One Shared Log Makes Ownership Visible Earlier' | Out-Null
Try-SetText $s 2 'Current' | Out-Null
Try-SetText $s 3 "Email check`nManual note`nHandoff`nDeadline risk" | Out-Null
Try-SetText $s 4 'Pilot' | Out-Null
Try-SetText $s 5 "Exception log`nFixed checkpoint`nVisible owner`nControl unchanged" | Out-Null

# Slide 5. Emphasis: limited risk and review point.
$s = $pres.Slides.Add(5, $ppLayoutText)
Set-PlaceholderText $s 1 'The Pilot Is Limited and Controlled' | Out-Null
Set-PlaceholderText $s 2 "Test before expanding`nWeek 0: review fields`nWeeks 1-4: daily checkpoint`nEnd: review delay, rework, and feedback" | Out-Null

# Slide 6. Emphasis: three clear actions.
$s = $pres.Slides.Add(6, $ppLayoutText)
Set-PlaceholderText $s 1 'The Request Is Approval, Ownership, and Review Criteria' | Out-Null
Set-PlaceholderText $s 2 "Approve the pilot`nConfirm the documentation lead`nAgree the review measures" | Out-Null

$pres.SaveAs($out)
$pres.Close()
$pp.Quit()

Get-Item -LiteralPath $out | Select-Object FullName, Length, LastWriteTime
} finally {
  if ($pres -ne $null) {
    try { $pres.Close() } catch {}
  }
  if ($pp -ne $null) {
    try { $pp.Quit() } catch {}
  }
}
