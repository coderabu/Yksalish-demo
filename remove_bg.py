"""
Ustozlar rasmidan fonni olib, kulrang studio fon bilan almashtirish.
Ishlatish: python remove_bg.py
"""
from rembg import remove
from PIL import Image
import io
import os

# Barcha ustoz rasmlari
TEACHER_IMAGES = [
    "ustoz1.jpg",
    "ustoz2.jpg",
    "ustoz445.jpg",
    "ustoz4.jpg",
    "ustoz6.jpg",
    "ustoz98.jpg",
    "ustoz44.jpg",
    "ustoz71.jpg",
    "ustoz77.jpg",
    "ustoz5.jpg",
    "ustoz90.jpg",
    "ustoz7.jpg",
    "ustoz18.jpg",
    "ustoz19.jpg",
    "ustoz11.jpg",
    "ustoz13.jpg",
    "ustoz14.jpg",
    "ustoz15.jpg",
    "ustoz16.jpg",
    "ustoz17.png",
    "ustoz20.jpg",
    "ustoz21.jpg",
    "ustoz22.jpg",
    "ustoz23.jpg",
    "ustoz25.jpg",
    "ustoz1111.jpg",
    "ustoz222.png",
]

# Studio kulrang fon (gradient effekti uchun Pillow)
STUDIO_BG_TOP    = (210, 214, 220)   # ochroq kulrang - yuqori
STUDIO_BG_BOTTOM = (155, 161, 172)   # to'qroq kulrang - pastki

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def make_gray_bg(width: int, height: int) -> Image.Image:
    """Yuqoridan pastga gradientli kulrang fon yaratadi."""
    bg = Image.new("RGB", (width, height))
    for y in range(height):
        t = y / height
        r = int(STUDIO_BG_TOP[0] + (STUDIO_BG_BOTTOM[0] - STUDIO_BG_TOP[0]) * t)
        g = int(STUDIO_BG_TOP[1] + (STUDIO_BG_BOTTOM[1] - STUDIO_BG_TOP[1]) * t)
        b = int(STUDIO_BG_TOP[2] + (STUDIO_BG_BOTTOM[2] - STUDIO_BG_TOP[2]) * t)
        for x in range(width):
            bg.putpixel((x, y), (r, g, b))
    return bg

def process(filename: str):
    src_path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(src_path):
        print(f"  [skip] topilmadi: {filename}")
        return

    print(f"  Qayta ishlayapti: {filename} ...", end="", flush=True)

    with open(src_path, "rb") as f:
        img_bytes = f.read()

    # Fonni olib tashlash
    no_bg_bytes = remove(img_bytes)
    person = Image.open(io.BytesIO(no_bg_bytes)).convert("RGBA")

    # Asl o'lchamda kulrang fon
    bg = make_gray_bg(person.width, person.height).convert("RGBA")

    # Odamni fonning ustiga qo'yish
    combined = Image.alpha_composite(bg, person).convert("RGB")

    # Ustiga yozib saqlash (JPG)
    out_name = os.path.splitext(filename)[0] + ".jpg"
    out_path = os.path.join(BASE_DIR, out_name)
    combined.save(out_path, "JPEG", quality=92)
    print(f" tayyor → {out_name}")

if __name__ == "__main__":
    print("=== Ustoz rasmlari fon olib tashlash ===")
    for img in TEACHER_IMAGES:
        process(img)
    print("\nBarcha rasmlar tayyor!")
