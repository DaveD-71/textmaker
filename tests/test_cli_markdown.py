import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from cli import normalize_markdown  # noqa: E402


def test_swp_style_tags_convert_headings_to_silent_divs():
    markdown = """---
title: Test
style_bridge:
  remove_horizontal_rules: true
---

# Unit 1: Audience

## Learning Outcomes

## Practice 1: Try It

## Speaking Task: Try It

## Learner Deliverable

### Local Subhead
"""

    result = normalize_markdown(markdown, swp_style_tags=True)

    assert '# Unit 1: Audience' not in result
    assert 'ps-heading-1: "PS Heading 1"' in result
    assert 'ps-section-head: "PS Section Head"' in result
    assert 'ps-practice-head: "PS Practice Head"' in result
    assert 'ps-speaking-task-head: "PS Speaking Task Head"' in result
    assert 'ps-learner-deliverable-head: "PS Learner Deliverable Head"' in result
    assert '::: {.ps-heading-1}\nUnit 1: Audience\n:::' in result
    assert '::: {.ps-speaking-task-head}\nSpeaking Task: Try It\n:::' in result


def test_swp_style_tags_strip_bom_before_front_matter():
    markdown = "\ufeff---\ntitle: Test\n---\n\n# Unit 1: Audience\n"

    result = normalize_markdown(markdown, swp_style_tags=True)

    assert not result.startswith("\ufeff")
    assert result.startswith("---\ntitle: Test\nstyle_map:")
    assert "\n---\n\n::: {.ps-heading-1}" in result


def test_swp_style_tags_do_not_rewrite_yaml_keys_as_labels():
    markdown = """---
title: Test
style_bridge:
  preserve_div_line_breaks: true
---

Useful terms:

Text.
"""

    result = normalize_markdown(markdown, swp_style_tags=True)

    assert "style_bridge:\n  preserve_div_line_breaks: true" in result
    assert "::: {.ps-section-label}\nUseful terms:\n:::" in result


def test_swp_style_tags_convert_quote_blocks_to_example_styles():
    markdown = """Weak opening:

> Hello. Today I will talk about many things.

Improved visual:

> Delays increased after the handoff step.
"""

    result = normalize_markdown(markdown, swp_style_tags=True)

    assert "ps-weak-example: \"PS Weak Example\"" in result
    assert "ps-improved-example: \"PS Improved Example\"" in result
    assert "::: {.ps-weak-example}\nHello. Today I will talk about many things.\n:::" in result
    assert "::: {.ps-improved-example}\nDelays increased after the handoff step.\n:::" in result
