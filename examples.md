# Worked examples

Mode-tagged. Restyle examples show the fidelity contract written out before prompting.

## Restyle 1. 自己的自行车照片

```text
Locked: low-angle side view, bike fills frame diagonally, wall and shadow behind, 4:3 landscape.
Transformed: steel frame → riveted brass with walnut grips; tires → iron-shod wooden wheels.
Mechanism: the existing chain becomes a real brass chain drive — chainring, chain, rear sprocket, all meshing.
```

The bike is still *that* bike, same angle, same wall. Not a poster, not a different bicycle.

## Restyle 2. 自拍(变风格,不换人)

```text
Locked: face structure, identity, head tilt, glasses, hair shape, 1:1.
Transformed: skin → etched brass plate with hairline engraving; glasses → brass ocular gauges; jacket → oiled leather with riveted collar; background room → warm workshop haze.
Mechanism: small clockwork visible at the temple and neck hinge.
```

Face addon from `prompt.md` goes in verbatim. Output is not a robot, not a stranger — the same face in another material.

## Restyle 3. 城市夜景(霓虹 → 五墨)

```text
Locked: skyline profile, river, bridge position, building heights, 16:9.
Transformed: neon/cyan palette → five inks; glass towers → riveted copper and iron; window grids → etched patterns; sky → soot-and-steam haze with warm workshop glow from below.
Mechanism: the bridge becomes a bascule bridge with exposed gear train and boiler house.
```

Night photo cyan is the #1 palette killer — kill it in the prompt, not in a second pass.

## Restyle 4. 群像 → automaton rebuild (asked for robots)

```text
Ask: 把我们三个变成蒸汽朋克机器人 → full rebuild allowed.
Locked: head count (3), relative heights, poses, clothing volumes.
Transformed: each person → one labeled brass automaton (FIG. A/B/C), shared boiler behind feeding all three, skin fully metal.
Framing: 3:4 engineering plate with callouts (the one rebuild case that becomes a poster).
```

## Poster 1. City cycling event

```text
Subject: 城市骑行活动海报
Thesis: chain drive on a brass safety bicycle because the event is about riding
Layout: hero-assembly
Text: title="BRASS VELOCITY" / date="12 SEPT 2026" / place="RIVERSIDE FOUNDRY" / labels=CHAIN RING, REAR SPROCKET, CALIPER
```

One bicycle as an engineering plate, chain clearly meshing. Not a peloton, not a character.

## Poster 2. Tea house evening concert

```text
Subject: 茶馆夜场音乐会
Thesis: steam calliope, valves feeding ranked pipes
Layout: dual-ink
Text: title="NIGHT STEAM RECITAL" / date="SAT 20:00" / place="LOTUS TEA HOUSE" / labels=STEAM CHEST, RANK A, VALVE
```

Rust-red overprint: a single musical staff or steam route, slightly misregistered.

## Poster 3. Lab project

```text
Subject: nanoDiffusionLab 项目海报
Thesis: difference engine gear train as a "diffusion" mill — input drum, masked teeth, output drum
Layout: cutaway
Text: title="MASKED MILL" / legend="nanoDiffusionLab" / labels=INPUT DRUM, MASK GATE, OUTPUT DRUM
```

No neural-net diagram, no robot.

## Real runs (in this repo)

Four CC0/public-domain inputs restyled end-to-end with `scripts/restyle.py` — input, exact prompt, and output in [`examples/`](./examples/README.md):

- Pet photo → clockwork automaton cat (`examples/cat/`)
- 1783 Ducreux portrait → spring-powered automaton (`examples/portrait/`)
- Street musician → steam calliope-guitar (`examples/street/`)
- Latte pour → vertical-boiler cup (`examples/coffee/`)
