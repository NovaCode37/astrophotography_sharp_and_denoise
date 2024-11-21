from PIL import Image
from astropy.io import fits
import cv2
import numpy as np
import matplotlib.pyplot as plt

def sharpen_image(image_array, strength=1.0, radius=1.0):
    """
    Sharpens an image using unsharp masking.  Handles different data types more robustly.
    """
    image_array = image_array.astype(np.float32)
    blurred = cv2.GaussianBlur(image_array, (0, 0), radius)
    sharpened = cv2.addWeighted(image_array, 1 + strength, blurred, -strength, 0)
    sharpened = np.clip(sharpened, 0, 255)
    return sharpened.astype(image_array.dtype)


def process_tiff(tiff_path, output_path, strength=1.0, radius=1.0,show_images=False):
    try:
        img = Image.open(tiff_path)
        img_array = np.array(img)
        original_dtype = img_array.dtype

        if len(img_array.shape) == 3:
            sharpened_array = np.zeros_like(img_array, dtype=np.float32)
            for i in range(img_array.shape[2]):
                sharpened_array[:, :, i] = sharpen_image(img_array[:, :, i], strength, radius)
        else:
            sharpened_array = sharpen_image(img_array, strength, radius)

        sharpened_img = Image.fromarray(sharpened_array.astype(original_dtype))
        sharpened_img.save(output_path)
        print(f"TIFF image processed and saved as {output_path}")

        if show_images:
            plt.figure(figsize=(10, 5))
            plt.subplot(121)
            plt.imshow(img)
            plt.title('Original')
            plt.subplot(122)
            plt.imshow(sharpened_img)
            plt.title('Sharpened')
            plt.show()

    except FileNotFoundError:
        print(f"Error: TIFF file not found: {tiff_path}")
    except Exception as e:
        print(f"Error processing TIFF: {e}")


def process_fits(fits_path, output_path, strength=1.0, radius=1.0, show_images=False):
    try:
        with fits.open(fits_path) as hdul:
            data = hdul[0].data
            if data is None or data.size == 0:
                print("FITS file is empty or contains no image data.")
                return

            original_dtype = data.dtype
            sharpened_data = sharpen_image(data, strength, radius)
            hdul[0].data = sharpened_data.astype(original_dtype)
            hdul.writeto(output_path, overwrite=True)
            print(f"FITS image processed and saved as {output_path}")

            if show_images:
                plt.figure(figsize=(10, 5))
                plt.subplot(121)
                plt.imshow(data, cmap='gray', origin='lower')
                plt.title('Original')
                plt.subplot(122)
                plt.imshow(sharpened_data, cmap='gray', origin='lower')
                plt.title('Sharpened')
                plt.show()

    except FileNotFoundError:
        print(f"Error: FITS file not found: {fits_path}")
    except Exception as e:
        print(f"Error processing FITS: {e}")



tiff_input = "input.tif" # ur path
tiff_output = "output_tiff.tif"
fits_input = r"ur_image.fits / ur_image.tiff" # ur path
fits_output = "sharpened_image.fits"

process_tiff(tiff_input, tiff_output, strength=0.8, radius=2.5)
process_fits(fits_input, fits_output, strength=0.8, radius=2.5)