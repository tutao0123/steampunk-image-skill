---
name: Steampunk Poster
description: Use this when generating a steampunk, Victorian industrial, or mechanical editorial poster / engineering-plate image from a subject. Also use it to iterate, tighten layout, or remap a brief onto real machinery.
---

# Steampunk Poster

Produce one Victorian industrial engineering-plate poster. This is a design system, not a vibes prompt. Every run must make four locked decisions before generating: **subject**, **mechanical thesis**, **layout**, **on-image text**.

Do not invent a second style. Do not skip the thesis. Do not generate until the four decisions are written down.

Companion files in this repo (read them when needed):

- `style.md` — ink, paper, type, print language
- `layouts.md` — plate layouts, including portrait/group automata
- `machines.md` — how to turn a topic into real machinery
- `examples.md` — worked briefs
- `prompt.md` — final prompt template

If this skill is running as a single file with no companions, the same rules below still apply.

## When to use / when not

Use for: posters, editorial covers, event flyers, mechanical plates, cutaways; also photos of cities, vehicles, landscapes, selfies, and group shots transcribed into this system.

Do not use for: cute character art, fashion looks, cyberpunk, photoreal product shots, logos, UI mockups, or anything that only needs "steampunk goggles" as dressing. A portrait must become an automaton plate, not a person in costume.

## 1. Intake

If the user already named a subject, use it. Ask at most one short question, and only if a required field is missing.

Extract:

| Field | Required | Default |
| --- | --- | --- |
| Subject / brief | yes | — |
| Title | no | invent a short Victorian English title from the brief |
| Date / place | no | omit from the plate |
| Language of on-image text | no | match the user's request; title may stay English if Chinese would likely distort |
| Layout | no | pick from `layouts.md` (hero assembly if unsure) |
| Mechanical thesis | no | pick from `machines.md` |

Write a 4-line brief to yourself before prompting:

```
Subject: ...
Thesis: {one real mechanism} because {why it belongs to this topic}
Layout: {hero-assembly | cutaway | exploded | gauge-board | dual-ink | portrait-automaton | group-automaton}
Text: title="..." / date="..." / place="..." / labels=part numbers
```

If the brief is an event poster, title + date + place must appear on the plate (title stamped, date/place in the legend box).

If the user attached a photo, classify it before generating:
- engineering drawing → **style** reference
- city / landscape / vehicle → **subject** reference (silhouette only)
- selfie or group → **portrait** reference; pick `portrait-automaton` or `group-automaton`
Neon night skylines may be subject shape only, never style.

## 2. Mechanical thesis (mandatory)

The picture fails if it is only atmosphere. Choose **one** primary logic and make it readable:

1. Gears meshing (pitch circle, at least two wheels, a pinion)
2. Piston travel (cylinder, rod, crosshead, crank)
3. Boiler + pipe routing (steam dome, valves, copper runs that connect)
4. Gauge cluster (bourdon gauges, needle positions, a valve wheel)
5. Chain / sprocket / belt drive (for cycling, mill, conveyor topics)

Map the topic onto machinery. Never illustrate the topic as a cute scene with bolts glued on.

- City cycling → brass bicycle: chainring, chain, rear sprocket, caliper, frame lugs
- Concert / tea house → pipe organ, phonograph, or steam calliope; pipes as the hero
- AI / lab / science → orrery, difference engine, or instrument bench with gauges
- City / map / travel → clockwork transit: rails, semaphore, boiler locomotive cutaway
- Food / coffee / tea → espresso boiler, pressure group, valve tree
- War / industry → riveted hull, turret gear, steam hammer

If the user already named a machine, that machine is the thesis. See `machines.md`.

## 3. Layout

Pick one. Do not mix two full layouts in one plate.

| Id | Use when |
| --- | --- |
| `hero-assembly` | default posters; machine fills the center |
| `cutaway` | "how it works", engines, boilers |
| `exploded` | parts, kits, product-as-machine |
| `gauge-board` | events with lots of data (date, program, rules) |
| `dual-ink` | two themes (e.g. city + night ride); one restrained overprint only |
| `portrait-automaton` | a selfie or single portrait, rebuilt as one brass automaton |
| `group-automaton` | a group photo, 2–6 labeled automata on one plate |

