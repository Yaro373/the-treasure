from PIL import Image


def resize(filename):
    img = Image.open(filename)
    img = img.resize((32, 32))
    img.save("32x32_" + filename)


resize('character.png')