"""Create an OpenPets import package using the existing pet artwork.

OpenPets 4.1 uses idle row column 6 as its static neutral pose. The original
Codex atlas reserves that cell, so this target-specific atlas copies idle frame
0 into it. The 73 authored animation frames are preserved exactly.
"""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CELL_WIDTH, CELL_HEIGHT = 192, 208


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package(manifest_path, output_root):
    project = json.loads(manifest_path.read_text(encoding="utf-8"))
    pet_id = project["slug"]
    if not isinstance(pet_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,63}", pet_id) or pet_id == "builtin":
        raise ValueError("Package slug must be an ASCII pet id.")
    source_path = manifest_path.parent / project["spritesheet"]
    original_sha = digest(source_path)
    with Image.open(source_path) as opened:
        original = opened.convert("RGBA")
    if project["spriteVersionNumber"] != 2 or original.size != (1536, 2288):
        raise ValueError("This exporter expects a 1536x2288 v2 atlas.")
    neutral = original.crop((0, 0, CELL_WIDTH, CELL_HEIGHT))
    if neutral.getchannel("A").getbbox() is None:
        raise ValueError("Idle frame 0 must contain a complete neutral pose.")
    expected = original.copy()
    expected.paste(neutral, (6 * CELL_WIDTH, 0))
    folder = output_root / pet_id
    folder.mkdir(parents=True, exist_ok=True)
    atlas_path = folder / "spritesheet.webp"
    expected.save(atlas_path, format="WEBP", lossless=True, quality=100, method=6, exact=True)
    with Image.open(atlas_path) as encoded:
        encoded.load()
        decoded = encoded.convert("RGBA")
    if decoded.size != expected.size or decoded.tobytes() != expected.tobytes():
        raise ValueError("WebP encoding changed the expected atlas pixels.")
    changed_cells = []
    for row in range(11):
        for column in range(8):
            x, y = column * CELL_WIDTH, row * CELL_HEIGHT
            bounds = (x, y, x + CELL_WIDTH, y + CELL_HEIGHT)
            if original.crop(bounds).tobytes() != decoded.crop(bounds).tobytes():
                changed_cells.append([row, column])
    if changed_cells not in ([], [[0, 6]]):
        raise ValueError(f"Unexpected artwork changes: {changed_cells}")
    metadata = {
        "id": pet_id,
        "displayName": project["name"],
        "description": project["description"],
        "spritesheetPath": "spritesheet.webp",
        "spriteVersionNumber": 2,
        "gazeAnchor": {"x": 0.5, "y": 0.45},
    }
    (folder / "pet.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    archive_path = output_root / f"{pet_id}-openpets.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for filename in ("pet.json", "spritesheet.webp"):
            archive.write(folder / filename, f"{pet_id}/{filename}")
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise ValueError("Archive integrity check failed.")
    if digest(source_path) != original_sha:
        raise ValueError("Original source atlas changed while packaging.")
    report = {
        "ok": True,
        "target": "OpenPets 4.1.0",
        "spriteVersionNumber": 2,
        "dimensions": [1536, 2288],
        "authored_animation_frames_preserved": 73,
        "changed_cells_zero_based": changed_cells,
        "static_neutral_cell_zero_based": [0, 6],
        "static_neutral_source_zero_based": [0, 0],
        "lossless_pixel_roundtrip": True,
        "source_sha256": original_sha,
        "spritesheet_sha256": digest(atlas_path),
        "zip_sha256": digest(archive_path),
        "zip_bytes": archive_path.stat().st_size,
        "source_reference": "https://github.com/OpenPetsHQ/openpets/blob/v4.1.0/apps/desktop/src/codex-pets-core.ts",
    }
    (output_root / f"{pet_id}-validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return {"archive": str(archive_path), "package_dir": str(folder), **report}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=ROOT / "pet.json")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "packages/openpets")
    args = parser.parse_args()
    print(json.dumps(package(args.manifest.resolve(), args.output_dir.resolve()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
