#!/usr/bin/env python3
"""Generate or restyle an image, via five providers (stdlib only).

Providers:
  siliconflow  images/generations, instruction-based edit models such as
               Qwen/Qwen-Image-Edit-2509 (recommended in China: direct access,
               ~CNY 0.30/image). Key: SILICONFLOW_API_KEY.
  openrouter   chat completions, image-output models such as
               google/gemini-2.5-flash-image (nano banana). Key: OPENROUTER_API_KEY.
               Note: image models are region-locked by OpenRouter; text models are not.
  openai       native OpenAI Images API with gpt-image-1. Key: OPENAI_API_KEY.
               Restyle uses /v1/images/edits with input_fidelity=high (keeps faces);
               output size is picked from the input's aspect ratio.
  gemini       Google AI Studio (Gemini API) with gemini-2.5-flash-image (nano
               banana). Key: GEMINI_API_KEY (or GOOGLE_API_KEY). Generous free tier.
  vertex       Google Vertex AI, same Gemini image models through your own GCP
               project. Auth: VERTEX_PROJECT env plus GOOGLE_ACCESS_TOKEN, or a
               logged-in `gcloud` CLI (token fetched automatically).
               VERTEX_LOCATION defaults to "global".

Pass --image to restyle an existing picture (Restyle mode); omit it for
text-to-image (Poster mode).

Add --verify to QC the saved image against the five-ink palette (scripts/style_check.py,
needs Pillow) and --judge to also ask a VLM (Qwen3-VL on SiliconFlow) whether the edit is a
true re-materialization. On failure the image is regenerated once, stricter, and the cleaner
result is kept.

Examples:
  python restyle.py --provider siliconflow --image photo.jpg --prompt-file prompt.txt --out out.png
  python restyle.py --image photo.jpg --prompt "..." --out out.png
  python restyle.py --provider openai --image photo.jpg --prompt "..." --out out.png
  python restyle.py --provider gemini --prompt-file poster.txt --out poster.png
  python restyle.py --provider vertex --image photo.jpg --prompt "..." --out out.png
"""

import argparse
import base64
import json
import mimetypes
import os
import struct
import subprocess
import sys
import urllib.error
import urllib.request
import uuid

SILICONFLOW_URL = "https://api.siliconflow.cn/v1/images/generations"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENAI_URL = "https://api.openai.com/v1/images"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models"
KEY_VARS = {
    "siliconflow": ["SILICONFLOW_API_KEY"],
    "openrouter": ["OPENROUTER_API_KEY"],
    "openai": ["OPENAI_API_KEY"],
    "gemini": ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
    "vertex": [],  # auth via GOOGLE_ACCESS_TOKEN or gcloud, see vertex_auth()
}
DEFAULT_MODELS = {
    "siliconflow": "Qwen/Qwen-Image-Edit-2509",
    "openrouter": "google/gemini-2.5-flash-image",
    "openai": "gpt-image-1",
    "gemini": "gemini-2.5-flash-image",
    "vertex": "gemini-2.5-flash-image",
}


