# Steampunk Image Skill

Turn images into steampunk — the same picture rebuilt in brass — or design Victorian engineering-plate posters from a text brief. Not generic steampunk vibes, not a goggle sticker.

## Two modes

| You give | You get |
| --- | --- |
| A photo + "把它变成蒸汽朋克" | **Restyle**: same composition, same subject — materials re-built as brass/copper/iron/leather, palette forced to five inks, one real mechanism built into the subject |
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

All agents on this machine:

```bash
npx skills add tutao0123/steampunk-image-skill -g --all
```

Then drop a photo ("把这张图改成蒸汽朋克风格") or give a brief ("给茶馆音乐会出一张蒸汽朋克海报").

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

## License

MIT. Companion public-domain / CC0 reference plates, if added later, keep their original licenses.
