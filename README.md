# LoRA Test App

End-to-end pipeline for training and serving custom Flux.1-dev style LoRAs. Hosts two of them in one Gradio app:

- **Kodachrome (architecture)** — vintage Kodachrome photographs of buildings (postwar ranch houses, Federal rowhouses, mid-century shopping plazas, Art Deco hotels, brutalist civic buildings).
- **Akira (anime cityscape)** — hand-painted cel-animation backgrounds in the style of Akira (dense Neo-Tokyo cityscapes, gouache rendering, restrained earth-tone palette).

> _Replace this with a link to the deployed Space:_  
> [![Open in Spaces](https://img.shields.io/badge/%F0%9F%A4%97-Open%20in%20Spaces-blue)](https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME)

## Pipeline

1. **Curate** ~30 reference images per style.
2. **Caption** each image with a focused, content-only description (under 70 words) and prepend a trigger word (`kodachrome` or `akira`).
3. **Train** a Flux.1-dev LoRA via [fal.ai's Fast LoRA Trainer](https://fal.ai/models/fal-ai/flux-lora-fast-training) (~$2, ~5 min per run).
4. **Deploy** a Gradio Space that selects between the LoRAs and proxies inference back to fal.ai.

## Repository layout

```
.
├── README.md             — this file
├── LICENSE               — MIT
├── Training Data/        — 29 captioned images for the Kodachrome LoRA (.jpg + .txt pairs)
└── space/                — the deployable Gradio app
    ├── app.py            — entry point
    ├── config.py         — LoRA registry + defaults
    ├── inference.py      — pure logic (fal.ai calls, prompt formatting)
    ├── ui.py             — Gradio Blocks layout
    ├── examples.py       — example prompts
    ├── tests/            — pytest smoke tests
    ├── requirements.txt  — runtime deps (used by the Space build)
    ├── pyproject.toml    — ruff + pytest config
    └── README.md         — Space-side README (rendered on the HF Space page)
```

The Akira training data and `.safetensors` weights live in sister directories on disk but aren't checked in — weights are distributed via the HF Space.

## Try it

Visit the [HuggingFace Space](https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME), pick a style, type a scene, generate.

## Local development

See [`space/README.md`](space/README.md) for the full local dev workflow. Quick version:

```bash
cd space
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt ruff pytest

ruff check . && ruff format --check .
pytest

export FAL_KEY=...   # required to run end-to-end
python app.py
```

## License

MIT for the code and LoRA weights in this repository.

The base Flux.1-dev model is governed by [Black Forest Labs' non-commercial license](https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md), so commercial deployment of the app would require a separate commercial license from BFL.
