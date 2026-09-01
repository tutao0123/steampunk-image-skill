---
name: steampunk-image-skill
description: Turn images into steampunk / Victorian industrial style, or design a steampunk poster from a text brief. Use whenever the user shares a photo or image and wants it restyled as steampunk, brass machinery, clockwork, automata, or Victorian industrial art (蒸汽朋克、机械风、复古机械、把图片变成机械/蒸汽朋克风格), or asks for a steampunk poster, flyer, or cover from a description. Also use to iterate on a failed steampunk generation.
---

# Steampunk Image

Two modes. Pick by input, not by mood:

- **Restyle** — an image was attached (or a specific real thing was named: "my bike", "这张照片"). Keep the picture, change its materials. The output must read as *the same picture rebuilt in brass*: same composition, same subject, same angle.
- **Poster** — no image, or the word 海报 / poster / cover was used for a *new* design. Produce a Victorian engineering-plate poster from the brief.

Companion files (read what the mode needs, not all of it):

- `prompt.md` — fill-in prompt templates, one per mode. Read it before generating.
- `style.md` — locked ink / paper / type system. Restyle exceptions at the end.
- `machines.md` — subject → real mechanism mapping. Read when choosing the mechanism.
- `layouts.md` — poster plate layouts. Poster mode only.
- `examples.md` — mode-tagged worked examples. Read one before your first run in each mode.

If running as a single file with no companions, follow this runbook and keep the five-ink palette and the forbidden lists.

## Mode selection

| Input | Mode |
| --- | --- |
| Photo/image attached, style change asked (改造/合成/变成蒸汽朋克风) | **Restyle** |
| A real thing named but not attached ("我的自行车", "我们公司楼") | Restyle posture: reconstruct the subject faithfully, then restyle; say that you approximated it |
| Text brief only, new artwork wanted | **Poster** |
| Selfie/group + "变成机器人/automaton" | Restyle with full rebuild (faces rule below) |

Ambiguous ("帮我搞个蒸汽朋克"), no image → Poster. When both could apply, ask one short question or default to Restyle if any image is in context.

## Restyle mode: image in → steampunk out

The image is the base, not inspiration. Pass the original file to the image tool together with the prompt (img2img / image edit). Generating from text alone when you could attach the image is the failure this mode exists to prevent.

### 1. Fidelity contract

Write two short lists before prompting — they go verbatim into the prompt and are what stops drift:

- **Locked** — composition, camera angle, framing, subject identity, head count, pose, which object is which. Aspect ratio = the input image's ratio.
- **Transformed** — materials (skin/metal/plastic/concrete → brushed brass, oxidized copper, riveted iron, walnut, leather, etched steel), palette (everything → the five inks in `style.md`; kill neon/cyan/magenta at the source), surfaces (rivets, patina, soot in recesses), light (warm soot-and-steam haze, workshop glow).

### 2. One mechanism, built in

Pick **one** readable mechanism that belongs to the photo's main subject — `machines.md` maps subjects to mechanisms. Build it *into* the subject: the bicycle's chain becomes a real brass chain drive; the kettle grows a boiler and pressure gauge; the building's clock face gets an exposed escapement. Never sprinkle gears as stickers, and never add machines the picture doesn't need.

### 3. Faces

- Restyle ask (变风格 / 合成风格) → keep the face's structure and identity; re-materialize it: etched-brass skin, lens or gauge eyes, clockwork at the temple. Not a costume filter, not a different person.
- Rebuild ask (变成机器人 / automaton / 机械人) → full automaton plate: pose and hair silhouette survive, skin does not. Use `layouts.md` portrait-automaton / group-automaton, 3:4 plate framing (this is the one restyle case where the output becomes a poster).

### 4. Tool handling

- Reference image + strength/denoise available → strength ≈ 0.5–0.65: high enough to re-materialize materials, low enough to keep composition.
- Text→image only → say so, then approximate: describe the photo's composition and subject in the prompt ("same composition as: …") and warn the result approximates the photo.
- Aspect: output follows the input. Only poster mode forces 3:4.

### 5. Generate

Fill the RESTYLE template in `prompt.md` — keep the Locked/Transformed lines in the prompt. Filename: `steampunk-{slug}.png`. One image, no unsolicited variations.

## Poster mode: brief in → plate out

Lock four decisions in a 4-line brief before generating. Do not skip the thesis.

```text
Subject: ...
Thesis: {one real mechanism} because {why it belongs to this topic}
Layout: {hero-assembly | cutaway | exploded | gauge-board | dual-ink | portrait-automaton | group-automaton}
Text: title="..." / date="..." / place="..." / labels=part numbers
```

- **Thesis (mandatory)** — choose one: gears meshing · piston travel · boiler + pipe routing · gauge cluster · chain/sprocket drive. Map the topic onto machinery with `machines.md`; a scene with bolts glued on fails.
- **Layout** — pick one from `layouts.md`. `hero-assembly` if unsure. Never mix two full layouts.
- **On-image text** — stamped title 2–5 English words in engraved Victorian serif; legend box (date/place/subtitle, short Chinese OK); callouts are part numbers plus 1–3 word labels; no paragraphs, no slogan stacking.
- **Event poster** → title + date + place must appear on the plate.

Generate with the POSTER template in `prompt.md`. Aspect 3:4, filename `steampunk-{slug}.png`.

## Quality gate

Reject and regenerate **once** (same thesis/layout, tighter prompt) if any check fails:

- **Restyle**: composition drifted · subject unrecognizable or replaced · neon/cyan/magenta survived · mechanism reads as stickers · face became a stranger
- **Poster**: no readable mechanism (gears don't mesh, pipes go nowhere) · palette broke · cute/anime/goggles-as-subject · glossy CGI look · event text missing · machine is an ornament, not the hero

If the second attempt fails the same check, show it anyway, name the miss, and ask one question (change mechanism, layout, or reference handling — one only).

## Deliver

Show the image, then two short sentences:

- Restyle: what was locked and which mechanism was built in. Poster: thesis + layout used, and what text went on the plate.

Stop. Iterate by changing **one** input at a time: reference handling, mechanism, layout, or text.
