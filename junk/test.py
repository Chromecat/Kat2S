
from PIL import Image, ImageDraw, ImageFont

image = Image.open('CivilDefence.png')

draw = ImageDraw.Draw(image)

font = ImageFont.truetype('Arial.ttf', size=45)

(x, y) = (100, 50)
message = "TEST"
color = 'rgb(255, 0, 0)'
draw.text((x, y), message, fill=color, font=font)
image.save('test.png')
