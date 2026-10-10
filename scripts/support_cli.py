"""CLI for Pie Calendar's local csrouter model."""
import argparse
import json
import subprocess
import sys

from support_runtime import ROOT, Router, load_config


def display(result):
    print(result["answer"])
    if result["state"] == "answered":
        documented = [source for source in result["sources"] if source.get("url")]
        if documented:
            print("\nSources:")
        for source in documented:
            print(f"- {source['title']}: {source['url']}")
        print(f"\nRoute: {result['label']} | confidence: {result['confidence']:.4f}")
    if result.get("handoff"):
        print(f"\nContact: {result['handoff']['url']}")
        print("Handoff required; this local CLI has not sent the conversation.")


def chat(router):
    print("Pie Calendar support experiment. Type /quit to exit.")
    while True:
        try:
            query = input("\nYou: ").strip()
        except EOFError:
            return 0
        if query == "/quit":
            return 0
        result = router.route(query)
        clarifications = 0
        # A new user message changes the input; never repeat the unchanged query.
        while result["state"] != "answered" and result["reason"] in {
            "below_confidence_threshold", "ambiguous_labels", "insufficient_detail",
            "multiple_intents_need_clarification", "no_enabled_answer"
        } and clarifications < router.config["max_clarifications"]:
            print("\nCould you describe one specific thing you're trying to do in Pie Calendar? "
                  "Mention the feature or setting, or request a human.")
            try:
                clarified = input("You: ").strip()
            except EOFError:
                break
            if clarified == "/quit":
                return 0
            result = router.route(clarified)
            clarifications += 1
        result["clarifications_used"] = clarifications
        display(result)


def main():
    parser = argparse.ArgumentParser(prog="./csrouter", description="Local Pie Calendar support router")
    commands = parser.add_subparsers(dest="command", required=True)
    ask = commands.add_parser("ask", help="Get a static answer or human-required response")
    ask.add_argument("query")
    ask.add_argument("--json", action="store_true", help="Print the full routing decision")
    commands.add_parser("chat", help="Interactive chat with at most two clarification attempts")
    commands.add_parser("labels", help="List answer routes and enabled status")
    train = commands.add_parser("train", help="Train and calibrate from the local CSV files")
    train.add_argument("--C", type=float, default=None,
                       help="Fixed regularization; default selects 0.01 or 0.1 using calibration")
    commands.add_parser("evaluate", help="Evaluate the frozen model/policy on held-out questions")
    args = parser.parse_args()
    if args.command in {"train", "evaluate"}:
        script = "train_support.py" if args.command == "train" else "evaluate_support.py"
        arguments = ["--C", str(args.C)] if args.command == "train" and args.C is not None else []
        return subprocess.call([sys.executable, str(ROOT / "scripts" / script), *arguments])
    if args.command == "labels":
        config = load_config()
        for label, route in config["routes"].items():
            status = "enabled" if route["enabled"] else "needs more calibration examples"
            print(f"{label:25s} {status:31s} {route['title']}")
        print("human_required            always available                Human assistance")
        return 0
    router = Router()
    if args.command == "chat":
        return chat(router)
    result = router.route(args.query)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        display(result)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except (FileNotFoundError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
