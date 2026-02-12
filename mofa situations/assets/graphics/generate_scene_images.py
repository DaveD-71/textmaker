#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from PIL import Image
from openai import OpenAI


@dataclass
class SceneSpec:
    scene_id: str
    title: str
    applies_to: str
    core_interaction: str
    location: str
    furniture_props: str
    body_language: str
    must_not_include: str
    negative_space: str
    cultural_notes: str
    japanese_staff: str
    local_person: str
    perspective: str
    palette: str
    design_notes: str
    image_status: str
    outstanding_actions: str


def parse_scene_asset_register(path: Path) -> list[SceneSpec]:
    text = path.read_text(encoding="utf-8")
    scenes: list[SceneSpec] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("| **S"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 16:
            continue

        scene_cell = cells[0]
        m = re.match(r"\*\*(?P<id>[^*]+)\*\*\s*(?P<title>.*)$", scene_cell)
        if not m:
            continue

        scenes.append(
            SceneSpec(
                scene_id=m.group("id").strip(),
                title=m.group("title").strip(),
                applies_to=cells[1],
                core_interaction=cells[2],
                location=cells[3],
                furniture_props=cells[4],
                body_language=cells[5],
                must_not_include=cells[6],
                negative_space=cells[7],
                cultural_notes=cells[8],
                japanese_staff=cells[9],
                local_person=cells[10],
                perspective=cells[11],
                palette=cells[12],
                design_notes=cells[13],
                image_status=cells[14],
                outstanding_actions=cells[15],
            )
        )

    if not scenes:
        raise RuntimeError(f"No scene rows found in {path}")
    return scenes


def parse_top10_scene_ids(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    scene_ids: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        m = re.match(r"##\s+SCENE\s+([A-Za-z0-9\-]+)", line)
        if m:
            scene_ids.append(m.group(1))
    if not scene_ids:
        raise RuntimeError(f"No scene IDs found in {path}")
    return scene_ids


def normalize_people(value: str) -> str:
    cleaned = value.replace("**", "")
    return cleaned.replace("—", "-")


def build_prompt(scene: SceneSpec) -> str:
    return f"""
Create a single illustration for a Japanese government workplace English-learning textbook.

Style requirements (strict):
- semi-realistic painterly editorial illustration, not photorealistic
- soft edges, gentle blending, even neutral lighting
- realistic anatomy and proportions
- no cartoon, no manga, no cinematic contrast
- no readable text anywhere in the image
- no logos, no watermarks, no brand names, no interface elements
- layout-ready for A4 page design with clear negative space at: {scene.negative_space}
- warm but professional institutional tone
- exactly two people unless scene details explicitly require otherwise

Scene brief:
- Scene ID: {scene.scene_id}
- Scene title: {scene.title}
- Applies to situations: {scene.applies_to}
- Core interaction: {scene.core_interaction}
- Location: {scene.location}
- Furniture and props: {scene.furniture_props}
- Body language: {scene.body_language}
- Cultural notes: {scene.cultural_notes}
- Japanese staff identity: {normalize_people(scene.japanese_staff)}
- Local person identity: {normalize_people(scene.local_person)}
- Perspective/composition: {scene.perspective}
- Dominant palette/accent: {scene.palette}
- Design notes: {scene.design_notes}

Must NOT include:
- {scene.must_not_include}
- any extra symbols, arrows, captions, labels, signage text, or numbers

Output framing and format requirements:
- landscape composition, approximately postcard proportion (3:2)
- full rectangular scene illustration that can be layered in MS Word
- keep interior scene fully opaque and avoid washed-out edges
""".strip()


def is_near_white(r: int, g: int, b: int, a: int, threshold: int) -> bool:
    if a == 0:
        return False
    return r >= threshold and g >= threshold and b >= threshold


def make_edge_white_transparent(input_path: Path, output_path: Path, threshold: int = 245) -> None:
    image = Image.open(input_path).convert("RGBA")
    w, h = image.size
    pixels = image.load()

    keep_transparent = [[False for _ in range(h)] for _ in range(w)]
    queue: deque[tuple[int, int]] = deque()

    def try_enqueue(x: int, y: int) -> None:
        if keep_transparent[x][y]:
            return
        r, g, b, a = pixels[x, y]
        if is_near_white(r, g, b, a, threshold):
            keep_transparent[x][y] = True
            queue.append((x, y))

    for x in range(w):
        try_enqueue(x, 0)
        try_enqueue(x, h - 1)
    for y in range(h):
        try_enqueue(0, y)
        try_enqueue(w - 1, y)

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if nx < 0 or ny < 0 or nx >= w or ny >= h:
                continue
            if keep_transparent[nx][ny]:
                continue
            r, g, b, a = pixels[nx, ny]
            if is_near_white(r, g, b, a, threshold):
                keep_transparent[nx][ny] = True
                queue.append((nx, ny))

    for x in range(w):
        for y in range(h):
            r, g, b, a = pixels[x, y]
            if keep_transparent[x][y]:
                pixels[x, y] = (r, g, b, 0)
            else:
                pixels[x, y] = (r, g, b, 255)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG")


def generate_scene_image(
    client: OpenAI,
    model: str,
    prompt: str,
    size: str,
    retries: int = 3,
) -> bytes:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            response = client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
            )
            b64 = response.data[0].b64_json
            if not b64:
                raise RuntimeError("Image API response did not include b64_json")
            import base64

            return base64.b64decode(b64)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt == retries:
                break
            time.sleep(2 * attempt)
    raise RuntimeError(f"Image generation failed after {retries} attempts: {last_error}")


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value)
    return value.strip("-").lower()


