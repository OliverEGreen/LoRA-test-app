"""Static configuration for the Flux LoRA app.

Add a new LoRA by appending an entry to ``LORAS``. Each .safetensors file
must be uploaded to the Space root alongside the app code.
"""

LORAS: dict[str, dict[str, str]] = {
    "Kodachrome (architecture)": {
        "path": "./kodachrome-architecture-v1.safetensors",
        "trigger": "kodachrome",
    },
    "Akira (anime cityscape)": {
        "path": "./akira-v1.safetensors",
        "trigger": "akira",
    },
}

DEFAULT_STYLE = "Kodachrome (architecture)"

IMAGE_SIZES: list[str] = [
    "square_hd",
    "square",
    "portrait_4_3",
    "portrait_16_9",
    "landscape_4_3",
    "landscape_16_9",
]

DEFAULT_IMAGE_SIZE = "landscape_4_3"
DEFAULT_GUIDANCE_SCALE = 3.5
DEFAULT_NUM_INFERENCE_STEPS = 28
DEFAULT_LORA_SCALE = 1.0

# int32 max — fal.ai's accepted seed range.
MAX_SEED = 2**31 - 1

FAL_ENDPOINT = "fal-ai/flux-lora"
