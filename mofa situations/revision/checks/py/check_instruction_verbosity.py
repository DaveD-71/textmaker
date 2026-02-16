import argparse
import re
from pathlib import Path

import yaml


WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")
TOKEN_RE = re.compile(r"[a-z]+")
STOPWORDS = {
    "a",
    "about",
    "after",
    "all",
    "also",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "clear",
    "clearly",
    "for",
    "from",
    "give",
    "have",
    "if",
    "in",
    "is",
    "it",
    "its",
    "may",
    "must",
    "need",
    "of",
    "on",
    "or",
    "other",
    "please",
    "polite",
    "roleplay",
    "simple",
    "should",
    "task",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "they",
    "this",
    "to",
    "up",
    "use",
    "using",
    "visitor",
    "visitors",
    "with",
    "write",
    "you",
    "your",
}


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text or ""))


def tokens(text: str) -> set[str]:
    values = TOKEN_RE.findall((text or "").lower())
    return {t for t in values if len(t) > 2 and t not in STOPWORDS}


def overlap_ratio(source: str, reference: str) -> float:
    src = tokens(source)
    ref = tokens(reference)
    if not src:
        return 0.0
    return len(src & ref) / len(src)


def get_roleplay_prompt(roleplays: list[dict], roleplay_id: int) -> str:
    for item in roleplays or []:
        if item.get("id") == roleplay_id:
            return (((item.get("prompt") or {}).get("en")) or "").strip()
    return ""


def status_from_signals(activity: str, wc: int, purpose_score: float, linkage_issues: list[str]) -> str:
    # We only evaluate prompts over 100 words by design.
    if linkage_issues:
        return "Likely unnecessary (long + linkage issue)"
    if purpose_score < 0.10:
        return "Likely unnecessary (long + weak purpose/objective alignment)"
    if wc >= 140 and purpose_score < 0.16:
        return "Possibly unnecessary (very long for current alignment)"
    return "Long but likely necessary"


def build_report(input_yaml: Path, output_txt: Path, min_words: int) -> None:
    data = yaml.safe_load(input_yaml.read_text(encoding="utf-8"))
    situations = data.get("situations") or {}

    lines = [
        "Instruction Verbosity + Linkage Check",
        f"Source: {input_yaml.as_posix()}",
        "Scope: roleplay 1, roleplay 2, writing task instruction prompts (English)",
        f"Filter: only prompts with >= {min_words} words",
        "",
        "Rules checked:",
        "1) Output activities should align with purpose/objectives.",
        "2) Writing task should follow Roleplay 1, not Roleplay 2.",
        "3) Roleplay model should match Roleplay 1 (not Roleplay 2).",
        "4) Writing model should match writing task instructions.",
        "",
        "Format: ID | Activity | Words | PurposeScore | RP1vsRP2 | ModelLink | Status | Notes",
        "",
    ]

    flagged = 0
    scanned_long = 0

    for sid, block in situations.items():
        details = block.get("details") or {}
        purpose = ((details.get("purpose") or {}).get("en") or "").strip()
        objectives = ((details.get("objectives") or {}).get("en") or "").strip()
        purpose_objectives = f"{purpose} {objectives}".strip()

        instructions = block.get("instructions") or {}
        roleplays = instructions.get("roleplays") or []
        rp1 = get_roleplay_prompt(roleplays, 1)
        rp2 = get_roleplay_prompt(roleplays, 2)
        wt = (((instructions.get("writing_task") or {}).get("prompt") or {}).get("en") or "").strip()

        language = block.get("language") or {}
        rp1_model = (((language.get("roleplay_1") or {}).get("model") or {}).get("dialogue") or "").strip()
        wt_model = (((language.get("writing_task") or {}).get("model") or {}).get("text") or "").strip()

        model_rp1_to_rp1 = overlap_ratio(rp1_model, rp1)
        model_rp1_to_rp2 = overlap_ratio(rp1_model, rp2)
        model_wt_to_wt = overlap_ratio(wt_model, wt)

        activities = [("Roleplay 1", rp1), ("Roleplay 2", rp2), ("Writing Task", wt)]
        for activity_name, prompt in activities:
            wc = word_count(prompt)
            if wc < min_words:
                continue
            scanned_long += 1

            purpose_score = overlap_ratio(prompt, purpose_objectives)
            rp1_link = overlap_ratio(prompt, rp1)
            rp2_link = overlap_ratio(prompt, rp2)
            rp1_vs_rp2 = f"{rp1_link:.3f}/{rp2_link:.3f}"

            linkage_issues: list[str] = []
            if activity_name == "Writing Task":
                if rp1_link <= rp2_link:
                    linkage_issues.append("writing task appears at least as close to RP2 as RP1")
                if model_wt_to_wt < 0.12:
                    linkage_issues.append("writing model appears weakly aligned to writing task")
                model_link = f"WT model={model_wt_to_wt:.3f}"
            elif activity_name == "Roleplay 1":
                if model_rp1_to_rp1 <= model_rp1_to_rp2:
                    linkage_issues.append("roleplay model appears at least as close to RP2 as RP1")
                model_link = f"RP1 model={model_rp1_to_rp1:.3f}/{model_rp1_to_rp2:.3f}"
            else:
                model_link = "N/A"

            status = status_from_signals(activity_name, wc, purpose_score, linkage_issues)
            notes = "; ".join(linkage_issues) if linkage_issues else "No linkage issues triggered."
            if status.startswith("Likely unnecessary") or status.startswith("Possibly unnecessary"):
                flagged += 1

            lines.append(
                f"{sid} | {activity_name} | {wc} | {purpose_score:.3f} | {rp1_vs_rp2} | "
                f"{model_link} | {status} | {notes}"
            )

    lines.extend(
        [
            "",
            f"Long prompts scanned: {scanned_long}",
            f"Likely/Possibly unnecessary candidates: {flagged}",
        ]
    )
    output_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check verbosity and linkage of situation task instructions.")
    parser.add_argument(
        "--input",
        default="mofa situations/text/Situations_all.yaml",
        help="Path to Situations_all.yaml",
    )
    parser.add_argument(
        "--output",
        default="mofa situations/checks/instruction_verbosity_linkage_check.txt",
        help="Output report path",
    )
    parser.add_argument(
        "--min-words",
        type=int,
        default=100,
        help="Only evaluate prompts with at least this many words",
    )
    args = parser.parse_args()

    input_yaml = Path(args.input)
    output_txt = Path(args.output)
    build_report(input_yaml=input_yaml, output_txt=output_txt, min_words=args.min_words)
    print(f"Wrote: {output_txt}")


if __name__ == "__main__":
    main()
