def addtimestamp(name):

    from PIL import Image, ImageDraw, ImageFont

    time = 90

    image = Image.open(str(name) + '.png')

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('Arial.ttf', size=45)

    (x, y) = (100, 50)
    message = str(time)
    color = 'rgb(255, 0, 0)'
    draw.text((x, y), message, fill=color, font=font)
    image.save(str(name) + '.png')
