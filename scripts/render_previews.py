"""Render this pet's encoded sprite pixels into GIFs, stills and optional MP4."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from pet_format import CELL_HEIGHT, CELL_WIDTH, FRAME_COUNTS, LOOK_LABELS, ROW_DURATIONS

ROOT = Path(__file__).resolve().parents[1]


def save_gif(frames, durations, output):
    frames[0].save(
        output, save_all=True, append_images=frames[1:], duration=durations,
        loop=0, disposal=2, optimize=False,
    )


def render(atlas_path, output_dir):
    with Image.open(atlas_path) as image:
        if image.size != (1536, 2288):
            raise ValueError(f"Expected 1536x2288 v2 atlas; got {image.size}")
        atlas = image.convert("RGBA")
    output_dir.mkdir(parents=True, exist_ok=True)

    def cell(row, column):
        x, y = column * CELL_WIDTH, row * CELL_HEIGHT
        return atlas.crop((x, y, x + CELL_WIDTH, y + CELL_HEIGHT))

    def panel(frame, label):
        result = Image.new("RGB", (224, 250), "#fff7e8")
        result.paste(frame, (16, 30), frame)
        ImageDraw.Draw(result).text((12, 10), label, fill="#42344c")
        return result

    all_frames, all_durations, states = [], [], {}
    for row, (state, durations) in enumerate(ROW_DURATIONS.items()):
        frames = [cell(row, index) for index in range(FRAME_COUNTS[row])]
        states[state] = frames
        save_gif(frames, durations, output_dir / f"{state}.gif")
        all_frames.extend(panel(frame, f"{state} / {i + 1}") for i, frame in enumerate(frames))
        all_durations.extend(durations)
    save_gif(all_frames, all_durations, output_dir / "all-states.gif")
    jump = states["idle"] + states["jumping"] + states["idle"]
    times = ROW_DURATIONS["idle"] + ROW_DURATIONS["jumping"] + ROW_DURATIONS["idle"]
    save_gif(jump, times, output_dir / "idle-jump-idle.gif")
    look = [panel(cell(9 + i // 8, i % 8), f"look {label}") for i, label in enumerate(LOOK_LABELS)]
    save_gif(look, [180] * len(look), output_dir / "look-loop.gif")
    examples = [
        (0, 0, "idle"), (3, 1, "waving"), (4, 2, "jump peak"),
        (7, 2, "working"), (9, 4, "look right"), (10, 4, "look left"),
    ]
    stills = Image.new("RGB", (224 * len(examples), 250), "#fff7e8")
    for i, (row, column, label) in enumerate(examples):
        stills.paste(panel(cell(row, column), label), (224 * i, 0))
    stills.save(output_dir / "motion-stills.png")
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        subprocess.run([
            ffmpeg, "-y", "-v", "error", "-i", str(output_dir / "all-states.gif"),
            "-vf", "fps=30,pad=ceil(iw/2)*2:ceil(ih/2)*2", "-c:v", "libx264",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output_dir / "all-states.mp4"),
        ], check=True)
    return {"ok": True, "output_dir": str(output_dir), "mp4_created": bool(ffmpeg)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atlas", type=Path, default=ROOT / "assets/spritesheet.png")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "build/previews")
    args = parser.parse_args()
    print(json.dumps(render(args.atlas.resolve(), args.output_dir.resolve()), indent=2))


if __name__ == "__main__":
    main()

