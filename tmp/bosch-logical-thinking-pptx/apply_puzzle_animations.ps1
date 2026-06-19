$ErrorActionPreference = 'Stop'

$DeckPath = "\\prod-fs-gen01\WorkFile\04_在宅勤務\★グローバルビジネス推進部（在宅）\ランゲージサービス課\Dobson（在宅）\02. Clients\Bosch\Logical Thinking & Discussion\Bosch 2026 - Logical Thinking & Discussion - Training Slides.pptx"

function Inches($v) { return [double]$v * 72.0 }
function RgbInt($r, $g, $b) { return [int]($r + ($g -shl 8) + ($b -shl 16)) }

function Get-SlideByTitle($presentation, $needle) {
  for ($i = 1; $i -le $presentation.Slides.Count; $i++) {
    $slide = $presentation.Slides.Item($i)
    foreach ($shape in $slide.Shapes) {
      if ($shape.HasTextFrame -and $shape.TextFrame.HasText) {
        $text = $shape.TextFrame.TextRange.Text
        if ($text -like "*$needle*") { return $slide }
      }
    }
  }
  throw "Slide title not found: $needle"
}

function Remove-ExistingPuzzleAnimationShapes($slide) {
  for ($i = $slide.Shapes.Count; $i -ge 1; $i--) {
    $shape = $slide.Shapes.Item($i)
    if ($shape.Name -like 'PuzzleStrike_*') {
      $shape.Delete()
    }
  }
}

function Add-AnimatedStrike($slide, $name, $x1, $x2, $y, $order) {
  $line = $slide.Shapes.AddLine((Inches $x1), (Inches $y), (Inches $x2), (Inches $y))
  $line.Name = "PuzzleStrike_$name"
  $line.Line.ForeColor.RGB = RgbInt 96 94 92
  $line.Line.Weight = 2.0
  # msoAnimEffectAppear = 1; msoAnimTriggerOnPageClick = 1.
  $null = $slide.TimeLine.MainSequence.AddEffect($line, 1, 1, $order)
}

$pp = New-Object -ComObject PowerPoint.Application
$pp.Visible = -1
$pres = $pp.Presentations.Open($DeckPath, $false, $false, $true)

$sales = Get-SlideByTitle $pres "Who Is Sales-Call?"
Remove-ExistingPuzzleAnimationShapes $sales
Add-AnimatedStrike $sales "Sales_Aiko" 1.99 2.23 2.36 1
Add-AnimatedStrike $sales "Sales_Ben" 2.34 2.54 2.36 2
Add-AnimatedStrike $sales "Sales_Carlos" 2.64 3.05 2.36 3

$rd = Get-SlideByTitle $pres "Who Is R&D-Chat?"
Remove-ExistingPuzzleAnimationShapes $rd
Add-AnimatedStrike $rd "RD_Ben" 2.34 2.54 3.14 1
Add-AnimatedStrike $rd "RD_Carlos" 2.64 3.05 3.14 2
Add-AnimatedStrike $rd "RD_Dita" 3.16 3.42 3.14 3

$pres.Save()
$pres.Close()
$pp.Quit()

[System.Runtime.InteropServices.Marshal]::ReleaseComObject($pres) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($pp) | Out-Null

Write-Output "Applied puzzle elimination animations."
