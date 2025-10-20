param(
    [Parameter(Mandatory)]
    [string]$Path
)

# Read bytes and decode as UTF-8
$bytes = [IO.File]::ReadAllBytes((Resolve-Path $Path))
$text  = [Text.Encoding]::UTF8.GetString($bytes)

# Keep only chars in U+2000..U+200F (zero-width/general punctuation) plus regular space
$zwChars = $text.ToCharArray() | Where-Object {
    $cp = [int][char]$_
    ( ($cp -ge 0x2000 -and $cp -le 0x200F) -or $_ -eq ' ' )
}
$zw = -join $zwChars

if (-not $zw) {
    Write-Host "No U+2000..U+200F characters found." -ForegroundColor Yellow
    exit 1
}

# Show which codepoints appear
$groups = $zw.ToCharArray() | Group-Object | Sort-Object Count -Descending
Write-Host "Detected codepoints (most frequent first):"
foreach ($g in $groups) {
    $ch = [char]$g.Name
    $cp = [int]$ch
    $label = if ($g.Name -eq ' ') { '[space]' } else { 'invisible' }
    "{0,-10} U+{1:X4}  x{2}" -f $label, $cp, $g.Count
}

# Pick top 2 distinct non-space characters as the two symbols
$signals = ($groups | Where-Object { $_.Name -ne ' ' }).Name | Select-Object -First 2
if ($signals.Count -lt 2) {
    Write-Host "Expected at least two distinct invisible characters to represent dot and dash." -ForegroundColor Yellow
    exit 1
}
$A = [char]$signals[0]
$B = [char]$signals[1]

# Morse map (A-Z and 0-9 only)
$morseMap = @{
    ".-"="A"; "-..."="B"; "-.-."="C"; "-.."="D"; "."="E"; "..-."="F"; "--."="G"; "...."="H"; ".."="I"; ".---"="J";
    "-.-"="K"; ".-.."="L"; "--"="M"; "-."="N"; "---"="O"; ".--."="P"; "--.-"="Q"; ".-."="R"; "..."="S"; "-"="T";
    "..-"="U"; "...-"="V"; ".--"="W"; "-..-"="X"; "-.--"="Y"; "--.."="Z";
    "-----"="0"; ".----"="1"; "..---"="2"; "...--"="3"; "....-"="4"; "....."="5"; "-...."="6"; "--..."="7"; "---.."="8"; "----."="9"
}

function Decode-Morse {
    param([string]$S, [char]$DotChar, [char]$DashChar)

    # Replace the two invisibles with . and - respectively
    $m = $S -replace [regex]::Escape([string]$DotChar), '.' `
             -replace [regex]::Escape([string]$DashChar), '-'

    # Keep only dots, dashes, and spaces; normalize
    $m = ($m -replace '[^.\- ]','' -replace '\s+',' ').Trim()

    if (-not $m) { return '' }

    # Treat double-or-more spaces as word separators
    $m = $m -replace ' {2,}', ' / '

    $tokens = $m -split ' '
    $out = foreach ($t in $tokens) {
        if ($t -eq '/' -or $t -eq '') { ' ' }
        elseif ($morseMap.ContainsKey($t)) { $morseMap[$t] }
        else { '?' }
    }
    (-join $out) -replace ' {2,}', ' '

}

$dec1 = Decode-Morse -S $zw -DotChar $A -DashChar $B
$dec2 = Decode-Morse -S $zw -DotChar $B -DashChar $A

"`nMorse attempt A (U+$("{0:X4}" -f [int]$A)='.', U+$("{0:X4}" -f [int]$B)='-'):"
$dec1
"`nMorse attempt B (reversed):"
$dec2

# Quick heuristic: show likely flag
foreach ($candidate in @($dec1,$dec2)) {
    if ($candidate -and ($candidate -match '\{[A-Za-z0-9_\-]{4,}\}' -or $candidate -match '(flag|ctf)')) {
        "`n>>> Likely flag:"
        $candidate
        break
    }
}
``
