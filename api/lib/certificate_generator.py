from PIL import Image, ImageDraw, ImageFont

def certificate_gen(name : str, hours : int):
    base = Image.open("api/static/template_certificado.jpg")
    draw = ImageDraw.Draw(base)
    fontName = ImageFont.truetype("arial.ttf", 60)
    fontHour = ImageFont.truetype("arial.ttf", 45)

    draw.text((500, 300), name, font=fontName, fill="black")
    draw.text((500, 400), f"{hours}", font=fontHour, fill="black")

    base.save(f"api/static/certificates_tmp/certificado_{name}.pdf", "PDF")