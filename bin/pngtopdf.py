from PIL import Image

print("Test")

def combine_png_to_pdf(png_files, output_pdf):
    # Open the first image
    img1 = Image.open(png_files[0])
    # Get the dimensions of the first image
    width, height = img1.size
    # Create a new image with the same dimensions as the first image
    combined_img = Image.new('RGB', (width, height * len(png_files)))
    # Paste each PNG image into the combined image
    for i, png_file in enumerate(png_files):
        img = Image.open(png_file)
        combined_img.paste(img, (0, i * height))
        #with Image.open(png_file) as img:
        #    combined_img.paste(img, (0, i * height))
    # Save the combined image as a PDF
    combined_img.save(output_pdf, "PDF", resolution=100.0)


def combine_png_to_pdf_2(png_files, pdf_file):
    images = []
    for file in png_files:
        image = Image.open(file)
        image = image.convert('RGB')
        images.append(image)
    images[0].save(pdf_file, save_all=True, append_images=images[1:])


def combine_png_to_pdf_3(png_files, pdf_file):
    img = Image.open(png_files[0])
    w,h=img.size
    images = []
    for i, png_file in enumerate(png_files):
        if i%4 ==0:
            new_image = Image.new('RGB', (w*2, h*2),(255,255,255))
            new_image.paste(Image.open(png_file), (0, 0))
            if (i+1) == len(png_files):
                images.append(new_image)
        if i%4 ==1:
            new_image.paste(Image.open(png_file), (w, 0))
            if (i+1) == len(png_files):
                images.append(new_image)
        if i%4 ==2:
            new_image.paste(Image.open(png_file), (0, h))
            if (i+1) == len(png_files):
                images.append(new_image)
        if i%4 ==3:
            new_image.paste(Image.open(png_file), (w, h))
            images.append(new_image)
    images[0].save(pdf_file, save_all=True, append_images=images[1:])

def combine_png_to_pdf_D(png_files, pdf_file):
    print(len(png_files),len(png_files)//4,len(png_files)%4)
    #for file in png_files:
    img1 = Image.open('CH01.png')
    img2 = Image.open('CH02.png')
    img3 = Image.open('CH03.png')
    img4 = Image.open('CH04.png')

    # get width and height
    w1, h1 = img1.size
    w2, h2 = img2.size
    w3, h3 = img3.size
    w4, h4 = img4.size

    # to calculate size of new image 
    w = max(w1, w2, w3, w4)
    h = max(h1, h2, h3, h4)

    # create big empty image with place for images
    new_image = Image.new('RGB', (w*2, h*2))

    # put images on new_image
    new_image.paste(img1, (0, 0))
    new_image.paste(img2, (w, 0))
    new_image.paste(img3, (0, h))
    new_image.paste(img4, (w, h))

    # save it
    new_image.save('new.png')
    new_image.save(pdf_file, save_all=True)

def png_to_grid(png_files,out_png,
    cell_size=None,           # None: 自動用最大寬高當格子大小
    margin=20,                # 外框留白
    gap=20,                   # 圖與圖間距
    bg_color=(255, 255, 255)  # 背景色：白
):
    assert len(png_files) == 7, "請提供剛好 7 張 PNG 檔案"

    imgs = [Image.open(p).convert("RGBA") for p in png_files]

    # 決定每格大小（cell）
    if cell_size is None:
        cell_w = max(im.width for im in imgs)
        cell_h = max(im.height for im in imgs)
    else:
        cell_w, cell_h = cell_size

    # 縮放到 cell 內（保比例），置中在固定 cell 畫布
    def fit_to_cell(im):
        im = im.copy()
        im.thumbnail((cell_w, cell_h), Image.Resampling.LANCZOS)
        cell = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 0))
        x = (cell_w - im.width) // 2
        y = (cell_h - im.height) // 2
        cell.paste(im, (x, y), im)
        return cell

    cells = [fit_to_cell(im) for im in imgs]
    # 固定 4 欄、2 列（上排4張、下排3張，右下角留白）
    cols = 4
    rows = 2

    out_w = margin * 2 + cols * cell_w + (cols - 1) * gap
    out_h = margin * 2 + rows * cell_h + (rows - 1) * gap

    canvas = Image.new("RGBA", (out_w, out_h), bg_color + (255,))

    # 上排：0~3
    for i in range(4):
        x = margin + i * (cell_w + gap)
        y = margin
        canvas.paste(cells[i], (x, y), cells[i])

    # 下排：4~6（放在第0~2欄，第3欄自然空白）
    for j in range(3):
        x = margin + j * (cell_w + gap)
        y = margin + (cell_h + gap)
        canvas.paste(cells[4 + j], (x, y), cells[4 + j])
    canvas.convert("RGB").save(out_png, "PNG")



png_files = ['CH01.png', 'CH02.png', 'CH03.png','CH04.png','CH05.png','CH06.png','CH07.png','CH08.png']

output_pdf = 'combined_images_1.pdf'
combine_png_to_pdf(png_files, output_pdf)

output_pdf = 'combined_images_2.pdf'
combine_png_to_pdf_2(png_files, output_pdf)

output_pdf = 'combined_images_3.pdf'
combine_png_to_pdf_3(png_files, output_pdf)

png_files = ['CH07.png', 'CH31.png', 'CH19.png','CH20.png','CH33.png','CH34.png','CH44.png']
output_pdf = 'spec_check.png'
png_to_grid(png_files,output_pdf)
