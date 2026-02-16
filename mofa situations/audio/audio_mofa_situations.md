# Roleplay Audio (Local Piper TTS)

This workflow synthesizes WAV files from:

- `mofa situations/text/Situations_all.yaml`
- each `language.roleplay_*/model.dialogue`

The `yaml-to-audio` command writes per-line WAV files (for example, `001_S.wav`, `002_T.wav`) so you can test roleplay voices quickly.

## 1) Install dependencies

Python deps (already used in this repo):

```powershell
pip install -r docs/requirements.txt
```

Install Piper and download voices (`*.onnx` + `*.onnx.json`) from Piper voices.

## 2) Configure voices

Edit:

- `docs/examples/voice_map.mofa_situations.json`

Set model paths to your local Piper voice files.

## 3) Dry run first

```powershell
python -m textmaker yaml-to-audio `
  --input "mofa situations/text/Situations_all.yaml" `
  --voice-map "docs/examples/voice_map.mofa_situations.json" `
  --output-dir "mofa situations/audio/out" `
  --path-filter "^situations\\..*\\.language\\.roleplay_\\d+\\.model\\.dialogue$" `
  --dry-run --limit 2
```

This validates YAML parsing and creates only `manifest.csv` + transcripts.

## 4) Generate WAVs

```powershell
python -m textmaker yaml-to-audio `
  --input "mofa situations/text/Situations_all.yaml" `
  --voice-map "docs/examples/voice_map.mofa_situations.json" `
  --output-dir "mofa situations/audio/out" `
  --path-filter "^situations\\..*\\.language\\.roleplay_\\d+\\.model\\.dialogue$"
```

Output goes to:

- `mofa situations/audio/out/<situation>/<roleplay_xxx>/*.wav`

## Optional flags

```powershell
# full piper path
python -m textmaker yaml-to-audio --piper-bin "C:/piper/piper.exe" `
  --input "mofa situations/text/Situations_all.yaml" `
  --voice-map "docs/examples/voice_map.mofa_situations.json"

# custom input/output/config
python -m textmaker yaml-to-audio `
  --input "mofa situations/text/Situations_all.yaml" `
  --voice-map "docs/examples/voice_map.mofa_situations.json" `
  --output-dir "mofa situations/audio/out"

# quick subset test
python -m textmaker yaml-to-audio `
  --input "mofa situations/text/Situations_all.yaml" `
  --voice-map "docs/examples/voice_map.mofa_situations.json" `
  --limit 5

# infer accent/locale codes from model filenames in your voice map
python -m textmaker yaml-to-audio `
  --voice-map "docs/examples/voice_map.mofa_situations.json" `
  --input "mofa situations/text/Situations_all.yaml" `
  --list-accents
```

## Accent options (Piper)

Accent is determined by the specific voice model you download. Common English locale tags include:

- `en_US` (US)
- `en_GB` (UK)
- `en_AU` (Australia)
- `en_CA` (Canada)
- `en_IN` (India)
- `ja_JP` (Japanese)

Practical approach:

- choose one locale per role (`S`, `T`) in `docs/examples/voice_map.mofa_situations.json`
- run `--list-accents` after you point the map to real model filenames
- tweak `length_scale` (faster/slower speech) for realism
