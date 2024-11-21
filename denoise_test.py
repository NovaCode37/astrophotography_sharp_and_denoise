from astropy.io import fits
from astropy.stats import sigma_clip
from skimage.restoration import denoise_tv_chambolle
import numpy as np
from PIL import Image
from scipy.ndimage import median_filter

def reduce_noise(image_path, output_path, method='median', sigma=3.0, weight=0.1):
    try:                                            
        if image_path.lower().endswith(('.fit', '.fits')):
            with fits.open(image_path) as hdul:
                data = hdul[0].data
                if data is None:
                    raise ValueError("FITS file contains no image data in the primary HDU.")
                original_dtype = data.dtype
                hdul_primary = hdul[0]

        elif image_path.lower().endswith(('.tif', '.tiff')):
            img = Image.open(image_path)
            data = np.array(img)
            original_dtype = data.dtype
        else:
            raise ValueError(f"Unsupported image format: {image_path}")


        processed_data = data.copy()

        if method == 'median':
            processed_data = median_filter(data, size=3)
        elif method == 'sigma_clip':
            clipped_data = sigma_clip(data, sigma=sigma, maxiters=5)
            processed_data = np.nan_to_num(clipped_data)
        elif method == 'tv_chambolle':
            processed_data = denoise_tv_chambolle(data, weight=weight)
        else:
            raise ValueError("Invalid noise reduction method.")


        if image_path.lower().endswith(('.fit', '.fits')):
            hdul_primary.data = processed_data.astype(original_dtype)
            hdul.writeto(output_path, overwrite=True)
            print(f"FITS image processed and saved as {output_path}")
        else:
            processed_img = Image.fromarray(processed_data.astype(original_dtype))
            processed_img.save(output_path)
            print(f"TIFF image processed and saved as {output_path}")

    except FileNotFoundError:
        print(f"Error: Image file not found: {image_path}")
    except fits.VerifyError as e:
        print(f"Error: Problem verifying FITS file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

tiff_input = "input.tif" #ur path
tiff_output = "output_tiff.tif"
input_fits_file = r"ur_image.fits / ur_image.tiff" #ur path
output_fits_file = "output_denoised.fits"

reduce_noise(input_fits_file, output_fits_file, method='tv_chambolle', weight=0.01)
