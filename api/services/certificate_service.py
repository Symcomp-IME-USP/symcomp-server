from PIL import Image, ImageDraw, ImageFont

def certificate_gen(name : str, hours : int):
    base = Image.open("template_certificado.png")
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype("arial.ttf", 60)

    draw.text((500, 300), name, font=font, fill="black")
    draw.text((500, 400), f"{hours} horas", font=font, fill="black")

    base.save(f"certificado_{name}.pdf", "PDF")