"""
Chunk markdown/wiki export content by heading section, not fixed token windows —
see 04-data-sources/wiki.md: "chunk by heading/section... avoid splitting a table
or a single rule description across chunks."

Recognises both ATX headings (`## Text`) and setext headings (`Text` on one line,
followed by a run of `=` for H1 or `-` for H2) — Confluence pages converted by
markdownify often use setext, and without it a whole page collapses into one chunk.
"""
import re

# Setext underline character -> heading level, per CommonMark.
_SETEXT_LEVEL = {"=": 1, "-": 2}


def _find_headings(markdown_text: str) -> list[tuple[int, int, str]]:
    """All ATX and setext headings as (char_offset, level, heading_text), sorted."""
    headings: list[tuple[int, int, str]] = []
    lines = markdown_text.split("\n")

    # Character offset of each line start, so we can slice the original text later.
    offsets: list[int] = []
    pos = 0
    for line in lines:
        offsets.append(pos)
        pos += len(line) + 1  # +1 for the newline

    for i, line in enumerate(lines):
        # ATX: `#`, `##`, ... followed by whitespace
        m = re.match(r"^(#{1,6})[ \t]+(.*)$", line)
        if m:
            headings.append((offsets[i], len(m.group(1)), m.group(2).strip()))
            continue
        # Setext: a text line whose NEXT line is a run of `=` (H1) or `-` (H2).
        if line.strip() and i + 1 < len(lines) and re.fullmatch(r"[=\-]{3,}[ \t]*", lines[i + 1]):
            underline = lines[i + 1].strip()
            lvl = _SETEXT_LEVEL["=" if underline.startswith("=") else "-"]
            headings.append((offsets[i], lvl, line.strip()))

    headings.sort(key=lambda h: h[0])
    return headings


def chunk_markdown_by_heading(markdown_text: str, min_heading_level: int = 2) -> list[dict]:
    """
    Returns [{heading, text}]. Content before the first heading of the target level
    is returned under heading="(intro)".

    Headings of level >= min_heading_level split chunks (so with the default 2, an
    H1 like the page's own title does not split); deeper (larger-number) headings are
    sub-sections that stay inside their parent chunk.
    """
    headings = _find_headings(markdown_text)
    splits = [(off, text) for off, lvl, text in headings if lvl >= min_heading_level]

    if not splits:
        return [{"heading": "(page)", "text": markdown_text.strip()}]

    chunks = []
    if splits[0][0] > 0:
        intro = markdown_text[: splits[0][0]].strip()
        if intro:
            chunks.append({"heading": "(intro)", "text": intro})

    for i, (start, heading) in enumerate(splits):
        end = splits[i + 1][0] if i + 1 < len(splits) else len(markdown_text)
        chunks.append({"heading": heading, "text": markdown_text[start:end].strip()})
    return chunks
