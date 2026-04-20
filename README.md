# Astrophotography Sharp & Denoise

Desktop GUI toolkit for post-processing astrophotography images. Provides two standalone tools — **image sharpening** and **noise reduction** — designed to work with raw astronomical data in FITS and TIFF formats.

## Features

### Sharpening Tool
- Unsharp mask algorithm using Gaussian blur subtraction
- Adjustable **strength** (0.0–2.0) and **Gaussian radius** (1.0–10.0)
- Per-channel processing for multi-channel images
- Supports FITS and TIFF input/output

### Denoising Tool
Three noise reduction methods optimized for different types of astronomical noise:

| Method | Best for | Key parameter |
|--------|----------|---------------|
| **Median filter** | Salt-and-pepper noise, hot pixels | Fixed 3×3 kernel |
| **TV-Chambolle** | Smooth background gradients, light pollution artifacts | `weight` (default: 0.1) |
| **Kappa-sigma clipping** | Cosmic ray hits, statistical outliers | `sigma` (default: 3.0) |

### General
- Tkinter-based GUI with file browser dialogs
- Preserves original data types and FITS headers
- FITS and TIFF format support

## Tech Stack

- **Python 3.10+**
- **OpenCV** — Gaussian blur, weighted blending for sharpening
- **Astropy** — FITS I/O, sigma clipping
- **scikit-image** — Total Variation denoising (Chambolle)
- **SciPy** — median filtering
- **NumPy** — array operations
- **Pillow** — TIFF I/O
- **Tkinter** — GUI

## Usage

### Sharpening
```bash
python sharpening_test.py
```
1. Browse and select input image (FITS or TIFF)
2. Choose output file path
3. Set sharpening strength and Gaussian radius
4. Click **Process**

### Denoising
```bash
python denoise_test.py
```
1. Browse and select input image
2. Choose output file path
3. Select method (median / tv_chambolle / sigma_clip)
4. Adjust sigma and weight parameters
5. Click **Process**

## How It Works

**Sharpening** applies an unsharp mask: the original image is blended with a Gaussian-blurred copy using `cv2.addWeighted`, emphasizing fine details like star edges and nebula structures.

**Denoising** offers three approaches:
- **Median filter** replaces each pixel with the median of its 3×3 neighborhood, effective against isolated hot pixels common in long-exposure astro captures
- **TV-Chambolle** minimizes total variation while preserving edges, useful for reducing smooth background noise without destroying star profiles
- **Kappa-sigma clipping** iteratively masks pixels that deviate beyond N sigma from the mean, targeting cosmic ray artifacts and statistical outliers

## Project Structure

```
├── sharpening_test.py   Sharpening tool with GUI
├── denoise_test.py      Denoising tool with GUI
└── README.md
```

## Future Work

- Batch processing for multiple images
- Before/after preview in the GUI
- Stacking module for combining multiple exposures
- Dark frame and flat field calibration
- Command-line interface for scripted workflows

## License

MIT
