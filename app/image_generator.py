import torch
from diffusers import StableDiffusionPipeline


MODEL_ID = "stable-diffusion-v1-5/stable-diffusion-v1-5"

_device = "mps"
_pipe = None


def load_model():
    global _pipe

    if _pipe is None:
        print("Loading Stable Diffusion model...")

        _pipe = StableDiffusionPipeline.from_pretrained(
            MODEL_ID,
            dtype=torch.float16
        )

        _pipe = _pipe.to(_device)

        print("Stable Diffusion model loaded!")

    return _pipe


def generate_thumbnail_image(prompt, output_path="outputs/thumbnail.png"):

    pipe = load_model()

    print("Generating YouTube thumbnail...")

    image = pipe(
        prompt,
        num_inference_steps=20,
        guidance_scale=7.5,
        width=512,
        height=512
    ).images[0]

    image.save(output_path)

    print(f"Thumbnail saved to: {output_path}")

    return output_path