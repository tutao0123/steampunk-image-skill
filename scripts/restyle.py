#!/usr/bin/env python3
"""Generate or restyle an image, via OpenRouter or SiliconFlow.

Providers:
  openrouter   chat completions, image-output models such as
               google/gemini-2.5-flash-image (nano banana). Key: OPENROUTER_API_KEY.
               Note: image models are region-locked by OpenRouter; text models are not.
  siliconflow  images/generations, instruction-based edit models such as
               Qwen/Qwen-Image-Edit-2509 (recommended in China: direct access,
               ~CNY 0.30/image). Key: SILICONFLOW_API_KEY.

Pass --image to restyle an existing picture (Restyle mode); omit it for
text-to-image (Poster mode).

Examples:
  python restyle.py --provider siliconflow --image photo.jpg --prompt-file prompt.txt --out out.png
  python restyle.py --image photo.jpg --prompt "..." --out out.png
  python restyle.py --prompt-file poster.txt --out poster.png
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.request

ENDPOINTS = {
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "siliconflow": "https://api.siliconflow.cn/v1/images/generations",
}
KEY_VARS = {"openrouter": "OPENROUTER_API_KEY", "siliconflow": "SILICONFLOW_API_KEY"}
DEFAULT_MODELS = {
    "openrouter": "google/gemini-2.5-flash-image",
    "siliconflow": "Qwen/Qwen-Image-Edit-2509",
}


def data_url(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"


def openrouter_payload(model, image_paths, prompt):
    content = [{"type": "text", "text": prompt}]
    for p in image_paths:
        content.append({"type": "image_url", "image_url": {"url": data_url(p)}})
    messages = [{"role": "user", "content": content if len(content) > 1 else prompt}]
    return {"model": model, "messages": messages}


def extract_openrouter_images(payload):
    """Pull generated images out of a chat completion response; nesting has
    varied across OpenRouter versions, so accept every shape seen so far."""
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


def siliconflow_payload(model, image_paths, prompt):
    payload = {"model": model, "prompt": prompt, "image_size": "1024x1024"}
    if image_paths:
        payload["image"] = data_url(image_paths[0])
    return payload


def save_image_url(url, out_path):
    if url.startswith("data:"):
        _, _, b64 = url.partition(",")
        if not b64:
            raise SystemExit(f"unexpected image payload: {url[:60]}")
        data = base64.b64decode(b64)
    elif url.startswith("http"):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    else:
        raise SystemExit(f"unsupported image url: {url[:60]}")
    with open(out_path, "wb") as f:
        f.write(data)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--provider", choices=sorted(ENDPOINTS), default="siliconflow")
    ap.add_argument("--image", action="append", default=[], help="source image; repeat for multiple refs")
    ap.add_argument("--prompt", help="prompt text (or use --prompt-file)")
    ap.add_argument("--prompt-file", help="read the prompt from a UTF-8 text file")
    ap.add_argument("--out", required=True, help="output png path")
    ap.add_argument("--model", help="default: provider-specific (%s)" % DEFAULT_MODELS)
    args = ap.parse_args()

    prompt = args.prompt or (
        open(args.prompt_file, encoding="utf-8").read() if args.prompt_file else None
    )
    if not prompt:
        ap.error("provide --prompt or --prompt-file")
    model = args.model or DEFAULT_MODELS[args.provider]
    api_key = os.environ.get(KEY_VARS[args.provider])
    if not api_key:
        sys.exit(f"set the {KEY_VARS[args.provider]} environment variable first")

    if args.provider == "openrouter":
        body = openrouter_payload(model, args.image, prompt)
    else:
        body = siliconflow_payload(model, args.image, prompt)

    req = urllib.request.Request(
        ENDPOINTS[args.provider],
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"API error {e.code}: {e.read().decode(errors='replace')[:500]}")

    if args.provider == "openrouter":
        images = extract_openrouter_images(payload)
    else:
        images = [i.get("url") for i in payload.get("images", []) if i.get("url")]
        if not images and payload.get("data"):  # openai-style shape, just in case
            images = [i.get("url") for i in payload["data"] if i.get("url")]
    if not images:
        detail = json.dumps(payload, ensure_ascii=False)[:400]
        sys.exit(f"no image in response. payload: {detail}")

    save_image_url(images[0], args.out)
    print(f"saved {args.out} via {args.provider}/{model} ({len(images)} image(s) returned)")


if __name__ == "__main__":
    main()
