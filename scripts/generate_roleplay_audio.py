#!/usr/bin/env python3
"""Generate roleplay MP3 files from Situations_all.yaml using Piper."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


SPEAKER_LINE_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]{0,31})\s*:\s*(.+)$")
ACCENT_RE = re.compile(r"^([a-z]{2}_[A-Z]{2})-")


@dataclass
class VoiceConfig:
    model: Path
    config: Path | None = None
    speaker: int | None = None
    length_scale: float | None = None
    noise_scale: float | None = None
    noise_w: float | None = None
    extra_args: list[str] | None = None


def sanitize_filename(text: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", text.strip())
    safe = safe.strip("._")
    return safe or "line"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def load_voice_map(path: Path) -> tuple[VoiceConfig, dict[str, VoiceConfig]]:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, dict):
        raise ValueError("Voice map must be a JSON object.")

    if "default" not in raw:
        raise ValueError("Voice map must include a 'default' object.")

    def parse_voice(obj: dict[str, Any]) -> VoiceConfig:
        if not isinstance(obj, dict):
            raise ValueError("Each voice config must be an object.")
        if "model" not in obj:
            raise ValueError("Each voice config must include a 'model' path.")
        model = Path(obj["model"])
        config = Path(obj["config"]) if "config" in obj else None
        speaker = int(obj["speaker"]) if "speaker" in obj else None
        length_scale = float(obj["length_scale"]) if "length_scale" in obj else None
        noise_scale = float(obj["noise_scale"]) if "noise_scale" in obj else None
        noise_w = float(obj["noise_w"]) if "noise_w" in obj else None
        extra_args = list(map(str, obj.get("extra_args", [])))
        return VoiceConfig(
            model=model,
            config=config,
            speaker=speaker,
            length_scale=length_scale,
            noise_scale=noise_scale,
            noise_w=noise_w,
            extra_args=extra_args,
        )

    default_voice = parse_voice(raw["default"])
    speaker_map_raw = raw.get("speakers", {})
    if not isinstance(speaker_map_raw, dict):
        raise ValueError("'speakers' must be an object.")
    speaker_map = {str(k): parse_voice(v) for k, v in speaker_map_raw.items()}
    return default_voice, speaker_map


def resolve_voice(
    speaker: str, default_voice: VoiceConfig, speaker_map: dict[str, VoiceConfig]
) -> VoiceConfig:
    return speaker_map.get(speaker, default_voice)


def build_piper_command(piper_bin: str, voice: VoiceConfig, output_file: Path) -> list[str]:
    cmd = [piper_bin, "--model", str(voice.model), "--output_file", str(output_file)]
    if voice.config is not None:
        cmd.extend(["--config", str(voice.config)])
    if voice.speaker is not None:
        cmd.extend(["--speaker", str(voice.speaker)])
    if voice.length_scale is not None:
        cmd.extend(["--length_scale", str(voice.length_scale)])
    if voice.noise_scale is not None:
        cmd.extend(["--noise_scale", str(voice.noise_scale)])
    if voice.noise_w is not None:
        cmd.extend(["--noise_w", str(voice.noise_w)])
    if voice.extra_args:
        cmd.extend(voice.extra_args)
    return cmd


def parse_dialogue_lines(dialogue: str) -> list[tuple[str, str]]:
    lines: list[tuple[str, str]] = []
    for raw in dialogue.splitlines():
        text = raw.strip()
        if not text:
            continue
        match = SPEAKER_LINE_RE.match(text)
        if match:
            lines.append((match.group(1), match.group(2).strip()))
        else:
            lines.append(("narrator", text))
    return lines


def iter_roleplay_dialogues(data: dict[str, Any]) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    situations = data.get("situations", {})
    if not isinstance(situations, dict):
        return out

    for situation_code in sorted(situations.keys()):
        situation = situations[situation_code]
        if not isinstance(situation, dict):
            continue
        language = situation.get("language", {})
        if not isinstance(language, dict):
            continue
        roleplay_keys = sorted(k for k in language.keys() if k.startswith("roleplay_"))
        for roleplay_key in roleplay_keys:
            roleplay = language.get(roleplay_key, {})
            if not isinstance(roleplay, dict):
                continue
            model = roleplay.get("model", {})
            if not isinstance(model, dict):
                continue
            dialogue = model.get("dialogue")
            if isinstance(dialogue, str) and dialogue.strip():
                out.append((str(situation_code), roleplay_key, dialogue))
    return out


def synthesize_line(
    piper_bin: str,
    voice: VoiceConfig,
    text: str,
    output_file: Path,
) -> None:
    temp_wav = output_file.with_suffix(".tmp.wav")
    cmd = build_piper_command(piper_bin, voice, temp_wav)
    try:
        proc = subprocess.run(
            cmd,
            input=text,
            text=True,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            stderr = (proc.stderr or "").strip()
            raise RuntimeError(f"Piper failed ({output_file.name}): {stderr}")

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(temp_wav),
            "-codec:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(output_file),
        ]
        ffmpeg_proc = subprocess.run(
            ffmpeg_cmd,
            text=True,
            capture_output=True,
            check=False,
        )
        if ffmpeg_proc.returncode != 0:
            stderr = (ffmpeg_proc.stderr or "").strip()
            raise RuntimeError(f"ffmpeg failed ({output_file.name}): {stderr}")
    finally:
        temp_wav.unlink(missing_ok=True)


def scan_accents(voice_map_path: Path) -> list[str]:
    with voice_map_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    accents: set[str] = set()

    def collect(obj: Any) -> None:
        if isinstance(obj, dict):
            model = obj.get("model")
            if isinstance(model, str):
                stem = Path(model).name
                match = ACCENT_RE.match(stem)
                if match:
                    accents.add(match.group(1))

    collect(raw.get("default"))
    speakers = raw.get("speakers", {})
    if isinstance(speakers, dict):
        for v in speakers.values():
            collect(v)

    return sorted(accents)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate MP3 files for roleplay dialogues from Situations_all.yaml using Piper."
    )
    parser.add_argument(
        "--input",
        default="mofa situations/text/Situations_all.yaml",
        help="Path to Situations_all.yaml",
    )
    parser.add_argument(
        "--voice-map",
        default="mofa situations/audio/voice_map.example.json",
        help="JSON voice map file (default voice + per-speaker overrides).",
    )
    parser.add_argument(
        "--output-dir",
        default="mofa situations/audio/out",
        help="Output root for generated MP3 files.",
    )
    parser.add_argument(
        "--piper-bin",
        default="piper",
        help="Piper executable name or full path.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional limit on number of situation-roleplay pairs for quick tests.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not call Piper; only write manifest.",
    )
    parser.add_argument(
        "--list-accents",
        action="store_true",
        help="Print accent/locale codes inferred from models in the voice map and exit.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    voice_map_path = Path(args.voice_map)
    output_dir = Path(args.output_dir)

    if args.list_accents:
        accents = scan_accents(voice_map_path)
        if accents:
            print("Detected accent/locale codes in voice map:")
            for code in accents:
                print(f"- {code}")
        else:
            print("No accent codes detected in voice-map model filenames.")
        return 0

    if not input_path.exists():
        raise FileNotFoundError(f"Input YAML not found: {input_path}")
    if not voice_map_path.exists():
        raise FileNotFoundError(f"Voice map not found: {voice_map_path}")

    if not args.dry_run and shutil.which(args.piper_bin) is None:
        raise FileNotFoundError(
            f"Piper executable not found: {args.piper_bin}. "
            "Install Piper or pass --piper-bin with a full path."
        )
    if not args.dry_run and shutil.which("ffmpeg") is None:
        raise FileNotFoundError(
            "ffmpeg executable not found on PATH. Install ffmpeg to enable MP3 output."
        )

    data = load_yaml(input_path)
    default_voice, speaker_map = load_voice_map(voice_map_path)
    dialogues = iter_roleplay_dialogues(data)
    if args.limit > 0:
        dialogues = dialogues[: args.limit]

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.csv"

    total_lines = 0
    with manifest_path.open("w", encoding="utf-8", newline="") as manifest_file:
        writer = csv.writer(manifest_file)
        writer.writerow(
            [
                "situation",
                "roleplay",
                "line_index",
                "speaker",
                "text",
                "mp3_path",
                "model_path",
            ]
        )

        for situation_code, roleplay_key, dialogue in dialogues:
            lines = parse_dialogue_lines(dialogue)
            pair_dir = output_dir / situation_code / roleplay_key
            pair_dir.mkdir(parents=True, exist_ok=True)

            transcript_path = pair_dir / "transcript.txt"
            with transcript_path.open("w", encoding="utf-8") as transcript_file:
                for line_index, (speaker, text) in enumerate(lines, start=1):
                    voice = resolve_voice(speaker, default_voice, speaker_map)
                    filename = f"{line_index:03d}_{sanitize_filename(speaker)}.mp3"
                    mp3_path = pair_dir / filename

                    if not args.dry_run:
                        synthesize_line(args.piper_bin, voice, text, mp3_path)

                    transcript_file.write(f"{line_index:03d} {speaker}: {text}\n")
                    writer.writerow(
                        [
                            situation_code,
                            roleplay_key,
                            line_index,
                            speaker,
                            text,
                            str(mp3_path),
                            str(voice.model),
                        ]
                    )
                    total_lines += 1

    print(f"Processed {len(dialogues)} roleplay models.")
    print(f"Processed {total_lines} lines.")
    print(f"Manifest: {manifest_path}")
    if args.dry_run:
        print("Dry run complete. No MP3 files were generated.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
