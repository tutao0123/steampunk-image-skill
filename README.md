# Steampunk Image Skill

Turn images into steampunk — the same picture rebuilt in brass — or design Victorian engineering-plate posters from a text brief. Not generic steampunk vibes, not a goggle sticker.

## What it looks like

| Before | After |
| --- | --- |
| <img src="examples/cat/input.jpg" width="400"> | <img src="examples/cat/output.jpg" width="400"> |

Same cat, same yawn — re-built in brass, one real mechanism visible. Twelve worked runs (input + prompt + output each) live in [examples/](./examples/README.md); every input photo there is CC0 / public domain, so you can reuse them in your own posts.

## Avatars that survive the circle crop

A dedicated **Avatar mode**: face locked, square 1:1, one small mechanism at the crop edge, plain walnut background. Nine CC0/PD portraits — paintings and museum busts — forged as one set:

<p align="center">
  <img src="examples/avatar-grid.jpg" width="560" alt="nine steampunk avatars">
</p>

Rules and template: [SKILL.md → Avatar mode](#avatar-mode), [prompt.md → AVATAR](prompt.md). Individual portraits: [examples/avatar/](examples/README.md#avatar-mode--circle-crop-safe).

## Twelve restyles

Vehicles, pets, food, streets, buildings, skies — every run keeps the original composition and builds in one readable mechanism. Click any name for input + prompt + full-size output.

**[Car](examples/car/)** · vertical-boiler engine

<p><img src="examples/car/input.jpg" width="47%" alt="car before"><img src="examples/car/output.jpg" width="47%" alt="car after"></p>

**[Bicycle](examples/bicycle/)** · brass chain drive

<p><img src="examples/bicycle/input.jpg" width="47%" alt="bicycle before"><img src="examples/bicycle/output.jpg" width="47%" alt="bicycle after"></p>

**[Motorcycle](examples/motorcycle/)** · boiler between the tanks

<p><img src="examples/motorcycle/input.jpg" width="47%" alt="motorcycle before"><img src="examples/motorcycle/output.jpg" width="47%" alt="motorcycle after"></p>

**[Biplane](examples/airplane/)** · steam radial engine

<p><img src="examples/airplane/input.jpg" width="47%" alt="airplane before"><img src="examples/airplane/output.jpg" width="47%" alt="airplane after"></p>

**[Airship](examples/balloon/)** · riveted dirigible

<p><img src="examples/balloon/input.jpg" width="47%" alt="balloon before"><img src="examples/balloon/output.jpg" width="47%" alt="balloon after"></p>

**[Cat](examples/cat/)** · clockwork automaton

<p><img src="examples/cat/input.jpg" width="47%" alt="cat before"><img src="examples/cat/output.jpg" width="47%" alt="cat after"></p>

**[Dog](examples/dog/)** · clockwork automaton

<p><img src="examples/dog/input.jpg" width="47%" alt="dog before"><img src="examples/dog/output.jpg" width="47%" alt="dog after"></p>

**[Latte](examples/coffee/)** · boiler-wall cup

<p><img src="examples/coffee/input.jpg" width="47%" alt="coffee before"><img src="examples/coffee/output.jpg" width="47%" alt="coffee after"></p>

**[Street busker](examples/street/)** · calliope-guitar

<p><img src="examples/street/input.jpg" width="47%" alt="street before"><img src="examples/street/output.jpg" width="47%" alt="street after"></p>

**[Clock tower](examples/clocktower/)** · exposed escapement

<p><img src="examples/clocktower/input.jpg" width="47%" alt="clocktower before"><img src="examples/clocktower/output.jpg" width="47%" alt="clocktower after"></p>

**[Dusk skyline](examples/skyline/)** · gear-crown beacon

<p><img src="examples/skyline/input.jpg" width="47%" alt="skyline before"><img src="examples/skyline/output.jpg" width="47%" alt="skyline after"></p>

**[1783 portrait](examples/portrait/)** · spring automaton

<p><img src="examples/portrait/input.jpg" width="47%" alt="portrait before"><img src="examples/portrait/output.jpg" width="47%" alt="portrait after"></p>

## Two modes

| You give | You get |
| --- | --- |
| A photo + "把它变成蒸汽朋克" | **Restyle**: same composition, same subject — materials re-built as brass/copper/iron/leather, palette forced to five inks, one real mechanism built into the subject |
| A portrait + "给我做个头像" | **Avatar**: square brass-plate bust that survives a circular crop — face locked, one mechanism at the edge |
| A text brief ("城市骑行活动海报") | **Poster**: a Victorian engineering-plate design with a locked mechanical thesis, layout, and stamped typography |

The restyle mode is image-first: the original photo is passed to the image tool together with the prompt, a **fidelity contract** locks composition and identity, and drift (new composition, replaced subject, neon surviving) is rejected at the quality gate.

## Install

With the open [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add tutao0123/steampunk-image-skill
```

Cursor only:

```bash
npx skills add tutao0123/steampunk-image-skill --agent cursor
```

Codex only:

```bash
npx skills add tutao0123/steampunk-image-skill --agent codex
```

All agents on this machine:

```bash
npx skills add tutao0123/steampunk-image-skill -g --all
```

Then drop a photo ("把这张图改成蒸汽朋克风格") or give a brief ("给茶馆音乐会出一张蒸汽朋克海报").

## Where images come from

- Agents with a built-in image tool: the skill attaches the original photo and prompt directly.
- Coding agents without one (Codex 等): the skill calls `scripts/restyle.py` — a single-file, stdlib-only Python script. Pick your provider with `--provider`; every call is one command:

| `--provider` | Service / model | Auth (env) | Notes |
| --- | --- | --- | --- |
| `siliconflow` *(default)* | Qwen-Image-Edit-2509 on [SiliconFlow](https://siliconflow.cn) | `SILICONFLOW_API_KEY` | ≈¥0.30/image, direct access in China |
| `openrouter` | [OpenRouter](https://openrouter.ai) image models — `google/gemini-2.5-flash-image`, `black-forest-labs/flux.2-klein-4b` (tested), `bytedance-seed/seedream-5-0-lite`, ... | `OPENROUTER_API_KEY` | one key, many models; pass any image model with `--model`. Caveats: image models are region-locked on some networks, and seedream's img2img endpoint was returning 500s at last test |
| `openai` | native [OpenAI Images API](https://platform.openai.com/docs/api-reference/images) — `gpt-image-1` | `OPENAI_API_KEY` | edits use `input_fidelity=high` (keeps faces); size auto-matched to the input's aspect |
| `gemini` | [Google AI Studio](https://aistudio.google.com) — `gemini-2.5-flash-image` (nano banana) | `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) | direct from Google, generous free tier |
| `vertex` | [Vertex AI](https://cloud.google.com/vertex-ai) — the same Gemini image models inside your GCP project | `VERTEX_PROJECT` + `GOOGLE_ACCESS_TOKEN`, or a logged-in `gcloud` CLI | `VERTEX_LOCATION` defaults to `global` |

```bash
python scripts/restyle.py --image photo.jpg --prompt-file restyle-prompt.txt --out steampunk.png   # default: SiliconFlow
python scripts/restyle.py --provider openai     --image photo.jpg --prompt-file restyle-prompt.txt --out steampunk.png
python scripts/restyle.py --provider gemini     --image photo.jpg --prompt-file restyle-prompt.txt --out steampunk.png
python scripts/restyle.py --provider vertex     --image photo.jpg --prompt-file restyle-prompt.txt --out steampunk.png
python scripts/restyle.py --provider openrouter --prompt-file poster.txt --out poster.png          # Poster mode works on every provider
```

All providers speak the same prompt contract (Locked / Transformed / one mechanism), so results are comparable — swap the flag, keep the prompt.

**Quality gate**: add `--verify` for a palette check (`scripts/style_check.py`) and `--judge` for a VLM art-director score (Qwen3-VL via SiliconFlow, 0-100). Scoring is lenient by design — partial restyles with some retained organic texture can still pass at a score of 70+; a failed gate triggers one automatic, stricter regeneration and the higher-scored result is kept.

## Visual lock (both modes)

- Inks: antique brass, oxidized copper, iron rust red, warm parchment beige, deep walnut brown
- Poster paper: aged vellum / letterpress; restyle keeps the photo's scene, re-materialized
- Type: engraved Victorian serif title; condensed stencil labels
- Forbidden: neon, cyan, magenta, cute cartoon steampunk, goggles-as-subject, cyberpunk, glossy 3D renders

## Files

| File | What it is |
| --- | --- |
| [SKILL.md](./SKILL.md) | Runbook: mode selection, restyle workflow, poster workflow, quality gate |
| [prompt.md](./prompt.md) | Fill-in prompt template per mode |
| [style.md](./style.md) | Ink, paper, type, print language; restyle exceptions |
| [machines.md](./machines.md) | Subject → real mechanism mapping; photo reference rules |
| [layouts.md](./layouts.md) | Poster plate layouts |
| [examples.md](./examples.md) | Worked examples, mode-tagged |
| [examples/](./examples/README.md) | Real runs: input + prompt + output for 12 restyles + 9 avatars |
| [scripts/restyle.py](./scripts/restyle.py) | Multi-provider image caller: SiliconFlow / OpenRouter / OpenAI / Gemini / Vertex (stdlib only) |

## License

MIT. The example input photos in `examples/` are CC0 or public domain (credits in [examples/README.md](./examples/README.md)); example outputs are generated images shown for demonstration.

