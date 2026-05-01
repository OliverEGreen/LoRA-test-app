"""Entry point for the HF Space.

Validates configuration, uploads LoRA weights to fal storage once at startup,
then constructs and launches the Gradio app.
"""

from inference import init_loras, require_fal_key
from ui import build_demo

require_fal_key()
LORA_URLS = init_loras()
demo = build_demo(LORA_URLS)

if __name__ == "__main__":
    demo.launch()
