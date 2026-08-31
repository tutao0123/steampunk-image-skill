# Steampunk Poster Skill

An agent skill that designs **Victorian industrial engineering-plate posters**, not generic "steampunk vibes".

Every run locks four decisions before it generates:

1. **Subject** — what the plate is about
2. **Mechanical thesis** — one real mechanism (gears, piston, boiler, pipes, gauges, chain)
3. **Layout** — hero assembly, cutaway, exploded, gauge-board, or dual-ink
4. **On-image text** — stamped title, legend, callouts

Then it builds one English prompt from a locked ink / paper / type / print system and renders **3:4**.

## Files

| File | What it is |
| --- | --- |
| [SKILL.md](./SKILL.md) | Runbook the agent follows |
| [style.md](./style.md) | Ink, paper, type, print language |
| [layouts.md](./layouts.md) | Five plate layouts |
| [machines.md](./machines.md) | Topic → machine mapping |
| [prompt.md](./prompt.md) | Final prompt template |
| [examples.md](./examples.md) | Worked briefs |

## Use

Put `SKILL.md` (and the companion files) in an agent skills folder, or tell the agent to follow this repo.

Give it a subject. For an event, also give title / date / place.

```
一张关于城市骑行的活动海报。
Title: BRASS VELOCITY
Date: 12 Sept 2026
Place: Riverside Foundry
```

## Visual lock (short)

- Inks: antique brass, oxidized copper, iron rust red, warm parchment beige, deep walnut brown
- Paper: aged vellum / letterpress, fiber, foxing, faint grid
- Type: engraved Victorian serif title; condensed stencil labels
- Forbidden: neon, cyan, magenta, cute cartoon steampunk, goggles-as-subject, unstructured flying clockwork, cyberpunk, photoreal game screenshots
