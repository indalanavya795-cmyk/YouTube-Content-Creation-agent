from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap


WIDTH = 1280
HEIGHT = 720


def _font(size, bold=False):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]

    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def create_thumbnail(topic, headline, output_path="outputs/thumbnail.png"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    image = Image.new("RGB", (WIDTH, HEIGHT), (20, 20, 25))
    draw = ImageDraw.Draw(image)

    # Background
    draw.rectangle(
        [0, 0, WIDTH, HEIGHT],
        fill=(20, 20, 25),
    )

    # Accent blocks
    draw.rectangle(
        [0, 0, 35, HEIGHT],
        fill=(255, 80, 60),
    )

    draw.rectangle(
        [WIDTH - 35, 0, WIDTH, HEIGHT],
        fill=(255, 80, 60),
    )

    # Topic
    topic_font = _font(42, bold=True)
    draw.text(
        (80, 70),
        str(topic).upper()[:45],
        font=topic_font,
        fill="white",
    )

    # Main headline
    headline_font = _font(82, bold=True)

    lines = textwrap.wrap(
        str(headline).upper(),
        width=20,
    )[:4]

    y = 180

    for line in lines:
        draw.text(
            (80, y),
            line,
            font=headline_font,
            fill="white",
            stroke_width=3,
            stroke_fill="black",
        )
        y += 100

    # Bottom label
    small_font = _font(30, bold=True)

    draw.rounded_rectangle(
        [80, 600, 390, 660],
        radius=18,
        fill=(255, 80, 60),
    )

    draw.text(
        (105, 613),
        "WATCH NOW",
        font=small_font,
        fill="white",
    )

    image.save(output_path, "PNG")

    return output_path
