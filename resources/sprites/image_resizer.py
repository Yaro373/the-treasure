from PIL import Image


def resize(filename, size, res_name=None):
    if res_name is None:
        res_name = filename
    img = Image.open(filename)
    img = img.resize((size, size))
    img.save(f"{size}x{size}_" + res_name)


def merge(*filenames, size=128, outfilename="out.png"):
    img = Image.new("RGBA", (len(filenames) * size, size))
    img2 = Image.open(filenames[0])
    img.paste(img2, (0, 0, img2.size[0], img2.size[1]))
    for i in range(len(filenames)):
        img2 = Image.open(filenames[i])
        img.paste(Image.open(filenames[i]), (size * i, 0, size * i + img2.size[0], img2.size[1]))
    img.save(outfilename)


def dark_image(filename, d):
    img = Image.open(filename)
    pixels = img.load()
    x, y = img.size
    for i in range(x):
        for j in range(y):
            r, g, b, a = pixels[i, j]
            if a == 0:
                continue

            sr = r // 8
            sg = g // 8
            sb = b // 8

            r -= sr * d
            g -= sg * d
            b -= sb * d

            r = max(r, 0)
            g = max(g, 0)
            b = max(b, 0)
            pixels[i, j] = r, g, b

    img.save(filename[:5] + f'_{d}' + filename[5:])

resize("Unbreakable Wall.png", 64, "unbreakable_wall.png")