All layouts share: generous parchment margin, dimension lines, numbered callouts, a small legend box, 3:4 portrait.

Details in `layouts.md`.

## 4. On-image text

Image models garble long or mixed-script type. Keep lettering sparse and hierarchical.

1. **Title** — 2–5 words, engraved Victorian serif, stamped / foil-pressed. Prefer English for the stamped title even if the chat is Chinese, unless the user insisted on a Chinese title.
2. **Legend box** — date, place, one-line subtitle. Condensed industrial sans or stencil. Chinese is OK here if the user asked; keep it short (title / 日期 / 地点).
3. **Callouts** — part numbers (`Fig. 12`, `A`, `B`) plus 1–3 word English labels (`CHAIN RING`, `STEAM DOME`).
4. **No paragraphs** on the plate. No slogan stacking. No QR codes unless asked.

If Chinese title is required, still generate, but expect distortion; offer a second pass with English stamped title + Chinese in the legend.

## 5. Assemble the prompt

One prompt, English, in this order. Do not drop the forbidden list. Fill `{...}` from the 4-line brief.

Use the template in `prompt.md`. If that file is missing, use this:

```text
A complete editorial poster designed as a Victorian industrial engineering plate, steampunk mechanical design system.

Plate job: {layout id}, 3:4 portrait, museum print quality, letterpress on aged vellum.

Mechanical thesis (must be readable): {thesis}. Show real mechanical logic, not decorative gears.

Hero machine: {concrete machine, materials, what is in the center}.

Visual system:
- Limited ink palette only: antique brass, oxidized copper, iron rust red, warm parchment beige, deep walnut brown. No neon, no cyan, no magenta, no clean digital gradients.
- Paper: aged blueprint / vellum / letterpress stock, visible fiber, slight foxing, faint grid or compass marks.
- Texture: brushed brass, rivets, gear teeth, piston rods, pressure gauges, valve wheels, etched metal, letterpress impression, light soot and steam haze. Not glossy 3D CGI.
- Typography: engraved Victorian serif for the main title; condensed industrial sans or stencil for labels, part numbers, and measurements. Title is stamped or foil-pressed into the paper. Small technical annotations around the machine.
- Composition: the machine is the hero. Rebuild the layout from scratch as one visual system: {layout-specific instructions}. Generous parchment margin, dimension lines, numbered callouts, a small legend box, one restrained dual-ink overprint only if layout is dual-ink.
- Must include at least one real mechanical logic: {thesis}.
- Forbidden: cute cartoon steampunk, goggles-on-face cliché as the only subject, flying clockwork junk with no structure, cyberpunk neon, photoreal game screenshot look, modern sans logotype, lens flare, chrome 3D render, extra characters in the foreground.

Print language: halftone on metal parts, slight plate misregistration, letterpress bite, controlled grain.

Subject to generate:
{subject}

On-image text (render exactly):
- Stamped title: {title}
- Legend: {date / place / subtitle or none}
- Callouts: {2–6 short labels}
```

## 6. Generate

- One image. Aspect ratio **3:4**. If the tool has `aspect_ratio`, set `3:4`.
- Filename: `steampunk-{slug}.png`.
- No extra variations unless asked.

## 7. Quality gate (before showing)

Reject and regenerate **once** (same thesis, tighter prompt) if any of these fail:

- No readable mechanism (gears don't mesh, pipes go nowhere, piston has no cylinder)
- Palette broke (cyan, magenta, neon, icy blue, clean digital gradient)
- Cute / anime / goggles-as-subject
- Glossy CGI or game screenshot
- Title missing when the brief was an event poster
- Machine is a small ornament instead of the hero
- Portrait run still shows photoreal skin, a selfie filter, or goggles-as-costume

If the second image still fails the same check, show it anyway, name the miss, and ask whether to change thesis or layout.

## 8. Deliver

Show the image. Then two short sentences:

1. Thesis + layout you used
2. What text you put on the plate

Stop. Do not stack unsolicited alternates. If they want a change, iterate by editing **one** of: thesis, layout, or text — not all three.
