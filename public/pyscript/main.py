from PIL import Image
from io import BytesIO

from pyscript import when # noqa # pyright: ignore [reportAttributeAccessIssue]
from pyscript.ffi import to_js # noqa # pyright: ignore [reportMissingImports]
# window is kept for performance.now(), console, Uint8Array, File, URL are used.
# document, display, page are no longer needed.
from js import window, console, Uint8Array, File, URL # noqa # pyright: ignore [reportMissingImports]
from pyscript.js_modules import interop # Our new JS bridge

async def add_bleed(image: Image, bleed: int) -> Image:
    console.log(f"(PY) Adding {bleed} pixels of bleed to the image")
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

    console.log("(PY) Bleed added to the image")
    return new_img

async def process_image(img: Image, bleed: int) -> Image:
    if bleed <= 0:
        console.log("(PY) No bleed required. Returning original image.")
        return img
    return await add_bleed(img, bleed)

async def create_image_file(modified_image: Image, name: str, fmt: str) -> File:
    stream = BytesIO()
    actual_fmt = fmt if fmt else 'PNG' # Ensure format is not None for saving
    modified_image.save(stream, format=actual_fmt.upper())
    stream_val = stream.getvalue()
    js_array = Uint8Array.new(len(stream_val))
    js_array.assign(stream_val)

    # Create a JS File object. Name and type are important for blob URL and download.
    return File.new([to_js(js_array)], name, to_js({"type": f"image/{actual_fmt.lower()}"}))

# display_image_file function is removed as results are dispatched via interop

@when("process-images", ".image-bleed-processor")
async def process_files(event):
    console.log("🚀 (PY) Starting image processing in PyScript!")
    try:
        files_js = event.detail.files # Keep as JS Array-like of File objects (e.g., FileList)
        bleed_amount = event.detail.bleedAmount
        num_files = files_js.length # Use .length for JS FileList or Array

        console.log(f"📏 (PY) Bleed amount set to: {bleed_amount}px")
        console.log(f"🖼️ (PY) Number of images to process: {num_files}")

        start_time = window.performance.now()
        processed_count = 0

        def update_progress():
            elapsed = (window.performance.now() - start_time) / 1000  # in seconds
            progress_val = (processed_count / num_files) * 100 if num_files > 0 else 0
            rate = processed_count / elapsed if elapsed > 0 else 0
            remaining_val = (num_files - processed_count) / rate if rate > 0 else 0

            progress_detail = {
                "progress": progress_val,
                "processed": processed_count,
                "total": num_files,
                "elapsed": elapsed,
                "remaining": remaining_val
            }
            # Dispatch progress event using the interop module
            # Ensure the dictionary is converted to a JS object for the JS function
            interop.dispatchProgressToVue(to_js(progress_detail))

        # Initial progress update (0%)
        update_progress()

        for i in range(num_files):
            file_obj = files_js.item(i) # Get File object from FileList/JS Array
            console.log(f"⚙️ (PY) Processing file {i + 1}/{num_files}: {file_obj.name}")

            array_buf = Uint8Array.new(await file_obj.arrayBuffer()) # Get ArrayBuffer from JS File
            bytes_list = bytearray(array_buf) # Convert to bytearray for BytesIO
            image_bytes = BytesIO(bytes_list)
            img = Image.open(image_bytes)

            img_format_str = img.format if img.format else 'PNG' # Default to PNG if format is not detected
            console.log(f"📄 (PY) Image details - Name: {file_obj.name}, Format: {img_format_str}, Size: {img.width}x{img.height}")

            modified_image = await process_image(img, bleed_amount)
            modified_img_file = await create_image_file(modified_image, file_obj.name, img_format_str)

            # Create a blob URL in Python to pass to JS, as JS side expects a URL
            blob_url = URL.createObjectURL(modified_img_file)

            # Dispatch processed image data to Vue via JS interop module
            interop.dispatchProcessedImageToVue(modified_img_file.name, blob_url, img_format_str)

            processed_count += 1
            update_progress() # Update progress after each image

            console.log(f"✅ (PY) File {i + 1}/{num_files}: {file_obj.name} processed successfully")

        console.log("🎉 (PY) All images processed successfully!")
    except Exception as e:
        console.error(f"❌ (PY) Error processing images: {str(e)}")
        # Future: dispatch an error event to JS/Vue via interop
        # if hasattr(interop, 'dispatchErrorToVue'):
        # interop.dispatchErrorToVue(str(e))
