"""Check repository Markdown relative links without network or third-party tooling."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent


def main():
    checked = 0
    errors = []
    for path in ROOT.rglob("*.md"):
        if any(part in (".venv", ".local", ".git") for part in path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8")
        for link in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            link = link.split(' "', 1)[0].strip("<>")
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            checked += 1
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f"{path.relative_to(ROOT)}: {link}")
            elif url.fragment and target.suffix == ".md":
                headings = re.findall(r"^#{1,6}\s+(.+)$", target.read_text(encoding="utf-8"), re.MULTILINE)
                slugs = [re.sub(r"[^\w -]", "", h.lower()).replace(" ", "-") for h in headings]
                if unquote(url.fragment) not in slugs:
                    errors.append(f"{path.relative_to(ROOT)}: anchor {link}")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: {checked} internal relative Markdown links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
