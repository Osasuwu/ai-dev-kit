"""Markdown paragraphs and their links, as the link check reads them.

Split out of the removed quote check: a doc body is split into paragraphs outside code
fences and HTML comments, and each paragraph's link targets and bare URLs are listed.
"""

from __future__ import annotations

import re

# [text](url) or [text](url "title"); the url may hold one level of parentheses.
_LINK_RE = re.compile(r"\[([^\]]*)\]\(((?:[^()\s]|\([^()\s]*\))+)(?:\s+\"[^\"]*\")?\)")
_BARE_URL_RE = re.compile(r"https?://[^\s)>\]`\"]+")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+")
_BLOCKQUOTE_RE = re.compile(r"^\s*(?:>\s?)+")
# An HTML comment; it never runs past a blank line, so a stray "<!--" hides one paragraph at most.
_COMMENT_RE = re.compile(r"<!--(?:(?!\n\s*\n).)*?-->", re.S)


def _strip_frontmatter(lines: list[str]) -> int:
    """Return the index of the first body line."""
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return i + 1
    return 0


def _paragraphs(text: str) -> list[tuple[int, str]]:
    """Split the body into (first line number, joined text); code fences are dropped.

    A blank line, a heading, a table row or a new list item starts a new paragraph.
    """
    lines = _body_lines(text)
    out: list[tuple[int, str]] = []
    buf: list[str] = []
    start = 0
    fence = ""  # the marker that opened the current fence; only the same one closes it

    def flush() -> None:
        if buf:
            out.append((start, " ".join(s.strip() for s in buf)))
            buf.clear()

    for i in range(_strip_frontmatter(lines), len(lines)):
        line = lines[i]
        opener = _FENCE_RE.match(line)
        if opener and (not fence or opener.group(1) == fence):
            flush()
            fence = "" if fence else opener.group(1)
            continue
        if fence:
            continue
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        if stripped.startswith(("#", "|")) or _LIST_ITEM_RE.match(line):
            flush()
            start = i + 1
            buf.append(line)
            if stripped.startswith(("#", "|")):
                flush()
            continue
        if not buf:
            start = i + 1
        buf.append(line)
    flush()
    return out


def _body_lines(text: str) -> list[str]:
    """The doc's lines with HTML comments blanked and blockquote markers removed."""
    return [
        _BLOCKQUOTE_RE.sub("", line)
        for line in _COMMENT_RE.sub(_blank, text).splitlines()
    ]


def _blank(match: re.Match) -> str:
    """An HTML comment becomes blank lines, so line numbers stay right."""
    return "\n" * match.group(0).count("\n")


def _urls(paragraph: str) -> tuple[str, ...]:
    """Markdown link targets, then bare URLs, in order."""
    urls = tuple(
        url for _, url in _LINK_RE.findall(paragraph) if not url.startswith("#")
    )
    bare = _BARE_URL_RE.findall(_LINK_RE.sub("", paragraph))
    return urls + tuple(u.rstrip(".,;:") for u in bare)


def paragraphs(text: str) -> list[tuple[int, str, tuple[str, ...]]]:
    """(first line number, joined text, links) for each body paragraph; code fences are dropped."""
    return [(line, para, _urls(para)) for line, para in _paragraphs(text)]
