# Image Resizer

A simple desktop app (Python + Tkinter) for batch-resizing images to an exact size in centimeters, with an optional colored border. The interface is in Arabic with a dark theme.

## Features

- Add multiple folders and process them all in one run
- Set the target width and height in **centimeters**
- Optional border with selectable thickness (0 – 6 pt) and a custom color
- Progress bar while processing
- Originals are never modified: results go into a `resized images` subfolder inside each source folder
- Existing files are never overwritten (`photo.jpg` → `photo_1.jpg`, `photo_2.jpg`, ...)

## Supported formats

`.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`

## Requirements

- Python 3.8+
- [Pillow](https://pypi.org/project/Pillow/)
- Tkinter (included with the standard Python installer on Windows and macOS; on Linux install `python3-tk`)

```bash
pip install pillow
```

## Usage

```bash
python image_resizer.py
```

1. Click **إضافة مجلد** (Add folder) and pick a folder of images. Repeat for more folders.
   Use **حذف المحدد** (Remove selected) or **مسح الكل** (Clear all) to adjust the list.
2. Enter the **العرض** (width) and **الطول** (height) in centimeters.
3. *(Optional)* Choose the border thickness from the dropdown and pick a color with **لون الإطار** (Border color).
4. Click **بدء** (Start). A message appears when all folders are done.
5. Find the results in `<your folder>/resized images/`.

## How sizes are calculated

Centimeters are converted to pixels at **96 DPI**:

```
pixels = cm × 96 / 2.54
border_px = pt × 96 / 72
```

For example, a 10 × 15 cm image becomes about 378 × 567 px.

## Notes

- The border is added **around** the resized image, so the final image is larger than the requested size by `2 × border` pixels on each dimension.
- Images are stretched to the exact width and height; the aspect ratio is not preserved.
- The default border is 1 pt and the default color is white until changed in the UI.
- Saved files keep the original format and filename.

## Building an executable (optional)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico image_resizer.py
```

If an `icon.ico` file sits next to the script, it is used as the window icon.

## Project structure

```
image_resizer.py   # the application
icon.ico           # optional window icon
README.md
```
