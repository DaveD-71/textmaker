"""
YAML -> MP3 converter using Piper.

Scans a YAML file for text leaves (for example, dialogue/text fields), then
generates MP3 files with optional normalization and chunking for better rhythm.
"""
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


DEFAULT_SPEAKER_LINE_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]{0,31})\s*:\s*(.+)$")
ACCENT_RE = re.compile(r"^([a-z]{2}_[A-Z]{2})-")
ABBREV_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bMr\.(?=\s|$)", re.IGNORECASE), "Mister"),
    (re.compile(r"\bMrs\.(?=\s|$)", re.IGNORECASE), "Missus"),
    (re.compile(r"\bMs\.(?=\s|$)", re.IGNORECASE), "Ms"),
    (re.compile(r"\bDr\.(?=\s|$)", re.IGNORECASE), "Doctor"),
    (re.compile(r"\bProf\.(?=\s|$)", re.IGNORECASE), "Professor"),
    (re.compile(r"\bSt\.(?=\s|$)", re.IGNORECASE), "Saint"),
    (re.compile(r"\betc\.(?=\s|$)", re.IGNORECASE), "etcetera"),
]


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


def slug_join(parts: list[str], max_len: int = 80) -> str:
    joined = "_".join(parts)
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", joined).strip("._")
    if not slug:
        slug = "block"
    return slug[:max_len]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def _parse_voice(obj: dict[str, Any]) -> VoiceConfig:
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


def _parse_voice_pool(node: Any) -> list[VoiceConfig]:
    if not isinstance(node, list):
        raise ValueError("Voice pool must be a list of voice configs.")
    return [_parse_voice(v) for v in node if isinstance(v, dict)]


def load_voice_map(
    path: Path,
) -> tuple[VoiceConfig, dict[str, VoiceConfig], list[VoiceConfig], dict[str, list[VoiceConfig]]]:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        raise ValueError("Voice map must be a JSON object.")
    if "default" not in raw:
        raise ValueError("Voice map must include a 'default' object.")

    default_voice = _parse_voice(raw["default"])
    speaker_map_raw = raw.get("speakers", {})
    if not isinstance(speaker_map_raw, dict):
        raise ValueError("'speakers' must be an object.")
    speaker_map = {str(k): _parse_voice(v) for k, v in speaker_map_raw.items() if isinstance(v, dict)}

    default_pool = _parse_voice_pool(raw.get("default_pool", [])) if "default_pool" in raw else []
    speaker_pools_raw = raw.get("speaker_pools", {})
    if not isinstance(speaker_pools_raw, dict):
        raise ValueError("'speaker_pools' must be an object.")
    speaker_pools = {
        str(k): _parse_voice_pool(v) for k, v in speaker_pools_raw.items() if isinstance(v, list)
    }

    return default_voice, speaker_map, default_pool, speaker_pools


def _choose_from_pool(pool: list[VoiceConfig], block_index: int, chunk_index: int) -> VoiceConfig:
    idx = (block_index + chunk_index - 2) % len(pool)
    return pool[idx]


def resolve_voice(
    speaker: str,
    default_voice: VoiceConfig,
    speaker_map: dict[str, VoiceConfig],
    default_pool: list[VoiceConfig],
    speaker_pools: dict[str, list[VoiceConfig]],
    block_index: int,
    chunk_index: int,
) -> VoiceConfig:
    if speaker in speaker_pools and speaker_pools[speaker]:
        return _choose_from_pool(speaker_pools[speaker], block_index, chunk_index)
    if speaker in speaker_map:
        return speaker_map[speaker]
    if default_pool:
        return _choose_from_pool(default_pool, block_index, chunk_index)
    return default_voice


def build_piper_command(
    piper_bin: str,
    voice: VoiceConfig,
    output_file: Path,
    sentence_silence: float | None,
    volume: float | None,
) -> list[str]:
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
    if sentence_silence is not None:
        cmd.extend(["--sentence_silence", str(sentence_silence)])
    if volume is not None:
        cmd.extend(["--volume", str(volume)])
    if voice.extra_args:
        cmd.extend(voice.extra_args)
    return cmd


def parse_text_items(
    text: str,
    split_mode: str,
    speaker_line_re: re.Pattern[str],
) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if split_mode == "speaker":
            match = speaker_line_re.match(line)
            if match:
                items.append((match.group(1), match.group(2).strip()))
            else:
                items.append(("narrator", line))
        else:
            items.append(("narrator", line))
    return items


def build_chunks(items: list[tuple[str, str]], chunk_mode: str) -> list[tuple[str, str]]:
    if not items:
        return []
    if chunk_mode == "line":
        return items
    if chunk_mode == "full":
        combined = " ".join(text for _, text in items)
        return [("narrator", combined.strip())] if combined.strip() else []

    # speaker-block: merge consecutive turns from the same speaker
    chunks: list[tuple[str, str]] = []
    cur_speaker, cur_text = items[0]
    buf = [cur_text]
    for speaker, text in items[1:]:
        if speaker == cur_speaker:
            buf.append(text)
        else:
            chunks.append((cur_speaker, " ".join(buf)))
            cur_speaker = speaker
            buf = [text]
    chunks.append((cur_speaker, " ".join(buf)))
    return [(s, t.strip()) for s, t in chunks if t.strip()]


