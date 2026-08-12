#!/usr/bin/env python3
"""Generate a single gpt-image-1 image with a native transparent background,
via a raw HTTP call to the OpenAI Images API.

Bypasses the openai Python SDK entirely: the installed SDK version (1.59.9,
pinned after repeated corrupted installs of newer versions on this network
drive) predates the `background` parameter that gpt-image-1 supports. Rather
than keep fighting SDK version issues, this calls the REST endpoint directly
with `requests`, which is stable and already installed.
"""
from __future__ import annotations

import argparse
import base64
import os
from pathlib import Path

import requests

API_URL = "https://api.openai.com/v1/images/generations"


def generate_transparent_image(prompt: str, size: str, model: str = "gpt-image-1") -> bytes:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set.")

    resp = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "prompt": prompt,
            "size": size,
            "background": "transparent",
        },
        timeout=180,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"OpenAI API error {resp.status_code}: {resp.text[:2000]}")

    data = resp.json()
    b64 = data["data"][0]["b64_json"]
    return base64.b64decode(b64)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a transparent-background image via raw HTTP")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--size", default="1024x1536")
    parser.add_argument("--model", default="gpt-image-1")
    args = parser.parse_args()

    png_bytes = generate_transparent_image(args.prompt, args.size, args.model)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(png_bytes)
    print(f"Saved: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
