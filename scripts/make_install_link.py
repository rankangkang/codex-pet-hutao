"""Print the documented desktop pet install link for an HTTPS sprite URL."""
import argparse
import json
from pathlib import Path
from urllib.parse import quote, urlencode, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def make_install_link(image_url, name, description="", sprite_version=2):
    parsed = urlsplit(image_url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Use an absolute HTTPS sprite URL without embedded credentials.")
    if any(ord(character) < 32 or character.isspace() for character in image_url):
        raise ValueError("The image URL must not contain unencoded whitespace or control characters.")
    if not name.strip():
        raise ValueError("Pet name must not be blank.")
    if sprite_version not in (1, 2):
        raise ValueError("Only sprite versions 1 and 2 are supported.")
    query = {"name": name, "imageUrl": image_url, "spriteVersionNumber": str(sprite_version)}
    if description:
        query["description"] = description
    return "codex://pets/install?" + urlencode(query, quote_via=quote)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image-url", required=True, help="Direct, accessible HTTPS PNG/WebP URL")
    parser.add_argument("--manifest", type=Path, default=ROOT / "pet.json")
    parser.add_argument("--name")
    args = parser.parse_args()
    metadata = json.loads(args.manifest.read_text(encoding="utf-8"))
    try:
        link = make_install_link(
            args.image_url, args.name or metadata["name"], metadata.get("description", ""),
            metadata["spriteVersionNumber"],
        )
    except ValueError as error:
        parser.error(str(error))
    print(link)


if __name__ == "__main__":
    main()

