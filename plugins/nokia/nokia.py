from io import BytesIO
from os.path import dirname
from collections import deque
from PIL import Image, ImageFont, ImageDraw

font_size = 70
line_gap = 20
body_pos = (205, 340)
subtitle_pos = (790, 320)
body_color = (0, 0, 0, 255)
subtitle_color = (129, 212, 250, 255)
line_rotate = -9.8
max_line_width = 680
max_content_height = 450
font = ImageFont.truetype(dirname(__file__) + "/assets/font.ttf", font_size)
model = Image.open(dirname(__file__) + "/assets/img.png")


def draw_subtitle(im: Image, text: str):
    width, height = font.getsize(text)
    image2 = Image.new("RGBA", (width, height))
    draw2 = ImageDraw.Draw(image2)
    draw2.text((0, 0), text=text, font=font, fill=subtitle_color)
    image2 = image2.rotate(line_rotate, expand=1)

    px, py = subtitle_pos
    sx, sy = image2.size
    im.paste(image2, (px, py, px + sx, py + sy), image2)


def generate_image(text: str) -> BytesIO:
    origin_im = model.copy()
    text = text[:900]
    length = len(text)
    width, height = font.getsize(text)
    current_width = 0
    lines = []
    line = ""
    q = deque(text)

    while q:
        word = q.popleft()
        width, _ = font.getsize(word)
        current_width += width
        if current_width >= max_line_width:
            q.appendleft(word)
            lines.append(line)
            current_width = 0
            line = ""
        else:
            line += word
    
    lines.append(line)
    image2 = Image.new("RGBA", (max_line_width, max_content_height))
    draw2 = ImageDraw.Draw(image2)
    for i, line in enumerate(lines):
        y = i * (height + line_gap)
        if y > max_content_height:
            break
        draw2.text((0, y), text=line, font=font, fill=body_color)
    image2 = image2.rotate(line_rotate, expand=1)

    px, py = body_pos
    sx, sy = image2.size
    origin_im.paste(image2, (px, py, px + sx, py + sy), image2)
    draw_subtitle(origin_im, f"{length}/900")

    buf = BytesIO()
    origin_im.save(buf, format="PNG")
    return buf
