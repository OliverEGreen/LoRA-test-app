---
title: Flux Style LoRAs
emoji: 🎨
colorFrom: yellow
colorTo: red
sdk: gradio
app_file: app.py
pinned: false
license: mit
short_description: Flux LoRAs — Kodachrome buildings & Akira cityscapes
---

# Flux Style LoRAs

Two custom [Flux.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) LoRAs in one app:

- **Kodachrome (architecture)** — vintage Kodachrome photographs of buildings: postwar ranch houses, Federal rowhouses, mid-century shopping plazas, Art Deco hotels, brutalist civic buildings.
- **Akira (anime cityscape)** — hand-painted cel-animation backgrounds in the style of Akira: dense Neo-Tokyo cityscapes, gouache rendering, restrained earth-tone palette.

This Space runs on free CPU and proxies inference through [fal.ai](https://fal.ai)'s Flux LoRA endpoint. Each generation costs the Space owner roughly $0.03–0.05.

## Trigger words

- `kodachrome` — added automatically when "Kodachrome" is selected.
- `akira` — added automatically when "Akira" is selected.

## Usage tips

- Pick the style first, then describe the scene.
- LoRA scale around 0.8–1.1 is the sweet spot. Drop lower if the style overpowers the subject; raise if the look is too subtle.
- 28 steps and guidance scale 3.5 are good defaults for Flux.1-dev.

## Setup (for forks of this Space)

1. Add a `FAL_KEY` Space secret with your fal.ai API key.
2. Upload `kodachrome-architecture-v1.safetensors` and `akira-v1.safetensors` to the Space root.
3. The app will upload both LoRAs to fal storage on first launch.

## Project layout

```
space/
├── app.py            # Entry point: bootstraps LoRAs, builds the demo, launches.
├── config.py         # LoRA registry, defaults, constants.
├── inference.py      # Pure logic: prompt formatting + fal.ai API calls.
├── ui.py             # Gradio Blocks layout.
├── examples.py       # Example prompts for the UI.
├── tests/            # pytest smoke tests for prompt formatting.
├── requirements.txt  # Pinned runtime deps (used by the Space build).
└── pyproject.toml    # ruff + pytest config and dev deps.
```

Add a new style by appending to `LORAS` in `config.py` and uploading the corresponding `.safetensors` to the Space root.

## Local development

```bash
cd space
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install ruff pytest

ruff check .            # lint
ruff format .           # format
pytest                  # run smoke tests

export FAL_KEY=...      # required to run app.py end-to-end
python app.py
```

## License

The LoRA weights are released under MIT. The base Flux.1-dev model is governed by [Black Forest Labs' non-commercial license](https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md).
