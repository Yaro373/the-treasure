from PIL import Image


def resize(filename, size):
    img = Image.open(filename)
    img = img.resize((size, size))
    img.save(f"{size}x{size}_" + filename)


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


dark_image('64x64_opened_chest.png', 8)
