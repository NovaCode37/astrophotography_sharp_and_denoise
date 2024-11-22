import tkinter as tk
from tkinter import filedialog
from astropy.io import fits
from astropy.stats import sigma_clip
from skimage.restoration import denoise_tv_chambolle
import numpy as np
from PIL import Image
from scipy.ndimage import median_filter
import os


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


def browse_input_file():
    filepath = filedialog.askopenfilename(filetypes=[("FITS files", "*.fit *.fits"), ("TIFF files", "*.tif *.tiff")])
    if filepath:
        input_path_entry.delete(0, tk.END)
        input_path_entry.insert(0, os.path.abspath(filepath))

def browse_output_file():
    filepath = filedialog.asksaveasfilename(filetypes=[("TIFF files", "*.tif *.tiff"), ("FITS files", "*.fit *.fits")], defaultextension=".tif") #Added FITS option
    if filepath:
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(0, os.path.abspath(filepath))

def process_button_clicked():
    input_path = input_path_entry.get()
    output_path = output_path_entry.get()
    method = method_var.get()
    try:
        sigma = float(sigma_entry.get())
    except ValueError:
        result_label.config(text="Invalid sigma value.")
        return
    try:
        weight = float(weight_entry.get())
    except ValueError:
        result_label.config(text="Invalid weight value.")
        return

    if not input_path or not output_path:
        result_label.config(text="Please specify input and output paths.")
        return

    if input_path.lower().endswith(('.fit', '.fits')) and not output_path.lower().endswith(('.fit', '.fits')):
        result_label.config(text="Output file type must be FITS if input is FITS.")
        return
    elif input_path.lower().endswith(('.tif', '.tiff')) and not output_path.lower().endswith(('.tif', '.tiff')):
        result_label.config(text="Output file type must be TIFF if input is TIFF.")
        return


    reduce_noise(input_path, output_path, method=method, sigma=sigma, weight=weight)
    result_label.config(text=f"Image processed successfully.")



root = tk.Tk()
root.title("Astronomical Image Denoising")

input_path_label = tk.Label(root, text="Input File Path:")
input_path_label.grid(row=0, column=0, sticky="w")
input_path_entry = tk.Entry(root, width=40)
input_path_entry.grid(row=0, column=1)
browse_input_button = tk.Button(root, text='Browse Input', command=browse_input_file)
browse_input_button.grid(row=0, column=2)

output_path_label = tk.Label(root, text="Output File Path:")
output_path_label.grid(row=1, column=0, sticky="w")
output_path_entry = tk.Entry(root, width=40)
output_path_entry.grid(row=1, column=1)
browse_output_button = tk.Button(root, text="Browse Output", command=browse_output_file)
browse_output_button.grid(row=1, column=2)

method_var = tk.StringVar(value="tv_chambolle")
method_label = tk.Label(root, text="Method:")
method_label.grid(row=2, column=0, sticky="w")
method_menu = tk.OptionMenu(root, method_var, "median", "sigma_clip", "tv_chambolle")
method_menu.grid(row=2, column=1)

sigma_label = tk.Label(root, text="Sigma (for sigma_clip):")
sigma_label.grid(row=3, column=0, sticky="w")
sigma_entry = tk.Entry(root, width=10)
sigma_entry.grid(row=3, column=1)
sigma_entry.insert(0, "3.0")

weight_label = tk.Label(root, text="Weight (for tv_chambolle):")
weight_label.grid(row=4, column=0, sticky="w")
weight_entry = tk.Entry(root, width=10)
weight_entry.grid(row=4, column=1)
weight_entry.insert(0, "0.01")

process_button = tk.Button(root, text="Process Image", command=process_button_clicked)
process_button.grid(row=5, column=1)

result_label = tk.Label(root, text="")
result_label.grid(row=6, column=1)

root.mainloop()