def data_url(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"


def image_size(path):
    """Return (width, height) of a PNG/JPEG file, or None. Stdlib only."""
    with open(path, "rb") as f:
        head = f.read(65536)
    if head[:8] == b"\x89PNG\r\n\x1a\n" and len(head) >= 24:
        w, h = struct.unpack(">II", head[16:24])
        return w, h
    if head[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(head):
            if head[i] != 0xFF:
                i += 1
                continue
            marker = head[i + 1]
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack(">HH", head[i + 5 : i + 9])
                return w, h
            seglen = struct.unpack(">H", head[i + 2 : i + 4])[0]
            i += 2 + seglen
    return None


def pick_openai_size(paths):
    """gpt-image-1 supports 1024x1024 / 1536x1024 / 1024x1536; match input aspect."""
    if paths:
        dims = image_size(paths[0])
        if dims:
            ratio = dims[0] / dims[1]
            if ratio > 1.15:
                return "1536x1024"
            if ratio < 0.87:
                return "1024x1536"
    return "1024x1024"


def openrouter_payload(model, image_paths, prompt):
    content = [{"type": "text", "text": prompt}]
    for p in image_paths:
        content.append({"type": "image_url", "image_url": {"url": data_url(p)}})
    messages = [{"role": "user", "content": content if len(content) > 1 else prompt}]
    payload = {"model": model, "messages": messages}
    if "gemini" in model.lower():
        # gemini image models route only when both output modalities are declared;
        # dedicated image models (seedream, flux, gpt-image) reject the param
        payload["modalities"] = ["image", "text"]
    return payload


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


def siliconflow_payload(model, image_paths, prompt, size):
    payload = {"model": model, "prompt": prompt, "image_size": size or "1024x1024"}
    if image_paths:
        payload["image"] = data_url(image_paths[0])
    return payload


def openai_request(model, image_paths, prompt, size):
    """Return (url, headers, body) for the OpenAI Images API."""
    key = os.environ["OPENAI_API_KEY"]
    headers = {"Authorization": f"Bearer {key}"}
    if image_paths:
        boundary = "----steampunk" + uuid.uuid4().hex
        lines = []
        for field, value in [("model", model), ("prompt", prompt),
                             ("size", size or pick_openai_size(image_paths)),
                             ("input_fidelity", "high"), ("n", "1")]:
            lines += [f"--{boundary}", f'Content-Disposition: form-data; name="{field}"', "", value]
        field = "image" if len(image_paths) == 1 else "image[]"
        for p in image_paths:
            mime = mimetypes.guess_type(p)[0] or "image/png"
            with open(p, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            lines += [f"--{boundary}",
                      f'Content-Disposition: form-data; name="{field}"; filename="{os.path.basename(p)}"',
                      f"Content-Type: {mime}",
                      "Content-Transfer-Encoding: base64", "", data]
        lines += [f"--{boundary}--", ""]
        body = ("\r\n".join(lines)).encode()
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        return f"{OPENAI_URL}/edits", headers, body
    body = json.dumps({"model": model, "prompt": prompt, "n": 1,
                       "size": size or "1024x1024"}).encode()
    headers["Content-Type"] = "application/json"
    return f"{OPENAI_URL}/generations", headers, body


def extract_openai_images(payload):
    found = []
    for item in payload.get("data", []):
        if item.get("b64_json"):
            found.append(f"data:image/png;base64,{item['b64_json']}")
        elif item.get("url"):
            found.append(item["url"])
    return found


def gemini_body(model, image_paths, prompt):
    parts = [{"text": prompt}]
    for p in image_paths:
        mime = mimetypes.guess_type(p)[0] or "image/png"
        with open(p, "rb") as f:
            parts.append({"inline_data": {"mime_type": mime,
                                          "data": base64.b64encode(f.read()).decode()}})
    return {"contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}


def gemini_request(model, image_paths, prompt):
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    url = f"{GEMINI_URL}/{model}:generateContent"
    return url, {"Content-Type": "application/json", "x-goog-api-key": key}, \
        json.dumps(gemini_body(model, image_paths, prompt)).encode()


def extract_gemini_images(payload):
    found = []
    for cand in payload.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                mime = inline.get("mimeType") or inline.get("mime_type") or "image/png"
                found.append(f"data:{mime};base64,{inline['data']}")
    return found


def vertex_auth():
    token = os.environ.get("GOOGLE_ACCESS_TOKEN")
    if token:
        return token
    try:
        out = subprocess.run(["gcloud", "auth", "print-access-token"],
                             capture_output=True, text=True, timeout=60)
    except FileNotFoundError:
        out = None
    if out and out.returncode == 0 and out.stdout.strip():
        return out.stdout.strip()
    sys.exit("Vertex auth failed: set GOOGLE_ACCESS_TOKEN, or install and log in "
             "to the gcloud CLI (gcloud auth application-default login / gcloud auth login)")


def vertex_request(model, image_paths, prompt):
    project = os.environ.get("VERTEX_PROJECT")
    if not project:
        sys.exit("set the VERTEX_PROJECT environment variable (your GCP project id)")
    location = os.environ.get("VERTEX_LOCATION", "global")
    host = "aiplatform.googleapis.com" if location == "global" \
        else f"{location}-aiplatform.googleapis.com"
    url = (f"https://{host}/v1/projects/{project}/locations/{location}"
           f"/publishers/google/models/{model}:generateContent")
    return url, {"Content-Type": "application/json",
                 "Authorization": f"Bearer {vertex_auth()}"}, \
        json.dumps(gemini_body(model, image_paths, prompt)).encode()


QC_RULES = ("\n\nRe-render rules (quality gate failed): fully re-materialize every surface in "
    "aged brass, copper, iron and leather with rivets, pipes and visible mechanisms - a sepia or "
    "warm color filter over the original photo is a reject. The background scene is re-materialized "
    "too, edge to edge, no frame, no borders, no text. Five-ink palette only: no blue, no cyan, "
    "no teal, no purple, no magenta, and no hot photographic green.")


def palette_score(path):
    """Five-ink palette QC via scripts/style_check.py (needs Pillow). None = unavailable."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        from style_check import analyze
    except ImportError:
        return None
    return analyze(path)


def vlm_judge(path, model="Qwen/Qwen3-VL-8B-Instruct"):
    """Ask a VLM whether this is a true re-materialization. True/False, or None if unavailable."""
    key = os.environ.get("SILICONFLOW_API_KEY")
    if not key:
        return None
    body = {"model": model, "max_tokens": 300, "temperature": 0,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": (
                    "Judge this AI-edited image against its intent: turn an ordinary photo into a steampunk "
                    "'re-materialization' where the subject's SURFACE MATERIALS are rebuilt as aged brass, copper, "
                    "iron and leather with rivets, pipes or visible mechanisms.\n"
                    "pass=true when: the main subject clearly reads as metal/leather machinery (plates, rivets, gears, "
                    "boilers, gauges) while keeping the original composition; an engraved or rendered automaton look is fine.\n"
                    "pass=false when: it is mostly the original photo with only a sepia/warm color filter; or large parts "
                    "(fur, paint, fabric, sky) keep their original photographic material; or saturated blue/cyan/purple is "
                    "prominent; or a real-world brand text or logo is clearly readable; or the edit added "
                    "accessories the original clearly does not show (hat, goggles, armor pieces).\n"
                    'Reply with JSON only: {"pass": true/false, "reason": "one short sentence"}')},
                {"type": "image_url", "image_url": {"url": data_url(path)}}]}]}
    req = urllib.request.Request("https://api.siliconflow.cn/v1/chat/completions",
                                 data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {key}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            txt = json.load(r)["choices"][0]["message"]["content"]
    except Exception:
        return None
    i, j = txt.find("{"), txt.rfind("}")
    try:
        return json.loads(txt[i:j + 1]).get("pass")
    except Exception:
        return None


def qc_pass(path, use_judge):
    """Return (ok, palette_result_or_None, judge_result_or_None)."""
    pal = palette_score(path)
    jd = vlm_judge(path) if use_judge else None
    ok = (pal is None or pal["pass"]) and jd is not False
    return ok, pal, jd


def keep_better(a_path, b_path, use_judge):
    """Pick the better of two images by QC scores; returns (path, (palette, judge))."""
    a = palette_score(a_path)
    b = palette_score(b_path)
    ja = vlm_judge(a_path) if use_judge else None
    jb = vlm_judge(b_path) if use_judge else None
    # rank: VLM pass beats judge-fail; palette pass beats palette-fail; then lower pollution
    def rank(pal, jd):
        return (1 if jd is False else 0,
                1 if (pal is not None and not pal["pass"]) else 0,
                (pal or {}).get("bad", 0) + (pal or {}).get("green", 0))
    a, ja = palette_score(a_path), (vlm_judge(a_path) if use_judge else None)
    b, jb = palette_score(b_path), (vlm_judge(b_path) if use_judge else None)
    return (b_path, (b, jb)) if rank(b, jb) < rank(a, ja) else (a_path, (a, ja))


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
    ap.add_argument("--provider", default="siliconflow",
                    choices=["gemini", "openai", "openrouter", "siliconflow", "vertex"])
    ap.add_argument("--image", action="append", default=[], help="source image; repeat for multiple refs")
    ap.add_argument("--prompt", help="prompt text (or use --prompt-file)")
    ap.add_argument("--prompt-file", help="read the prompt from a UTF-8 text file")
    ap.add_argument("--out", required=True, help="output png path")
    ap.add_argument("--model", help="default: provider-specific (%s)" % DEFAULT_MODELS)
    ap.add_argument("--size", help='output size, e.g. "1024x1024" (openai / siliconflow); '
                                   'default: auto from input aspect (openai) or 1024x1024')
    ap.add_argument("--verify", action="store_true",
                    help="QC the saved image against the five-ink palette; on failure regenerate once, stricter")
    ap.add_argument("--judge", action="store_true",
                    help="also ask a VLM (Qwen3-VL via SiliconFlow, uses SILICONFLOW_API_KEY) whether the edit "
                         "is a true re-materialization; implies --verify")
    args = ap.parse_args()

    prompt = args.prompt or (
        open(args.prompt_file, encoding="utf-8").read() if args.prompt_file else None
    )
    if not prompt:
        ap.error("provide --prompt or --prompt-file")
    model = args.model or DEFAULT_MODELS[args.provider]

    missing = [v for v in KEY_VARS[args.provider] if not os.environ.get(v)]
    if args.provider == "gemini" and len(missing) == len(KEY_VARS["gemini"]):
        sys.exit("set the GEMINI_API_KEY (or GOOGLE_API_KEY) environment variable first")
    elif args.provider != "gemini" and args.provider != "vertex" and missing:
        sys.exit(f"set the {missing[0]} environment variable first")

    use_judge = args.judge
    do_verify = args.verify or args.judge

    def run(ptext, out_path):
        if args.provider == "siliconflow":
            url = SILICONFLOW_URL
            headers = {"Content-Type": "application/json",
                       "Authorization": f"Bearer {os.environ[KEY_VARS['siliconflow'][0]]}"}
            body = json.dumps(siliconflow_payload(model, args.image, ptext, args.size)).encode()
            extract = siliconflow_extract
        elif args.provider == "openrouter":
            url = OPENROUTER_URL
            headers = {"Content-Type": "application/json",
                       "Authorization": f"Bearer {os.environ[KEY_VARS['openrouter'][0]]}"}
            body = json.dumps(openrouter_payload(model, args.image, ptext)).encode()
            extract = extract_openrouter_images
        elif args.provider == "openai":
            url, headers, body = openai_request(model, args.image, ptext, args.size)
            extract = extract_openai_images
        elif args.provider == "gemini":
            url, headers, body = gemini_request(model, args.image, ptext)
            extract = extract_gemini_images
        else:
            url, headers, body = vertex_request(model, args.image, ptext)
            extract = extract_gemini_images

        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                payload = json.load(resp)
        except urllib.error.HTTPError as e:
            sys.exit(f"API error {e.code}: {e.read().decode(errors='replace')[:500]}")

        if args.provider == "siliconflow":
            images = [i.get("url") for i in payload.get("images", []) if i.get("url")]
            if not images and payload.get("data"):  # openai-style shape, just in case
                images = [i.get("url") for i in payload["data"] if i.get("url")]
        else:
            images = extract(payload)
        if not images:
            detail = json.dumps(payload, ensure_ascii=False)[:400]
            sys.exit(f"no image in response. payload: {detail}")
        save_image_url(images[0], out_path)
        return len(images)

    n = run(prompt, args.out)

    if do_verify:
        ok, pal, jd = qc_pass(args.out, use_judge)
        if not ok:
            print(f"quality gate failed (palette={pal}, judge={jd}); retrying once, stricter")
            retry = args.out + ".retry.png"
            n = run(prompt + QC_RULES, retry)
            best, (pal, jd) = keep_better(args.out, retry, use_judge)
            if os.path.abspath(best) != os.path.abspath(args.out):
                os.replace(best, args.out)
            if os.path.exists(retry) and os.path.abspath(retry) != os.path.abspath(args.out):
                os.remove(retry)
            print(f"quality gate after retry: palette={pal}, judge={jd}")
    print(f"saved {args.out} via {args.provider}/{model} ({n} image(s) returned)")


def siliconflow_extract(payload):
    return [i.get("url") for i in payload.get("images", []) if i.get("url")]


if __name__ == "__main__":
    main()
