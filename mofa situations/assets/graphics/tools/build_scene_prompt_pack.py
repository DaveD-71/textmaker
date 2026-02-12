#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


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

        m = re.match(r"\*\*(?P<id>[^*]+)\*\*\s*(?P<title>.*)$", cells[0])
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
            )
        )

    if not scenes:
        raise RuntimeError(f"No scene rows found in {path}")
    return scenes


def parse_top10_scene_ids(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    scene_ids: list[str] = []
    for raw_line in text.splitlines():
        m = re.match(r"##\s+SCENE\s+([A-Za-z0-9\-]+)", raw_line.strip())
        if m:
            scene_ids.append(m.group(1))
    if not scene_ids:
        raise RuntimeError(f"No scene IDs found in {path}")
    return scene_ids


def clean_person(text: str) -> str:
    return text.replace("**", "").replace("—", "-")


def build_prompt(scene: SceneSpec) -> str:
    return f"""Generate ONE image only.

If reference images are attached, they are STYLE-ONLY references.
Hard anti-copy constraints:
- create a completely new composition from scratch
- do NOT copy camera angle, character placement, poses, framing, or prop arrangement from references
- do NOT replicate faces or identity details from reference photos
- do NOT reproduce any text, marks, numbering, borders, or watermarks from references
- if output resembles a reference composition, regenerate with a clearly different layout and angle

Priority constraints (must satisfy all):
1) LOCATION: {scene.location}
2) ACTION: {scene.core_interaction}
3) PROPS: {scene.furniture_props}
4) BODY LANGUAGE: {scene.body_language}
5) NEGATIVE SPACE: {scene.negative_space}
6) MUST NOT INCLUDE: {scene.must_not_include}

Global style lock:
- semi-realistic painterly editorial illustration for institutional textbook use
- soft edges and brush-like blending, realistic anatomy, calm neutral expressions
- evenly lit scene, no dramatic cinematic contrast, not photorealistic, not anime/cartoon
- layout-ready composition with negative space at: {scene.negative_space}

Scene brief:
- Scene ID: {scene.scene_id}
- Title: {scene.title}
- Applies to: {scene.applies_to}
- Core interaction: {scene.core_interaction}
- Location: {scene.location}
- Furniture/props: {scene.furniture_props}
- Body language: {scene.body_language}
- Cultural notes: {scene.cultural_notes}
- Japanese staff: {clean_person(scene.japanese_staff)}
- Local person: {clean_person(scene.local_person)}
- Perspective/composition: {scene.perspective}
- Dominant palette/accent: {scene.palette}
- Design notes: {scene.design_notes}

Output requirements:
- PNG, landscape postcard-like ratio (3:2), target 1536x1024 or closest available
- no text, no labels, no readable signage, no numbers, no logos, no watermark
- no embedded arrows, captions, symbols, icons, or instructional graphics
- keep a clean white outer border region; interior scene content should appear fully opaque

Return only the image.""".strip()


def build_revision_prompt(scene: SceneSpec) -> str:
    return f"""Revise this image to match scene {scene.scene_id} exactly.

Fix these non-negotiables:
- Location must be: {scene.location}
- Core interaction must be: {scene.core_interaction}
- Required props: {scene.furniture_props}
- Required body language: {scene.body_language}
- Keep negative space at: {scene.negative_space}
- Remove forbidden content: {scene.must_not_include}

Keep style:
- semi-realistic painterly editorial illustration, calm professional tone
- no text, no numbers, no logos, no signage text, no watermark

Preserve image quality and output one revised image only.""".strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build ChatGPT-browser prompt pack for scene images")
    parser.add_argument(
        "--register",
        default="mofa situations/assets/scene_asset_register.md",
        help="Path to scene register markdown",
    )
    parser.add_argument(
        "--top-scenes",
        default="mofa situations/assets/graphics/required/scenes.md",
        help="Path to top scenes markdown",
    )
    parser.add_argument(
        "--out-dir",
        default="",
        help="Output directory. Default: mofa situations/assets/graphics/prompt_pack_YYYYMMDD_HHMMSS",
    )
    args = parser.parse_args()

    all_scenes = parse_scene_asset_register(Path(args.register))
    top10 = parse_top10_scene_ids(Path(args.top_scenes))
    by_id = {s.scene_id: s for s in all_scenes}
    scenes = [by_id[sid] for sid in top10 if sid in by_id]

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.out_dir) if args.out_dir else Path(f"mofa situations/assets/graphics/prompt_pack_{ts}")
    out_dir.mkdir(parents=True, exist_ok=True)

    index_lines = ["# Scene Prompt Pack", "", "Use one prompt per fresh chat in ChatGPT web.", ""]

    for i, scene in enumerate(scenes, start=1):
        prompt = build_prompt(scene)
        filename = f"{i:02d}_{scene.scene_id}.txt"
        revision_filename = f"{i:02d}_{scene.scene_id}_revision.txt"
        (out_dir / filename).write_text(prompt + "\n", encoding="utf-8")
        (out_dir / revision_filename).write_text(build_revision_prompt(scene) + "\n", encoding="utf-8")
        index_lines.append(f"- {filename}: {scene.title}")
        index_lines.append(f"- {revision_filename}: {scene.title} (repair prompt)")

    checklist = out_dir / "download_and_naming_checklist.csv"
    checklist_rows = ["order,scene_id,title,target_filename"]
    for i, scene in enumerate(scenes, start=1):
        checklist_rows.append(f"{i},{scene.scene_id},\"{scene.title}\",{i:02d}_{scene.scene_id}.png")
    checklist.write_text("\n".join(checklist_rows) + "\n", encoding="utf-8")

    (out_dir / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"Wrote prompt pack for {len(scenes)} scenes: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
