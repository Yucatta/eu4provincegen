import cv2
import numpy as np
from PIL import Image

def rgb_mask(image, rgb_color):
    data = np.array(image)
    return (np.all(data == rgb_color, axis=-1).astype(np.uint8)) * 255

def contour_to_svg_path(contour):
    points = contour.squeeze()
    path_data = "M " + " L ".join(f"{x},{y}" for x, y in points) + " Z"
    return f'<path d="{path_data}" fill="none" stroke="black" stroke-width="1"/>'

def save_svg(paths, width, height, filename="province.svg"):
    with open(filename, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n')
        for path in paths:
            f.write(f"  {path}\n")
        f.write("</svg>")

# --- Main Example ---
img = Image.open("provinces.bmp").convert("RGB")
rgb = (173,34,64)  # Your target province color
mask = rgb_mask(img, rgb)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
svg_paths = [contour_to_svg_path(c) for c in contours]

save_svg(svg_paths, img.width, img.height)
print("SVG saved as province.svg")
