from PIL import Image


def resize(filename):
    img = Image.open(filename)
    img = img.resize((64, 64))
    img.save("64x64_" + filename)


resize('opened_chest.png')