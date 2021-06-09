from PIL import Image


def add_watermark(pil_img, watermark_img, position=(0, 0)):
    width, height = pil_img.size

    w2h = watermark_img.size[0] / watermark_img.size[1]
    wm_height = height // 3
    wm_width = int(w2h * wm_height)

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(pil_img, (0, 0))

    watermark_img = watermark_img.resize((wm_width, wm_height))
    transparent.paste(watermark_img, position, mask=watermark_img)
    return transparent.convert('RGB')


def gen_thumbnail_with_watermark(input_thumbnail_path, watermark_path, output_thumbnail_path):
    add_watermark(Image.open(input_thumbnail_path),
                  Image.open(watermark_path)).save(output_thumbnail_path)


if __name__ == "__main__":
    gen_thumbnail_with_watermark(fr'C:\Users\79161\PycharmProjects\PyCutBot\useful_scripts\thumbnail_nf.png',
                                 fr'C:\Users\79161\PycharmProjects\PyCutBot\src\img\watermark.png',
                                 fr'C:\Users\79161\PycharmProjects\PyCutBot\useful_scripts\thumbnail_nf2_MARKED.png')
