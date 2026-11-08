"""Check package integrity and atlas occupancy; import still needs Pets preflight."""
import hashlib
import json
from pathlib import Path

from PIL import Image

from pet_format import CELL_HEIGHT, CELL_WIDTH, COLUMNS, FRAME_COUNTS, ROWS

ROOT = Path(__file__).resolve().parents[1]


def main():
    checksums = json.loads((ROOT / "checksums.json").read_text(encoding="utf-8"))
    for relative, expected in checksums.items():
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError(f"Missing or invalid package asset: {relative}")
        observed = hashlib.sha256(path.read_bytes()).hexdigest()
        if observed != expected:
            raise ValueError(f"SHA-256 mismatch: {relative}")
    metadata = json.loads((ROOT / "pet.json").read_text(encoding="utf-8"))
    atlas_path = (ROOT / metadata["spritesheet"]).resolve()
    if not atlas_path.is_relative_to(ROOT):
        raise ValueError("Atlas must be inside this package.")
    with Image.open(atlas_path) as opened:
        if opened.format != "PNG" or opened.mode != "RGBA":
            raise ValueError("Expected an RGBA PNG sprite sheet.")
        if opened.size != (CELL_WIDTH * COLUMNS, CELL_HEIGHT * ROWS):
            raise ValueError(f"Unexpected atlas dimensions: {opened.size}")
        alpha = opened.getchannel("A")
        for row, count in enumerate(FRAME_COUNTS):
            for column in range(COLUMNS):
                x, y = column * CELL_WIDTH, row * CELL_HEIGHT
                present = alpha.crop((x, y, x + CELL_WIDTH, y + CELL_HEIGHT)).getbbox() is not None
                if present != (column < count):
                    raise ValueError(f"Unexpected cell occupancy: row {row}, frame {column}")
    print(json.dumps({"ok": True, "assets_checked": len(checksums), "sprite_version": 2, "required_frames": sum(FRAME_COUNTS)}, indent=2))


if __name__ == "__main__":
    main()

