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

png_files = ['CH01.png', 'CH02.png', 'CH03.png','CH04.png','CH05.png','CH06.png','CH07.png','CH08.png']

output_pdf = 'combined_images_1.pdf'
combine_png_to_pdf(png_files, output_pdf)

output_pdf = 'combined_images_2.pdf'
combine_png_to_pdf_2(png_files, output_pdf)

output_pdf = 'combined_images_3.pdf'
combine_png_to_pdf_3(png_files, output_pdf)
