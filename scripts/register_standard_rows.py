"""Apply one stable scale and ground transform per extracted animation row.

The jump row's original displacement is preserved. Its resting height determines
the common neutral height, leaving actual overhead space for the airborne pose.
No artwork is synthesized or individually fit to a bounding box.
"""
import argparse
import json
from pathlib import Path

from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("source_root")
parser.add_argument("output_root")
args = parser.parse_args()
source, output = Path(args.source_root), Path(args.output_root)
manifest = json.loads((source / "frames-manifest.json").read_text())
jump_rest = Image.open(source / "jumping/04.png").convert("RGBA")
rest_bounds = jump_rest.getbbox()
target_height = rest_bounds[3] - rest_bounds[1]
ground = rest_bounds[3]
transforms = {}
for row in manifest["rows"]:
    state = row["state"]
    files = sorted((source / state).glob("*.png"))
    anchor_index = 4 if state == "jumping" else 0
    anchor = Image.open(files[anchor_index]).convert("RGBA")
    bounds = anchor.getbbox()
    scale = target_height / (bounds[3] - bounds[1])
    width, height = round(192 * scale), round(208 * scale)
    left = (192 - width) // 2
    top = ground - round(bounds[3] * scale)
    destination = output / state
    destination.mkdir(parents=True, exist_ok=True)
    for path in files:
        frame = Image.open(path).convert("RGBA")
        if frame.size != (width, height):
            frame = frame.resize((width, height), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (192, 208))
        canvas.alpha_composite(frame, (left, top))
        canvas.save(destination / path.name)
    row["frames"] = [str((destination / path.name).resolve()) for path in files]
    transforms[state] = {"scale": scale, "left": left, "top": top, "reference_index": anchor_index}
output.mkdir(parents=True, exist_ok=True)
(output / "frames-manifest.json").write_text(json.dumps(manifest, indent=2))
(output / "row-registration.json").write_text(json.dumps({"target_resting_height": target_height, "baseline": ground, "transforms": transforms}, indent=2))
print(json.dumps({"ok": True, "resting_height": target_height, "baseline": ground, "output_root": str(output.resolve())}, indent=2))
