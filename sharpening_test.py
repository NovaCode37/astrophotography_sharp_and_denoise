import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from astropy.io import fits
import cv2
import numpy as np
import matplotlib.pyplot as plt


def sharpen_image(image_array, strength=1.0, radius=1.0):
    image_array = image_array.astype(np.float32)
    blurred = cv2.GaussianBlur(image_array, (0, 0), radius)
    sharpened = cv2.addWeighted(image_array, 1 + strength, blurred, -strength, 0)
    sharpened = np.clip(sharpened, 0, 255)
    return sharpened.astype(image_array.dtype)


def process_image(input_path, output_path, strength, radius, image_type):
    try:
        if image_type == "TIFF":
            img = Image.open(input_path)
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

        elif image_type == "FITS":
            with fits.open(input_path) as hdul:
                data = hdul[0].data
                if data is None or data.size == 0:
                    print("FITS file is empty or contains no image data.")
                    return
                original_dtype = data.dtype
                sharpened_data = sharpen_image(data, strength, radius)
                hdul[0].data = sharpened_data.astype(original_dtype)
                hdul.writeto(output_path, overwrite=True)
                print(f"FITS image processed and saved as {output_path}")
        else:
            print("Unsupported image type.")
            return

    except FileNotFoundError:
        print(f"Error: File not found: {input_path}")
    except Exception as e:
        print(f"Error processing image: {e}")


def browse_input_file():
    filepath = filedialog.askopenfilename()
    input_path_entry.delete(0, tk.END)
    input_path_entry.insert(0, filepath)

def browse_output_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".tif") 
    output_path_entry.delete(0, tk.END)
    output_path_entry.insert(0, filepath)


def process_button_clicked():
    input_path = input_path_entry.get()
    output_path = output_path_entry.get()
    strength = float(strength_entry.get())
    radius = float(radius_entry.get())
    image_type = image_type_var.get()

    if not input_path or not output_path:
        result_label.config(text="Please specify input and output paths.")
        return

    process_image(input_path, output_path, strength, radius, image_type)
    result_label.config(text=f"Image processed successfully.")



root = tk.Tk()
root.title("Image Sharpening Tool")

input_path_label = tk.Label(root, text="Input File Path:")
input_path_label.grid(row=0, column=0, sticky="w")
input_path_entry = tk.Entry(root, width=40)
input_path_entry.grid(row=0, column=1)
browse_input_button = tk.Button(root, text="Browse Input", command=browse_input_file)
browse_input_button.grid(row=0, column=2)

output_path_label = tk.Label(root, text="Output File Path:")
output_path_label.grid(row=1, column=0, sticky="w")
output_path_entry = tk.Entry(root, width=40)
output_path_entry.grid(row=1, column=1)
browse_output_button = tk.Button(root, text="Browse Output", command=browse_output_file)
browse_output_button.grid(row=1, column=2)

strength_label = tk.Label(root, text="Sharpening Strength (0.0-2.0):")
strength_label.grid(row=2, column=0, sticky="w")
strength_entry = tk.Entry(root, width=10)
strength_entry.grid(row=2, column=1)
strength_entry.insert(0, "0.8")

radius_label = tk.Label(root, text="Gaussian Radius (1.0-10.0):")
radius_label.grid(row=3, column=0, sticky="w")
radius_entry = tk.Entry(root, width=10)
radius_entry.grid(row=3, column=1)
radius_entry.insert(0, "2.5")

image_type_var = tk.StringVar(value="TIFF")
image_type_label = tk.Label(root, text="Image Type:")
image_type_label.grid(row=4, column=0, sticky="w")
image_type_menu = tk.OptionMenu(root, image_type_var, "TIFF", "FITS")
image_type_menu.grid(row=4, column=1)

process_button = tk.Button(root, text="Process Image", command=process_button_clicked)
process_button.grid(row=5, column=1)

result_label = tk.Label(root, text="")
result_label.grid(row=6, column=1)


root.mainloop()

#gui added
