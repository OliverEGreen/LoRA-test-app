"""Gradio UI layer.

Adapts between Gradio components and the pure ``inference`` module:
translates the (seed, randomize) checkbox into the inference layer's
optional-int seed contract, and converts ``ValueError`` raised by the
inference layer into ``gr.Error`` so the user sees a friendly toast.
"""

from __future__ import annotations

import gradio as gr

from config import (
    DEFAULT_GUIDANCE_SCALE,
    DEFAULT_IMAGE_SIZE,
    DEFAULT_LORA_SCALE,
    DEFAULT_NUM_INFERENCE_STEPS,
    DEFAULT_STYLE,
    IMAGE_SIZES,
    LORAS,
    MAX_SEED,
)
from examples import EXAMPLES
from inference import generate


def build_demo(lora_urls: dict[str, str]) -> gr.Blocks:
    """Construct the Gradio Blocks app, bound to the given LoRA URL map."""

    def on_generate(
        prompt: str,
        style: str,
        seed: int,
        randomize_seed: bool,
        image_size: str,
        guidance_scale: float,
        num_inference_steps: int,
        lora_scale: float,
    ) -> tuple:
        try:
            image, used_seed = generate(
                prompt=prompt,
                style=style,
                lora_url=lora_urls[style],
                seed=None if randomize_seed else int(seed),
                image_size=image_size,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
                lora_scale=lora_scale,
            )
        except ValueError as exc:
            raise gr.Error(str(exc)) from exc
        return image, used_seed

    with gr.Blocks(title="Flux Style LoRAs") as demo:
        gr.Markdown(
            """
            # Flux Style LoRAs
            Two custom Flux.1-dev LoRAs: vintage Kodachrome architectural photography,
            and Akira-style hand-painted anime cityscapes. Pick a style — the trigger
            word is added automatically.
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                style = gr.Radio(
                    choices=list(LORAS.keys()),
                    value=DEFAULT_STYLE,
                    label="Style",
                )
                prompt = gr.Textbox(
                    label="Scene description",
                    placeholder=(
                        "e.g. Victorian terraced houses on a steep San Francisco "
                        "street, autumn afternoon"
                    ),
                    lines=3,
                )
                run_btn = gr.Button("Generate", variant="primary")

                with gr.Accordion("Advanced", open=False):
                    image_size = gr.Dropdown(
                        choices=IMAGE_SIZES,
                        value=DEFAULT_IMAGE_SIZE,
                        label="Image size",
                    )
                    with gr.Row():
                        seed = gr.Slider(0, MAX_SEED, value=0, step=1, label="Seed")
                        randomize_seed = gr.Checkbox(value=True, label="Randomize")
                    with gr.Row():
                        guidance_scale = gr.Slider(
                            1.0,
                            10.0,
                            value=DEFAULT_GUIDANCE_SCALE,
                            step=0.1,
                            label="Guidance scale",
                        )
                        num_inference_steps = gr.Slider(
                            10,
                            50,
                            value=DEFAULT_NUM_INFERENCE_STEPS,
                            step=1,
                            label="Steps",
                        )
                    lora_scale = gr.Slider(
                        0.0,
                        1.5,
                        value=DEFAULT_LORA_SCALE,
                        step=0.05,
                        label="LoRA scale",
                    )

            with gr.Column(scale=1):
                output_image = gr.Image(label="Output", format="png")
                seed_output = gr.Number(label="Used seed", interactive=False, precision=0)

        gr.Examples(examples=EXAMPLES, inputs=[style, prompt])

        run_btn.click(
            fn=on_generate,
            inputs=[
                prompt,
                style,
                seed,
                randomize_seed,
                image_size,
                guidance_scale,
                num_inference_steps,
                lora_scale,
            ],
            outputs=[output_image, seed_output],
        )

    return demo
