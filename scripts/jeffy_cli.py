"""Small standard-library CLI for the locally installed Jeffy package."""

import argparse
import importlib.metadata
import importlib.resources
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def run_native(command, arguments):
    if command == "train" and not any(
        arg == "--save-dir" or arg.startswith("--save-dir=") for arg in arguments
    ):
        arguments = [*arguments, "--save-dir", str(ROOT / "models" / "jeffy")]
    entry = next(
        entry for entry in importlib.metadata.distribution("jeffy-classify").entry_points
        if entry.name == f"jeffy-{command}"
    )
    sys.argv = [entry.name, *arguments]
    return entry.load()()


def main():
    # Preserve upstream training options and its own --help output.
    if len(sys.argv) > 1 and sys.argv[1] == "train":
        return run_native(sys.argv[1], sys.argv[2:])

    parser = argparse.ArgumentParser(prog="./jeffy", description="Project-local Jeffy classifier CLI")
    parser.add_argument("--version", action="version", version=importlib.metadata.version("jeffy-classify"))
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="List model manifests without downloading encoders")
    listing.add_argument("--pack-dir", type=Path, help="Custom model pack directory")
    predict = commands.add_parser("predict", help="Classify text and print Jeffy's JSON result")
    predict.add_argument("task", help="Classifier ID, e.g. banking77 or sms_spam")
    predict.add_argument("text", help="Query to classify (quote text containing spaces)")
    predict.add_argument("--pack-dir", type=Path, help="Custom model pack directory")
    commands.add_parser("train", help="Train from CSV/TSV/JSONL; use train --help for options")
    serve = commands.add_parser("serve", help="Start Jeffy's local playground")
    serve.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    serve.add_argument("--port", type=int, default=int(os.environ.get("JEFFY_PORT", "8400")))
    serve.add_argument("--pack-dir", type=Path, help="Custom model pack directory")
    args = parser.parse_args()

    if args.command == "serve":
        if args.pack_dir:
            os.environ["JEFFY_PACK_DIR"] = str(args.pack_dir.resolve())
        import uvicorn
        uvicorn.run("jeffy.server:app", host=args.host, port=args.port)
        return 0

    pack = args.pack_dir or os.environ.get("JEFFY_PACK_DIR")
    if pack is None:
        pack = Path(str(importlib.resources.files("jeffy") / "pack"))
    pack = Path(pack).resolve()
    if not pack.is_dir():
        parser.error(f"Model pack directory does not exist: {pack}")
    manifests = sorted(pack.glob("*/manifest.json"))
    if not manifests:
        parser.error(f"No classifier manifests found in {pack}")
    if args.command == "list":
        for path in manifests:
            manifest = json.loads(path.read_text())
            print(f"{manifest['dataset']:25s} {manifest['n_classes']:3d} classes  {manifest['description']}")
        return 0

    # Reject unknown tasks before downloading/loading the text encoder.
    tasks = {json.loads(path.read_text())["dataset"] for path in manifests}
    if args.task not in tasks:
        parser.error(f"Unknown classifier {args.task!r}; run ./jeffy list")
    from jeffy.engine import Engine

    engine = Engine(pack_dir=str(pack), device="cpu")
    engine.load()
    result = engine.predict(args.task, args.text)
    print(json.dumps(result, indent=2))
    return 1 if "error" in result else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
