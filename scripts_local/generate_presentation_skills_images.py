#!/usr/bin/env python3
"""Batch-generate Presentation Skills textbook images via raw HTTP calls to the
OpenAI Images API (gpt-image-1).

Uses raw HTTP (via `requests`) rather than the openai Python SDK, since the
SDK has repeatedly corrupted itself on this network-drive-backed venv across
multiple version attempts (1.x and 2.x). Raw HTTP only depends on `requests`,
which has been stable throughout.

Diagram/process-type images get a NATIVE transparent background (the
gpt-image-1 `background: "transparent"` API parameter) so their flat
background is never baked in and never needs post-hoc color-keying. Scenario
(illustrated-scene) images stay fully opaque, since they're meant to be full
rectangular illustrations, not cutouts.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import time
from pathlib import Path

import requests

API_URL = "https://api.openai.com/v1/images/generations"
DEFAULT_REGISTER = Path(__file__).resolve().parents[1] / "books" / "Presentation Skills" / "images" / "image_register.json"

TRANSPARENT_TYPES = {"diagram", "process", "icon_set"}


def load_register(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_prompt(style_lock: dict, image_spec: dict) -> str:
    kind = image_spec["type"]
    style = style_lock["photo_style"] if kind == "scenario" else style_lock["diagram_style"]
    return f"{style}\n\nSpecific illustration to create:\n{image_spec['prompt']}"


def generate_image(prompt: str, size: str, model: str, transparent: bool, retries: int = 3) -> bytes:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set.")

    payload = {"model": model, "prompt": prompt, "size": size}
    if transparent:
        payload["background"] = "transparent"

    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(
                API_URL,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json=payload,
                timeout=180,
            )
            if resp.status_code != 200:
                raise RuntimeError(f"OpenAI API error {resp.status_code}: {resp.text[:2000]}")
            data = resp.json()
            b64 = data["data"][0]["b64_json"]
            return base64.b64decode(b64)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt == retries:
                break
            time.sleep(2 * attempt)
    raise RuntimeError(f"Image generation failed after {retries} attempts: {last_error}")


def clean_transparent_pixels(png_bytes: bytes) -> bytes:
    """Zero out RGB in fully-transparent pixels to avoid ghost-color bleed in
    renderers that don't correctly ignore RGB when alpha=0."""
    import io

    from PIL import Image

    img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a == 0:
                pixels[x, y] = (255, 255, 255, 0)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Presentation Skills images from the register via raw HTTP")
    parser.add_argument("--register", default=str(DEFAULT_REGISTER))
    parser.add_argument("--batch", default=None, help="Only generate images tagged with this batch name")
    parser.add_argument("--ids", nargs="*", default=None, help="Only generate images with these specific ids")
    parser.add_argument("--out-dir", default="")
    parser.add_argument("--model", default="gpt-image-1")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    register_path = Path(args.register)
    register = load_register(register_path)
    style_lock = register["style_lock"]
    all_images = register["images"]

    selected = all_images
    if args.batch:
        selected = [i for i in selected if i.get("batch") == args.batch]
    if args.ids:
        wanted = set(args.ids)
        selected = [i for i in selected if i["id"] in wanted]

    if not selected:
        print("No images matched the given filters.")
        return 1

    out_dir = Path(args.out_dir) if args.out_dir else register_path.parent / "generated"
    raw_dir = out_dir / "raw"
    prompt_dir = out_dir / "prompts"
    for d in (raw_dir, prompt_dir):
        d.mkdir(parents=True, exist_ok=True)

    manifest_path = out_dir / "manifest.json"
    manifest: list[dict] = []
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            manifest = []
    manifest_by_id = {m["id"]: m for m in manifest}

    print(f"Generating {len(selected)} image(s) into: {out_dir}")
    for idx, spec in enumerate(selected, start=1):
        image_id = spec["id"]
        if spec.get("generation_method") == "composited_from_icon_sheet":
            print(f"[skip] {image_id} uses a custom build script ({spec.get('build_script')}), not this generic batch path")
            continue
        prompt = build_prompt(style_lock, spec)
        transparent = spec["type"] in TRANSPARENT_TYPES

        prompt_path = prompt_dir / f"{image_id}.txt"
        prompt_path.write_text(prompt + "\n", encoding="utf-8")

        print(f"[{idx}/{len(selected)}] {image_id} - {spec['title']} (transparent={transparent})")

        if args.dry_run:
            continue

        png_bytes = generate_image(
            prompt=prompt,
            size=spec.get("size", "1536x1024"),
            model=args.model,
            transparent=transparent,
        )
        if transparent:
            png_bytes = clean_transparent_pixels(png_bytes)

        raw_path = raw_dir / f"{image_id}.png"
        raw_path.write_bytes(png_bytes)

        manifest_by_id[image_id] = {
            "id": image_id,
            "unit": spec["unit"],
            "type": spec["type"],
            "batch": spec.get("batch"),
            "title": spec["title"],
            "transparent": transparent,
            "raw_png": str(raw_path),
            "prompt": str(prompt_path),
            "size": spec.get("size", "1536x1024"),
            "model": args.model,
        }

    if not args.dry_run:
        manifest_path.write_text(
            json.dumps(list(manifest_by_id.values()), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"Manifest: {manifest_path}")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
