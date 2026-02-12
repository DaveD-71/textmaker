# No-API Image Workflow (ChatGPT Browser + Local Cleanup)

## 1. Generate prompts (already done once)

```powershell
python "mofa situations/assets/graphics/tools/build_scene_prompt_pack.py"
```

Latest prompt pack folder:
- `mofa situations/assets/graphics/prompt_pack_20260212_160642`

## 2. In ChatGPT browser, generate 10 images

For each file `01_*.txt` to `10_*.txt` in the prompt pack:
1. Start a fresh chat.
2. Paste the full prompt from that `.txt` file.
3. Generate one image.
4. Download PNG.
5. Rename exactly to the target filename listed in `download_and_naming_checklist.csv`.

Put all 10 downloaded PNGs into one folder, for example:
- `mofa situations/assets/graphics/browser_raw_20260212`

## 3. Convert outer white edges to transparency

```powershell
python "mofa situations/assets/graphics/tools/edge_white_to_transparent.py" `
  --input-dir "mofa situations/assets/graphics/browser_raw_20260212" `
  --output-dir "mofa situations/assets/graphics/scene_layers_20260212" `
  --threshold 245
```

Result:
- White pixels connected to the outer border become transparent.
- Interior content is forced fully opaque.

## 4. Use in Word

Insert images from:
- `mofa situations/assets/graphics/scene_layers_20260212`

These are ready to place as a layer over your background.
