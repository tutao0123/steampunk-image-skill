# Style bible

Locked. Do not add inks, fonts, or finishes that are not here.

## Ink

Five inks, used as a limited letterpress / intaglio set. Think plates and pigments, not a digital palette.

| Name | Role | Approx. |
| --- | --- | --- |
| Warm parchment beige | Ground, paper | `#E4D2B0` |
| Antique brass | Metal, title foil, highlights | `#B08D4A` |
| Oxidized copper | Pipes, patina, secondary metal | `#6D7F57` |
| Iron rust red | Dual-ink overprint, rust, seals | `#8E3A2F` |
| Deep walnut brown | Line work, type, shadows | `#3B2418` |

Rules:

- Paper stays beige. Never fill the background with black or teal.
- Brass and copper are metals, not gold-foil luxury branding.
- Rust red is an overprint or oxidation, never a flat modern accent color.
- No sixth ink. No white except paper show-through. No black richer than walnut.

## Paper

Aged blueprint / vellum / letterpress stock.

Must read:

- Visible rag fiber
- Slight foxing (small rust spots, sparse)
- Faint compass rose or letterpress grid in the margin
- Impression bite around the title and heavy rules

Not: stained coffee-shop collage, burnt edges, dripping wax, leather-bound photo.

## Type

Two families only.

1. **Title** — engraved Victorian serif (think De Vinne / engraved Caslon). Stamped or foil-pressed into the paper. Tracking slightly tight. 2–5 words.
2. **Labels / legend / measurements** — condensed industrial sans or stencil. All-caps English for part names. Small.

No script, no blackletter, no techno mono, no modern geometric logotype.

## Texture & print

On metal: brushed brass, rivets, gear teeth, etched plates, halftone, soot in recesses.

On paper: letterpress bite, slight plate misregistration (one ink offset 0.5–1 mm), controlled grain.

Not: glossy 3D CGI, subsurface chrome, ray-traced steam, octane render, photoreal game engine.

## Camera / plate

- Flat or near-flat editorial plate, not a cinematic 3/4 hero render
- Museum print, 3:4 portrait
- Machine occupies roughly the middle 60–70% of the height
- Margin is parchment, not empty black

## Restyle exceptions

In restyle mode the input photo overrides part of this bible:

- **Aspect** follows the input image, not 3:4. No parchment margin is forced.
- **Paper / plate rules** (vellum ground, margin, plate framing) apply only when the user asked for a poster-style plate output. A plain restyle keeps the photo's scene, re-materialized.
- **Palette, ink, type, and texture rules** always apply: five inks, no neon, letterpress/print language over CGI. Killing cyan/neon at the source matters most in restyle mode, because night photos and screens leak it.
- Faces: identity is locked even though skin is re-materialized — see SKILL.md faces rule.
