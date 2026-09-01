#!/usr/bin/env python3
"""Generate or restyle an image via the OpenRouter chat completions API.

Works with image-output models such as google/gemini-2.5-flash-image-preview
(nano banana). Pass --image to restyle an existing picture (Restyle mode);
omit it for text-to-image (Poster mode). The API key comes from the
OPENROUTER_API_KEY environment variable.

Examples:
  python restyle.py --image photo.jpg --prompt-file prompt.txt --out steampunk-bike.png
  python restyle.py --prompt-file poster.txt --out steampunk-poster.png
  python restyle.py --image photo.jpg --prompt "..." --out out.png --model openai/gpt-image-1
(gpt-image-1 may require OpenRouter's dedicated Image API instead of chat
completions; if the request fails, fall back to the default Gemini model.)
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.request

API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-2.5-flash-image"


def data_url(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"


def build_messages(image_paths, prompt):
    content = [{"type": "text", "text": prompt}]
    for p in image_paths:
        content.append({"type": "image_url", "image_url": {"url": data_url(p)}})
    return [{"role": "user", "content": content if len(content) > 1 else prompt}]


def extract_images(payload):
    """Pull every generated image out of a chat completion response.

    OpenRouter returns them under choices[].message.images[]; the exact
    nesting has varied, so accept both {"image_url": {...}} and raw strings.
    """
    found = []
    for choice in payload.get("choices", []):
        message = choice.get("message", {})
        for item in message.get("images") or []:
            if isinstance(item, str):
                found.append(item)
            elif isinstance(item, dict):
                url = item.get("image_url")
                if isinstance(url, dict):
                    url = url.get("url")
                if url:
                    found.append(url)
        inline = message.get("content")
        if isinstance(inline, list):
            for part in inline:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    url = part.get("image_url")
                    if isinstance(url, dict):
                        url = url.get("url")
                    if url and url.startswith("data:"):
                        found.append(url)
    return found


def save_data_url(url, out_path):
    header, _, b64 = url.partition(",")
    if not b64:
        raise SystemExit(f"unexpected image payload (no base64 data): {header[:60]}")
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(b64))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--image", action="append", default=[], help="source image; repeat for multiple refs")
    ap.add_argument("--prompt", help="prompt text (or use --prompt-file)")
    ap.add_argument("--prompt-file", help="read the prompt from a UTF-8 text file")
    ap.add_argument("--out", required=True, help="output png path")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    prompt = args.prompt or (
        open(args.prompt_file, encoding="utf-8").read() if args.prompt_file else None
    )
    if not prompt:
        ap.error("provide --prompt or --prompt-file")
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        sys.exit("set the OPENROUTER_API_KEY environment variable first")

    body = json.dumps(
        {"model": args.model, "messages": build_messages(args.image, prompt)}
    ).encode()
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        sys.exit(f"API error {e.code}: {detail}")

    images = extract_images(payload)
    if not images:
        text = ""
        try:
            text = payload["choices"][0]["message"]["content"]
        except Exception:
            pass
        sys.exit(f"no image in response. model text: {str(text)[:400]}")
    save_data_url(images[0], args.out)
    print(f"saved {args.out} ({len(images)} image(s) returned)")


if __name__ == "__main__":
    main()
