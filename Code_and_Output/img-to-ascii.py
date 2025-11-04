from PIL import Image, ImageEnhance


ASCII_CHARACTERS = "@%#*+=-:. "  #After analysing multiple characters, These are the best suited ones to create an image (Dense -> Rare characters).

def resize_image(image, new_width=300): #Resizing the image to maintain the aspect ratio.
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.5)
    return image.resize((new_width, new_height))

def monochrome(image):
    return image.convert("L")

def enhance(image):  #Increasing the Contrast
    image = ImageEnhance.Contrast(image).enhance(2.0)   # Strong contrast
    image = ImageEnhance.Brightness(image).enhance(1.1) # Slight brightness boost
    return image

def pixels_to_ascii(image):  #Mapping grayscale characters to image pixels.
    pixels = image.getdata()
    ascii_str = "".join(ASCII_CHARACTERS[pixel * len(ASCII_CHARACTERS) // 256] for pixel in pixels) #Mapping dense characters and rare characters.
    return ascii_str

def image_to_ascii(image_path, new_width=300): #Opening the image.
    try:
        image = Image.open(image_path) 
    except:
        print("Image was not found. Verify the path and try again.")
        return None

    image = enhance(monochrome(resize_image(image, new_width)))
    ascii_str = pixels_to_ascii(image)
    width = image.width
    ascii_image = "\n".join(ascii_str[i:i + width] for i in range(0, len(ascii_str), width)) #Breaking the long ASCII into multiple lines.
    return ascii_image

def save_to_txt(ascii_art, output_file="ascii_art.txt"):  #Saving the image (characters) in a textfile to be put in the html webpage.
    with open(output_file, "w", encoding="utf-8") as f:  #Encoding with UTF-8 as windows uses W-1252 and the characters change.
        f.write(ascii_art)
    print(f"Saved ASCII text to {output_file}")

def save_as_html(ascii_art, output_file="ascii_art.html"): #Saving the HTML file with the textfile in its body.
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{background-color: rgba(228, 228, 228); color: black; font-family: monospace; white-space: pre; font-size: 1px; line-height: 1px;}}
        </style>
    </head>
    <body>
        {ascii_art}
    </body>
    </html> """
    with open(output_file, "w", encoding="utf-8") as f: #Creating the html file.
        f.write(html)
    print("HTML file saved")

#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    path = "SVJ63.jpg"   # Image File (supports jpg, png and jpeg).
    width = 4000  # Adjusting Width (Keep it roughly 2x-4x of your image size).
    #To view the image, Zoomout of the html webpage to 25% or 33% depending on the size of your image (Maximum image width is 2000px)

    ascii_art = image_to_ascii(path, new_width=width)

    if ascii_art:
        output_file = f"ascii_art.html"
        save_as_html(ascii_art, output_file=output_file)
