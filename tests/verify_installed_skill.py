import argparse
from pathlib import Path


REQUIRED = [
    "SKILL.md",
    "pasadu.md",
    "agents/openai.yaml",
    "reference/law/prb60.md",
    "reference/law/rbb60.md",
    "reference/law/rbb60-3.md",
    "scripts/pasadu/evidence_packet.py",
    "data/index/chunks.json",
    "data/release.json",
]

FORBIDDEN = ["tests", "evals", "docs", "how2agent", ".codex", ".claude", ".gemini"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()

    skill_dir = args.skill_dir.resolve()
    missing = [path for path in REQUIRED if not (skill_dir / path).is_file()]
    unexpected = [path for path in FORBIDDEN if (skill_dir / path).exists()]

    if missing or unexpected:
        if missing:
            print("Missing:", ", ".join(missing))
        if unexpected:
            print("Unexpected:", ", ".join(unexpected))
        raise SystemExit(1)

    print(f"PASADU_INSTALL_VERIFIED: {skill_dir}")


if __name__ == "__main__":
    main()
