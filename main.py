import os
import argparse
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from dotenv import load_dotenv

load_dotenv()
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

MODEL_ID = "CompVis/stable-diffusion-v1-4"
DEVICE = "cuda"

RESULTS = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS, exist_ok=True)

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID, revision="fp16", torch_dtype=torch.float16, use_auth_token=AUTH_TOKEN
)
pipe.to(DEVICE)

def generate_image(prompt: str, output_path: str = None):
    if output_path is None:
        i = len([f for f in os.listdir(RESULTS) if f.endswith(".png")])
        output_path = os.path.join(RESULTS, f"image_{i + 1}.png")
    
    with autocast(DEVICE):
        image = pipe(prompt, guidance_scale=8.5)["sample"][0]
    image.save(output_path)
    print(f"Image saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an image using Stable Diffusion")
    parser.add_argument("prompt", type=str, help="Text prompt for image generation")
    parser.add_argument("--output", type=str, default=None, help="Output image path")
    args = parser.parse_args()
    
    generate_image(args.prompt, args.output)
