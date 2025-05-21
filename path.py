import os
import json
from svgelements import SVG, Path

input_folder = "fullmap/"
output_json = {}

for filename in os.listdir(input_folder):
    if not filename.endswith(".svg"):
        continue

    svg = SVG.parse(os.path.join(input_folder, filename))
    paths = []

    for element in svg.elements():
        if isinstance(element, Path):
            d = element.d()
            paths.append(f'{d}')

    key = os.path.splitext(filename)[0]
    output_json[key] = "\n".join(paths)

with open("test.json", "w") as f:
    json.dump(output_json, f, indent=2)

print(f"✅ Converted {len(output_json)} SVGs to output.json")
