# Steampunk Poster Skill

Victorian industrial engineering-plate posters. Not generic steampunk vibes.

Install with the open [skills CLI](https://github.com/vercel-labs/skills) — this is the npm-style install for agent skills. GitHub is the registry; you do not `npm install` this repo.

```bash
npx skills add tutao0123/steampunk-image-skill
```

Cursor only:

```bash
npx skills add tutao0123/steampunk-image-skill --agent cursor
```

All agents on this machine:

```bash
npx skills add tutao0123/steampunk-image-skill --all -g
```

Then ask the agent for a steampunk poster, or drop a city / bus / selfie / group photo.

## What it does

Every run locks four decisions before generating:

1. **Subject**
2. **Mechanical thesis** — one real mechanism (gears, piston, boiler, pipes, gauges, chain)
3. **Layout** — hero, cutaway, exploded, gauge-board, dual-ink, portrait-automaton, group-automaton
4. **On-image text**

Photos are transcribed, not filtered: vehicles become brass machines, people become automata.

Example brief:

```
一张关于城市骑行的活动海报。
Title: BRASS VELOCITY
Date: 12 Sept 2026
Place: Riverside Foundry
```

## Visual lock

- Inks: antique brass, oxidized copper, iron rust red, warm parchment beige, deep walnut brown
- Paper: aged vellum / letterpress
- Type: engraved Victorian serif title; condensed stencil labels
- Forbidden: neon, cyan, magenta, cute cartoon steampunk, goggles-as-subject, cyberpunk, photoreal game screenshots

## Files

| File | What it is |
| --- | --- |
| [SKILL.md](./SKILL.md) | Runbook (`npx skills add` finds this at repo root) |
| [style.md](./style.md) | Ink, paper, type, print language |
| [layouts.md](./layouts.md) | Plate layouts |
| [machines.md](./machines.md) | Topic → machine mapping |
| [prompt.md](./prompt.md) | Prompt template |
| [examples.md](./examples.md) | Worked briefs |

## License

MIT. Companion public-domain / CC0 reference plates, if added later, keep their original licenses.
