"""Pure inference logic: prompt formatting + fal.ai API calls.

This module deliberately does not import gradio, so the prompt-formatting
logic is unit-testable in isolation and the fal interaction can be reused
from any UI layer.
"""

from __future__ import annotations

import os
from io import BytesIO

import fal_client
import requests
from PIL import Image

from config import FAL_ENDPOINT, LORAS


def _format_prompt(prompt: str, trigger: str) -> str:
    """Prepend the trigger word to the prompt unless it's already there.

    Raises:
        ValueError: if the prompt is empty or whitespace-only.
    """
    cleaned = prompt.strip()
    if not cleaned:
        raise ValueError("Prompt is empty.")
    if cleaned.lower().startswith(trigger.lower()):
        return cleaned
    return f"{trigger}, {cleaned}"


def require_fal_key() -> None:
    """Raise RuntimeError if FAL_KEY is missing from the environment."""
    if not os.environ.get("FAL_KEY"):
        raise RuntimeError(
            "FAL_KEY environment variable is not set. "
            "Add your fal.ai API key as a Space secret named FAL_KEY."
        )


def init_loras() -> dict[str, str]:
    """Upload every configured LoRA to fal.ai storage.

    Returns:
        Mapping of style name → fal storage URL.
    """
    urls: dict[str, str] = {}
    for name, cfg in LORAS.items():
        print(f"Uploading {name} → fal.ai storage...")
        urls[name] = fal_client.upload_file(cfg["path"])
        print(f"  → {urls[name]}")
    return urls


def generate(
    *,
    prompt: str,
    style: str,
    lora_url: str,
    seed: int | None,
    image_size: str,
    guidance_scale: float,
    num_inference_steps: int,
    lora_scale: float,
) -> tuple[Image.Image, int]:
    """Generate one image via fal.ai's Flux LoRA endpoint.

    Args:
        prompt: User-supplied scene description.
        style: LoRA name (key into ``LORAS``).
        lora_url: fal storage URL for the chosen LoRA's weights.
        seed: Explicit seed, or ``None`` to let fal pick randomly.
        image_size: One of the size presets supported by fal-ai/flux-lora.
        guidance_scale: Flux CFG scale (typical: 3.5).
        num_inference_steps: Diffusion steps (typical: 28).
        lora_scale: Strength applied to the LoRA at inference (0–1.5).

    Returns:
        A tuple of (PIL image, seed actually used by fal).
    """
    trigger = LORAS[style]["trigger"]
    full_prompt = _format_prompt(prompt, trigger)

    arguments: dict = {
        "prompt": full_prompt,
        "image_size": image_size,
        "num_inference_steps": int(num_inference_steps),
        "guidance_scale": float(guidance_scale),
        "loras": [{"path": lora_url, "scale": float(lora_scale)}],
        "num_images": 1,
        "enable_safety_checker": False,
    }
    if seed is not None:
        arguments["seed"] = int(seed)

    result = fal_client.subscribe(
        FAL_ENDPOINT,
        arguments=arguments,
        with_logs=False,
    )

    image_url = result["images"][0]["url"]
    used_seed = int(result.get("seed", seed if seed is not None else 0))

    response = requests.get(image_url, timeout=30)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    return image, used_seed
