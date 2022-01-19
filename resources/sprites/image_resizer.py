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


resize("Floor2.png", 64, "floor_2.png")

dark_image("64x64_floor_2.png", 1)
dark_image("64x64_floor_2.png", 2)
dark_image("64x64_floor_2.png", 3)
dark_image("64x64_floor_2.png", 4)
dark_image("64x64_floor_2.png", 5)
dark_image("64x64_floor_2.png", 6)
dark_image("64x64_floor_2.png", 7)
dark_image("64x64_floor_2.png", 8)

# for i in range(1, 11):
#     resize("Shoot_Animation-" + str(i) + ".png", 128, "shoot_animation_" + str(i) + ".png")
#
# merge("128x128_shoot_animation_1.png",
#       "128x128_shoot_animation_2.png",
#       "128x128_shoot_animation_3.png",
#       "128x128_shoot_animation_4.png",
#       "128x128_shoot_animation_5.png",
#       "128x128_shoot_animation_6.png",
#       "128x128_shoot_animation_7.png",
#       "128x128_shoot_animation_8.png",
#       "128x128_shoot_animation_9.png",
#       "128x128_shoot_animation_10.png",
#       size=128, outfilename="128_128_shoot_animation.png"
# #       )
#
#
resize("chest.png", 400, "prize_1.png")
resize("IMG_3977(1).PNG", 400, "prize_2.png")
resize("IMG_3977.PNG", 400, "prize_3.png")
resize("IMG_3979.PNG", 400, "prize_4.png")
resize("Default ghost.png", 400, "prize_5.png")
resize("Statue 1.png", 400, "prize_6.png")
resize("Statue 2.png", 400, "prize_7.png")
resize("Statue 3.png", 400, "prize_8.png")
resize("Statue 4.png", 400, "prize_9.png")