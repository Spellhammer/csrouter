"""Render the current static-answer catalog as a reviewable Markdown file."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    config = json.loads((ROOT / "config/support/routes.json").read_text())
    lines = ["# Pie Calendar answer review", "",
             "Documentation-based answers are drafts pending product-owner approval. The license_activation referral was approved directly by the product owner.", ""]
    for label, route in config["routes"].items():
        status = "enabled" if route["enabled"] else "disabled pending more calibration evidence"
        lines += [f"## {route['title']}", "", f"Label: `{label}` | automatic response: {status} | threshold: {route['threshold']}",
                  "", route["answer"], "", "Sources:", ""]
        for source in route["sources"]:
            if source.get("url"):
                lines.append(f"- [{source['title']}]({source['url']}) (article updated {source['last_updated']})")
            else:
                lines.append(f"- {source['title']} ({source.get('provided_on', '')})")
        if route.get("handoff"):
            lines += ["", f"Future handoff: `{route['handoff']['method']}` — {route['handoff']['url']}. No message is sent by the CLI."]
        approved = route.get("review_status") == "approved_by_product_owner"
        lines += ["", "Review: approved by product owner" if approved else "Review: [ ] Answer correct for supported versions  [ ] Wording approved", ""]
    target = ROOT / "docs/support-answer-review.md"
    target.write_text("\n".join(lines) + "\n")
    print(target)


if __name__ == "__main__":
    main()
