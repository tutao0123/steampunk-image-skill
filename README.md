# Steampunk Image Skill

Turn images into steampunk — the same picture rebuilt in brass — or design Victorian engineering-plate posters from a text brief. Not generic steampunk vibes, not a goggle sticker.

## What it looks like

| Before | After |
| --- | --- |
| <img src="examples/cat/input.jpg" width="400"> | <img src="examples/cat/output.jpg" width="400"> |

Same cat, same yawn — re-built in brass, one real mechanism visible. Twelve worked runs (input + prompt + output each) live in [examples/](./examples/README.md); every input photo there is CC0 / public domain, so you can reuse them in your own posts.

## Twelve restyles

Vehicles, pets, food, streets, buildings, skies — every run keeps the original composition and builds in one readable mechanism. Click any folder name for input + prompt + full-size output.

<table>
  <colgroup><col width="25%"><col width="25%"><col width="25%"><col width="25%"></colgroup>
  <tr><th>Before</th><th>After</th><th>Before</th><th>After</th></tr>
  <tr><td><a href="examples/car/"><img src="examples/car/input.jpg" width="100%" alt="car before"></a><br><sub><b><a href="examples/car/">Car</a></b> · vertical-boiler engine</sub></td><td><img src="examples/car/output.jpg" width="100%" alt="car after"></td><td><a href="examples/bicycle/"><img src="examples/bicycle/input.jpg" width="100%" alt="bicycle before"></a><br><sub><b><a href="examples/bicycle/">Bicycle</a></b> · brass chain drive</sub></td><td><img src="examples/bicycle/output.jpg" width="100%" alt="bicycle after"></td></tr>
  <tr><td><a href="examples/motorcycle/"><img src="examples/motorcycle/input.jpg" width="100%" alt="motorcycle before"></a><br><sub><b><a href="examples/motorcycle/">Motorcycle</a></b> · boiler between the tanks</sub></td><td><img src="examples/motorcycle/output.jpg" width="100%" alt="motorcycle after"></td><td><a href="examples/airplane/"><img src="examples/airplane/input.jpg" width="100%" alt="airplane before"></a><br><sub><b><a href="examples/airplane/">Biplane</a></b> · steam radial engine</sub></td><td><img src="examples/airplane/output.jpg" width="100%" alt="airplane after"></td></tr>
  <tr><td><a href="examples/balloon/"><img src="examples/balloon/input.jpg" width="100%" alt="balloon before"></a><br><sub><b><a href="examples/balloon/">Airship</a></b> · riveted dirigible</sub></td><td><img src="examples/balloon/output.jpg" width="100%" alt="balloon after"></td><td><a href="examples/cat/"><img src="examples/cat/input.jpg" width="100%" alt="cat before"></a><br><sub><b><a href="examples/cat/">Cat</a></b> · clockwork automaton</sub></td><td><img src="examples/cat/output.jpg" width="100%" alt="cat after"></td></tr>
  <tr><td><a href="examples/dog/"><img src="examples/dog/input.jpg" width="100%" alt="dog before"></a><br><sub><b><a href="examples/dog/">Dog</a></b> · clockwork automaton</sub></td><td><img src="examples/dog/output.jpg" width="100%" alt="dog after"></td><td><a href="examples/coffee/"><img src="examples/coffee/input.jpg" width="100%" alt="coffee before"></a><br><sub><b><a href="examples/coffee/">Latte</a></b> · boiler-wall cup</sub></td><td><img src="examples/coffee/output.jpg" width="100%" alt="coffee after"></td></tr>
  <tr><td><a href="examples/street/"><img src="examples/street/input.jpg" width="100%" alt="street before"></a><br><sub><b><a href="examples/street/">Street busker</a></b> · calliope-guitar</sub></td><td><img src="examples/street/output.jpg" width="100%" alt="street after"></td><td><a href="examples/clocktower/"><img src="examples/clocktower/input.jpg" width="100%" alt="clocktower before"></a><br><sub><b><a href="examples/clocktower/">Clock tower</a></b> · exposed escapement</sub></td><td><img src="examples/clocktower/output.jpg" width="100%" alt="clocktower after"></td></tr>
  <tr><td><a href="examples/skyline/"><img src="examples/skyline/input.jpg" width="100%" alt="skyline before"></a><br><sub><b><a href="examples/skyline/">Dusk skyline</a></b> · gear-crown beacon</sub></td><td><img src="examples/skyline/output.jpg" width="100%" alt="skyline after"></td><td><a href="examples/portrait/"><img src="examples/portrait/input.jpg" width="100%" alt="portrait before"></a><br><sub><b><a href="examples/portrait/">1783 portrait</a></b> · spring automaton</sub></td><td><img src="examples/portrait/output.jpg" width="100%" alt="portrait after"></td></tr>
</table>

## Avatars that survive the circle crop

A dedicated **Avatar mode**: face locked, square 1:1, one small mechanism at the crop edge, plain walnut background. Nine CC0/PD portraits — paintings and museum busts — forged as one set:

<p align="center">
  <img src="examples/avatar-grid.jpg" width="560" alt="nine steampunk avatars">
</p>

Rules and template: [SKILL.md → Avatar mode](#avatar-mode), [prompt.md → AVATAR](prompt.md). Individual portraits: [examples/avatar/](examples/README.md#avatar-mode--circle-crop-safe).

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
| `openrouter` | nano banana / gpt-image-1 via [OpenRouter](https://openrouter.ai) | `OPENROUTER_API_KEY` | one key, many models; image models are region-locked by OpenRouter on some networks |
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
