from PIL import ImageDraw, ImageTk, ImageFont

def generate(screenshot, desktop, selected=False):
    thumb = screenshot.resize((128, 72))

    font = ImageFont.truetype("/usr/share/fonts/gnu-free/FreeSans.otf", 14)

    draw = ImageDraw.Draw(thumb)
    text_width, text_height = draw.textsize(desktop, font)
    
    draw.rectangle([0, 72-text_height-4, text_width+8, 72], outline=None, fill=(51, 51, 51))
    draw.text((4, 72-text_height-2), desktop, (255, 255, 255), font=font)

    img = ImageTk.PhotoImage(thumb)

    return img