def _expand_clock_time(match: re.Match[str]) -> str:
    hour = int(match.group(1))
    minute = int(match.group(2))
    hour_words = {
        0: "twelve",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve",
        13: "one",
        14: "two",
        15: "three",
        16: "four",
        17: "five",
        18: "six",
        19: "seven",
        20: "eight",
        21: "nine",
        22: "ten",
        23: "eleven",
    }
    if minute == 0:
        return f"{hour_words.get(hour % 24, str(hour))} o'clock"
    if minute < 10:
        return f"{hour_words.get(hour % 24, str(hour))} oh {minute}"
    return f"{hour_words.get(hour % 24, str(hour))} {minute}"


def normalize_tts_text(text: str) -> str:
    out = text.strip()
    for pattern, replacement in ABBREV_PATTERNS:
        out = pattern.sub(replacement, out)
    out = re.sub(r"\b(\d{1,2}):(\d{2})\b", _expand_clock_time, out)
    out = re.sub(r"\s*\.\.\.\s*", ", ", out)
    out = re.sub(r"\s*-\s*", " ", out)
    out = re.sub(r"\s+", " ", out).strip()
    return out


def iter_text_blocks(
    node: Any,
    path_tokens: list[str],
    wanted_keys: set[str],
    path_filter: re.Pattern[str] | None,
    out: list[tuple[str, str]],
) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            token = str(key)
            next_tokens = path_tokens + [token]
            if isinstance(value, str) and key in wanted_keys:
                dotted = ".".join(next_tokens)
                if path_filter is None or path_filter.search(dotted):
                    if value.strip():
                        out.append((dotted, value))
            if isinstance(value, (dict, list)):
                iter_text_blocks(value, next_tokens, wanted_keys, path_filter, out)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            next_tokens = path_tokens + [str(index)]
            if isinstance(item, (dict, list)):
                iter_text_blocks(item, next_tokens, wanted_keys, path_filter, out)


def block_dir_for_path(source_stem: str, dotted_path: str, block_index: int) -> Path:
    tokens = dotted_path.split(".")
    if (
        len(tokens) >= 5
        and tokens[0] == "situations"
        and tokens[2] == "language"
        and tokens[3].startswith("roleplay_")
    ):
        return Path(source_stem) / tokens[1] / tokens[3]
    return Path(source_stem) / f"{block_index:04d}_{slug_join(tokens)}"


