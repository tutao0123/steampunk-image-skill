# Prompt templates

Three templates, one per mode. Fill the braces, keep the rest verbatim, and attach the source image when the mode is Restyle or Avatar.

## RESTYLE (image attached)

```text
Restyle the attached image as a steampunk / Victorian industrial re-materialization. This is the same picture rebuilt in brass, not a new picture.

Locked (preserve exactly): composition, camera angle, framing, subject identity, {head count / pose / which object is where}. Aspect ratio {input ratio}.

Transformed (re-materialize everything visible):
- Materials: {concrete: skin → etched brass; concrete → riveted iron; fabric → oiled leather; wood → walnut; ...}. Every surface is rebuilt in metal or leather — **no fur, feathers, skin or fabric remains anywhere**; fur/feather/scale patterns are re-interpreted as engraved metal grain flowing in the same directions (never a mask or costume over the living original).
- Palette, five inks only: warm parchment beige #E4D2B0, antique brass #B08D4A, oxidized copper #6D7F57, iron rust red #8E3A2F, deep walnut brown #3B2418. No neon, no cyan, no magenta, no clean digital gradient.
- One mechanism, built into the subject and mechanically readable: {mechanism from machines.md, e.g. "the bicycle's chain becomes a real brass chain drive: chainring, chain, rear sprocket"}. Gears only where something rotates, pistons only where something reciprocates.
- Surface: rivets, patina, etched metal, soot in recesses, gentle steam haze, warm workshop light.
- Print language: Victorian engineering-plate illustration, letterpress grain, slight ink misregistration. Not glossy 3D CGI, not cyberpunk, not a photo filter.

Forbidden: changing the composition, adding or removing subjects, replacing the main subject, adding accessories not present in the photo (hats, goggles, armor), neon or cyan accents, chrome 3D render look, cute cartoon goggles as the only change, text (unless asked below).

On-image text: {usually none; if asked, 2–6 short labels in condensed stencil}
```

Faces add-on when the subject is a person and the ask is restyle: "Keep the face's structure and identity exactly; skin becomes etched brass, eyes become lenses or small gauges, a small clockwork is visible at the temple."

## AVATAR (portrait attached, 头像/profile picture asked)

```text
Restyle the attached portrait as a steampunk avatar. Same person, same face, rebuilt in brass — not a new character.

Locked (preserve exactly): head-and-shoulders framing and square 1:1 crop, face structure and identity, expression, head angle, hairstyle silhouette, eye direction. The face is the hero — clean, centered, unobstructed.

Transformed (re-materialize everything visible):
- Skin becomes polished and patinated brass plates with fine seams following the original face planes; brow, nose and cheeks keep their exact original shape.
- Eyes become warm amber glass lenses keeping the original gaze; brows become fine engraved lines.
- Hair/headwear: {re-cut in brass/copper, same silhouette; headwear → same shape in riveted leather or copper}
- Clothing at the shoulders becomes a riveted leather collar with a machined brass neck ring.
- One small mechanism, placed at the edge of the frame where an avatar circle-crop still shows it: {neck gear ring | jaw hinge | temple gear | ear-piece gauge | winding key at the collar}
- Background becomes plain deep walnut brown with a faint parchment glow behind the head, no objects.
- Palette, five inks only: warm parchment beige #E4D2B0, antique brass #B08D4A, oxidized copper #6D7F57, iron rust red #8E3A2F, deep walnut brown #3B2418. No neon, no cyan, no magenta.
- Surface: fine rivets, patina, soot in recesses. Must read clearly at 200 px avatar size: strong silhouette, nothing busy behind the head.
- Print language: Victorian engineering-plate rendering, letterpress grain. Not glossy 3D CGI, not cartoon, not photoreal human skin.

Forbidden: changing the face or expression, adding hats, goggles or objects not present, full body, busy background, neon or cyan, text, borders.

On-image text: none.
```

Before generating, crop the input to a head-and-shoulders square yourself — the crop controls framing, not the model. For a set (九宫格): one shared palette and background, vary only the mechanism per person.

## POSTER (text brief, new artwork)

```text
A complete editorial poster designed as a Victorian industrial engineering plate, steampunk mechanical design system.

Plate job: {layout id}, 3:4 portrait, museum print quality, letterpress on aged vellum.

Mechanical thesis (must be readable): {thesis}. Show real mechanical logic, not decorative gears.

Hero machine: {concrete machine, materials, what is in the center}.

Visual system:
- Limited ink palette only: antique brass, oxidized copper, iron rust red, warm parchment beige, deep walnut brown. No neon, no cyan, no magenta, no clean digital gradients.
- Paper: aged blueprint / vellum / letterpress stock, visible fiber, slight foxing, faint grid or compass marks.
- Texture: brushed brass, rivets, gear teeth, piston rods, pressure gauges, valve wheels, etched metal, letterpress impression, light soot and steam haze. Not glossy 3D CGI.
- Typography: engraved Victorian serif for the main title; condensed industrial sans or stencil for labels, part numbers, and measurements. Title is stamped or foil-pressed into the paper.
- Composition: the machine is the hero. {layout-specific instructions from layouts.md}. Generous parchment margin, dimension lines, numbered callouts, a small legend box, one restrained rust-red overprint only if layout is dual-ink.
- Forbidden: cute cartoon steampunk, goggles-on-face cliché as the only subject, flying clockwork junk with no structure, cyberpunk neon, photoreal game screenshot look, modern sans logotype, lens flare, chrome 3D render, extra characters in the foreground.

Print language: halftone on metal parts, slight plate misregistration, letterpress bite, controlled grain.

Subject to generate:
{subject}

On-image text (render exactly):
- Stamped title: {title}
- Legend: {date / place / subtitle or none}
- Callouts: {2–6 short labels}
```
