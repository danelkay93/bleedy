from PIL import Image
# import cv2
from io import BytesIO

from pyscript import when, display  # noqa # pyright: ignore [reportAttributeAccessIssue]
from pyscript.web import page  # noqa # pyright: ignore [reportMissingImports]
from pyscript.ffi import to_js  # noqa # pyright: ignore [reportMissingImports]
from js import document, window, console, Uint8Array, File, URL # noqa # pyright: ignore [reportMissingImports]

async def add_bleed(image: Image, bleed: int) -> Image:
    console.log(f"Adding {bleed} pixels of bleed to the image")
    old_width, old_height = image.size
    new_img = Image.new("RGB", (old_width + 2 * bleed, old_height + 2 * bleed))
    new_img.paste(image, (bleed, bleed))

    for y, vertical_position in [(0, 0), (old_height - bleed, old_height + bleed)]:
        segment = image.crop((0, y, old_width, y + bleed)).transpose(
                Image.Transpose.FLIP_TOP_BOTTOM)
        new_img.paste(segment, (bleed, vertical_position))

    for x, horizontal_position in [(bleed, 0), (old_width, old_width + bleed)]:
        segment = new_img.crop((x, 0, x + bleed, old_height + 2 * bleed)).transpose(
                Image.Transpose.FLIP_LEFT_RIGHT)
        new_img.paste(segment, (horizontal_position, 0))

    console.log("Bleed added to the image")
    return new_img

async def process_image(img: Image, bleed: int) -> Image:
    if bleed <= 0:
        console.log("No bleed required. Returning original image.")
        return img
    return await add_bleed(img, bleed)


async def create_image_file(modified_image: Image, name: str, fmt: str) -> File:
    stream = BytesIO()
    modified_image.save(stream, format=fmt.upper())
    stream_val = stream.getvalue()
    js_array = Uint8Array.new(len(stream_val))
    js_array.assign(stream_val)
    # js_array = Uint8Array.new(stream.getvalue())

    return File.new([to_js(js_array)], name, to_js({"type": f"image/{fmt.lower()}"}))

async def display_image_file(img_file: File):
    #Create new tag and insert into page
    new_image = document.createElement('img')
    new_image.src = URL.createObjectURL(img_file)
    document.getElementById("bleedy-output").appendChild(new_image)


@when("process-images", "div[id='image-processor-component']")
async def process_files(event):
    console.log("Processing images in PyScript!")
    files = event.detail.files.to_py()  # Convert JS objects to Python
    bleed_amount = event.detail.bleedAmount
    console.log(f"Bleed amount: {bleed_amount}")

    for i, file in enumerate(files):
        console.log(f"Processing file: {file.name}")
        array_buf = Uint8Array.new(await file.arrayBuffer())
        bytes_list = bytearray(array_buf)
        image_bytes = BytesIO(bytes_list)
        img = Image.open(image_bytes)
        console.log(f"Image {i + 1}: {file.name} opened. Format: {img.format}, Width: {img.width}, Height: {img.height}")
        modified_image = await process_image(img, bleed_amount)
        modified_img_file = await create_image_file(modified_image, file.name, img.format)
        await display_image_file(modified_img_file)
        # Example: processing file data with PIL
        # file_data = file.arrayBuffer().to_py()
        # img = Image.open(BytesIO(file_data))
        # img_with_border = ImageOps.expand(img, border=bleed_amount, fill="red")
        # img_with_border.show()
        console.log(f"File {i + 1}: {file.name} processed.")