def synthesize_line(
    piper_bin: str,
    voice: VoiceConfig,
    text: str,
    output_file: Path,
    sentence_silence: float | None,
    volume: float | None,
) -> None:
    temp_wav = output_file.with_suffix(".tmp.wav")
    cmd = build_piper_command(piper_bin, voice, temp_wav, sentence_silence, volume)
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

    def collect_voice(obj: Any) -> None:
        if not isinstance(obj, dict):
            return
        model = obj.get("model")
        if isinstance(model, str):
            stem = Path(model).name
            match = ACCENT_RE.match(stem)
            if match:
                accents.add(match.group(1))

    collect_voice(raw.get("default"))
    speakers = raw.get("speakers", {})
    if isinstance(speakers, dict):
        for v in speakers.values():
            collect_voice(v)

    default_pool = raw.get("default_pool", [])
    if isinstance(default_pool, list):
        for v in default_pool:
            collect_voice(v)

    speaker_pools = raw.get("speaker_pools", {})
    if isinstance(speaker_pools, dict):
        for pool in speaker_pools.values():
            if isinstance(pool, list):
                for v in pool:
                    collect_voice(v)

    return sorted(accents)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate MP3 files from YAML text fields using Piper."
    )
    parser.add_argument("--input", required=True, help="Input YAML file path.")
    parser.add_argument(
        "--voice-map",
        required=True,
        help="JSON voice map file (supports speakers and speaker_pools).",
    )
    parser.add_argument(
        "--output-dir",
        default="audio_out",
        help="Output root for generated MP3 files (default: audio_out).",
    )
    parser.add_argument(
        "--piper-bin",
        default="piper",
        help="Piper executable name or full path.",
    )
    parser.add_argument(
        "--text-keys",
        default="dialogue,text",
        help="Comma-separated YAML keys to synthesize (default: dialogue,text).",
    )
    parser.add_argument(
        "--path-filter",
        help=(
            "Optional regex on dotted YAML paths (example: "
            "'^situations\\..*\\.language\\.roleplay_\\d+\\.model\\.dialogue$')."
        ),
    )
    parser.add_argument(
        "--split-mode",
        choices=("speaker", "line"),
        default="speaker",
        help="Parse mode: speaker (S: ...) or line (narrator lines).",
    )
    parser.add_argument(
        "--chunk-mode",
        choices=("line", "speaker-block", "full"),
        default="speaker-block",
        help="Chunking mode for synthesis (default: speaker-block).",
    )
    parser.add_argument(
        "--normalize-text",
        action="store_true",
        help="Normalize abbreviations/punctuation for more natural TTS.",
    )
    parser.add_argument(
        "--sentence-silence",
        type=float,
        default=0.04,
        help="Piper sentence silence seconds (default: 0.04).",
    )
    parser.add_argument(
        "--volume",
        type=float,
        default=0.85,
        help="Piper output volume multiplier (default: 0.85).",
    )
    parser.add_argument(
        "--speaker-line-regex",
        default=DEFAULT_SPEAKER_LINE_RE.pattern,
        help="Regex with 2 groups for speaker mode: group1=speaker, group2=text.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional limit on number of matched text blocks.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not call Piper; only write manifest/transcripts.",
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
        return

    if not input_path.exists():
        print(f"Error: input YAML not found: {input_path}")
        sys.exit(1)
    if not voice_map_path.exists():
        print(f"Error: voice map not found: {voice_map_path}")
        sys.exit(1)
    if not args.dry_run and shutil.which(args.piper_bin) is None:
        print(
            f"Error: Piper executable not found: {args.piper_bin}. "
            "Install Piper or pass --piper-bin with a full path."
        )
        sys.exit(2)
    if not args.dry_run and shutil.which("ffmpeg") is None:
        print(
            "Error: ffmpeg executable not found on PATH. "
            "Install ffmpeg to enable MP3 output."
        )
        sys.exit(2)

    text_keys = {k.strip() for k in args.text_keys.split(",") if k.strip()}
    if not text_keys:
        print("Error: --text-keys must include at least one key name.")
        sys.exit(2)

    path_filter = re.compile(args.path_filter) if args.path_filter else None
    speaker_line_re = re.compile(args.speaker_line_regex)

    data = load_yaml(input_path)
    default_voice, speaker_map, default_pool, speaker_pools = load_voice_map(voice_map_path)

    blocks: list[tuple[str, str]] = []
    iter_text_blocks(data, [], text_keys, path_filter, blocks)
    blocks.sort(key=lambda item: item[0])
    if args.limit > 0:
        blocks = blocks[: args.limit]

    source_stem = sanitize_filename(input_path.stem)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.csv"

    total_chunks = 0
    with manifest_path.open("w", encoding="utf-8", newline="") as manifest_file:
        writer = csv.writer(manifest_file)
        writer.writerow(
            [
                "source_file",
                "block_path",
                "block_index",
                "chunk_index",
                "speaker",
                "chunk_text",
                "mp3_path",
                "model_path",
                "chunk_mode",
                "normalized",
            ]
        )

        for block_index, (dotted_path, text_block) in enumerate(blocks, start=1):
            items = parse_text_items(text_block, args.split_mode, speaker_line_re)
            chunks = build_chunks(items, args.chunk_mode)
            pair_dir = output_dir / block_dir_for_path(source_stem, dotted_path, block_index)
            pair_dir.mkdir(parents=True, exist_ok=True)

            transcript_path = pair_dir / "transcript.txt"
            with transcript_path.open("w", encoding="utf-8") as transcript_file:
                transcript_file.write(f"# {dotted_path}\n")
                transcript_file.write(f"# chunk_mode={args.chunk_mode}\n")
                for chunk_index, (speaker, text) in enumerate(chunks, start=1):
                    tts_text = normalize_tts_text(text) if args.normalize_text else text
                    voice = resolve_voice(
                        speaker,
                        default_voice,
                        speaker_map,
                        default_pool,
                        speaker_pools,
                        block_index,
                        chunk_index,
                    )
                    filename = f"{chunk_index:03d}_{sanitize_filename(speaker)}.mp3"
                    mp3_path = pair_dir / filename

                    if not args.dry_run:
                        synthesize_line(
                            args.piper_bin,
                            voice,
                            tts_text,
                            mp3_path,
                            args.sentence_silence,
                            args.volume,
                        )

                    transcript_file.write(f"{chunk_index:03d} {speaker}: {text}\n")
                    writer.writerow(
                        [
                            str(input_path),
                            dotted_path,
                            block_index,
                            chunk_index,
                            speaker,
                            tts_text,
                            str(mp3_path),
                            str(voice.model),
                            args.chunk_mode,
                            str(bool(args.normalize_text)).lower(),
                        ]
                    )
                    total_chunks += 1

    print(f"Matched {len(blocks)} text blocks.")
    print(f"Processed {total_chunks} chunks.")
    print(f"Manifest: {manifest_path}")
    if args.dry_run:
        print("Dry run complete. No MP3 files were generated.")


if __name__ == "__main__":
    main()
