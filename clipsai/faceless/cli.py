# standard library imports
import argparse
import json

# local imports
from .pipeline import FacelessVideoGenerator


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a faceless video")
    parser.add_argument("--script", required=True, help="Narration text or path to .txt")
    parser.add_argument("--out", required=True, help="Output MP4 path (absolute)")
    parser.add_argument(
        "--images",
        default=None,
        help="JSON list of absolute image paths, or path to a .json file containing list",
    )
    parser.add_argument("--voice", default=None, help="TTS voice identifier")
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()

    # Load script
    script_text = args.script
    if script_text.lower().endswith(".txt"):
        with open(script_text, "r", encoding="utf-8") as f:
            script_text = f.read()

    # Load images
    image_paths = None
    if args.images:
        val = args.images
        if val.lower().endswith(".json"):
            with open(val, "r", encoding="utf-8") as f:
                image_paths = json.load(f)
        else:
            image_paths = json.loads(val)

    gen = FacelessVideoGenerator(resolution=(args.width, args.height), fps=args.fps)
    out = gen.generate(
        script_text=script_text,
        output_video_path=args.out,
        image_paths=image_paths,
        voice=args.voice,
    )
    print(out)


if __name__ == "__main__":
    main()