def select_scenes(
    all_scenes: list[SceneSpec],
    preferred_scene_ids: Iterable[str] | None,
) -> list[SceneSpec]:
    by_id = {s.scene_id: s for s in all_scenes}
    if preferred_scene_ids:
        selected: list[SceneSpec] = []
        for sid in preferred_scene_ids:
            if sid in by_id:
                selected.append(by_id[sid])
        if selected:
            return selected
    return all_scenes


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate MOFA scene images from the register via OpenAI API")
    parser.add_argument(
        "--register",
        default="mofa situations/assets/scene_asset_register.md",
        help="Path to scene_asset_register.md",
    )
    parser.add_argument(
        "--top-scenes",
        default="mofa situations/assets/graphics/required/scenes.md",
        help="Path to top scenes sheet used to target 10 scenes",
    )
    parser.add_argument(
        "--out-dir",
        default="",
        help="Output directory. Default: mofa situations/assets/graphics/generated_YYYYMMDD_HHMMSS",
    )
    parser.add_argument("--model", default="gpt-image-1", help="OpenAI image model")
    parser.add_argument("--size", default="1536x1024", help="Image size, e.g. 1536x1024")
    parser.add_argument(
        "--white-threshold",
        type=int,
        default=245,
        help="Edge white threshold for transparency masking",
    )
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.")
        print("Set it in this shell, then rerun this command.")
        return 2

    register_path = Path(args.register)
    top_scenes_path = Path(args.top_scenes)

    all_scenes = parse_scene_asset_register(register_path)
    preferred_ids = parse_top10_scene_ids(top_scenes_path) if top_scenes_path.exists() else None
    selected_scenes = select_scenes(all_scenes, preferred_ids)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.out_dir) if args.out_dir else Path(f"mofa situations/assets/graphics/generated_{timestamp}")
    raw_dir = out_dir / "raw"
    final_dir = out_dir / "final_png"
    prompt_dir = out_dir / "prompts"
    for d in (raw_dir, final_dir, prompt_dir):
        d.mkdir(parents=True, exist_ok=True)

    client = OpenAI(api_key=api_key)

    manifest: list[dict[str, str]] = []

    print(f"Generating {len(selected_scenes)} scenes into: {out_dir}")
    for idx, scene in enumerate(selected_scenes, start=1):
        prompt = build_prompt(scene)
        base_name = f"{idx:02d}_{scene.scene_id}_{slugify(scene.title)}"

        prompt_path = prompt_dir / f"{base_name}.txt"
        prompt_path.write_text(prompt + "\n", encoding="utf-8")

        print(f"[{idx}/{len(selected_scenes)}] {scene.scene_id} {scene.title}")
        png_bytes = generate_scene_image(
            client=client,
            model=args.model,
            prompt=prompt,
            size=args.size,
        )

        raw_path = raw_dir / f"{base_name}.png"
        raw_path.write_bytes(png_bytes)

        final_path = final_dir / f"{base_name}.png"
        make_edge_white_transparent(
            input_path=raw_path,
            output_path=final_path,
            threshold=args.white_threshold,
        )

        manifest.append(
            {
                "scene_id": scene.scene_id,
                "title": scene.title,
                "raw_png": str(raw_path),
                "final_png": str(final_path),
                "prompt": str(prompt_path),
                "size": args.size,
                "image_status": scene.image_status,
                "outstanding_actions": scene.outstanding_actions,
            }
        )

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Done. Wrote {len(selected_scenes)} images.")
    print(f"Final PNG folder: {final_dir}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
