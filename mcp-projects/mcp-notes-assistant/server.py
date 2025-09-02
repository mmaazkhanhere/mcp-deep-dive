from pathlib import Path
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="Notes Assistant MCP",
    debug=True,
    log_level="DEBUG",
    stateless_http=True
)

BASE_DIR = Path(__file__).resolve().parent
NOTES_DIR = BASE_DIR / "notes"

# It is more like a guardrail. It makes sure that the notes folder exists and is a directory.
@mcp.resource("notes://index") 
def _assert_notes_dir():
    if not NOTES_DIR.exists():
        raise ValueError("Notes folder not found")
    if not NOTES_DIR.is_dir():
        raise ValueError("Notes paths is not a directory")
    

# Returns all the notes file that are in markdown format from the folder and display in sorted order. 
def _list_md_files() -> list[Path]:
    _assert_notes_dir() # We first check if the folder is valid
    return sorted([p for p in NOTES_DIR.glob("*.md") if p.is_file()])


# Basically we are rejecting everything that is not exactly in the notes directory or something that doesn't end with md
def _safe_note_path(name: str) -> Path:
    """Reject path traversal; only allow files inside NOTES_DIR with .md suffix."""

    p = (NOTES_DIR / name).resolve()
    if p.parent != NOTES_DIR or not p.name.endswith(".md"):
        raise ValueError("Invalid note path")
    return p

# Read file as a UTF-8 text
def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _frontmatter_meta(text: str) -> dict[str, Any]:
    """
    Tiny front-matter extractor (YAML-like between --- lines).
    Returns dict with keys title, tags if present; otherwise {}
    """
    lines = text.splitlines()
    if len(lines) >= 3 and lines[0].strip() == "---":
        meta_lines = []
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                break
            meta_lines.append(lines[i])
        meta = {}
        for line in meta_lines:
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        # normalize tags to list if present like: tags: [a, b]
        if "tags" in meta:
            raw = meta["tags"]
            if raw.startswith("[") and raw.endswith("]"):
                items = [x.strip().strip(",") for x in raw[1:-1].split(",") if x.strip()]
                meta["tags"] = items
        return meta
    return {}

def _atomic_write(path: Path, text: str) -> int:
    """Write text atomically and return bytes written."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)
    return len(text.encode("utf-8"))


@mcp.resource("notes://list", mime_type="application/json")
def list_notes()->list[dict[str, Any]]:
    """
    Returns JSON array of notes wih simple metadata
    """
    items = []
    for p in _list_md_files():
        text = _read_text(p)
        meta = _frontmatter_meta(text)
        items.append({
            "name": p.name,
            "title": meta.get("title", p.name),
            "tags": meta.get("tags", []),
        })
    return items


@mcp.tool(
    name="read_note",
    description="Read a Markdown note by filename and return its raw content."
)
def read_note(name: str) -> str:
    path = _safe_note_path(name)
    return _read_text(path)

@mcp.tool(
    name="search_notes",
    description="Search notes by keyword (case-insensitive). Returns matches with a small snippet."
)
def search_notes(query: str, limit: int = 10) -> list[dict[str, Any]]:
    # requires a non-empty query
    if not query or not query.strip():
        raise ValueError("query must not be empty")
    q = query.lower()

    # Initialize results and go through all notes
    results: list[dict[str, Any]] = []
    for p in _list_md_files():
        content = _read_text(p)
        text_lc = content.lower()
        name_lc = p.name.lower()
        
        # Score matches and skip non-matches:
        score = (1 if q in name_lc else 0) + text_lc.count(q)
        if score == 0:
            continue

        # snippet around first occurrence
        idx = text_lc.find(q)
        if idx == -1:
            snippet = ""
        else:
            start = max(0, idx - 60)
            end = min(len(content), idx + 60)
            snippet = content[start:end].replace("\n", " ")

        # Pull metadata and add to results:
        meta = _frontmatter_meta(content)
        results.append({
            "name": p.name,
            "title": meta.get("title"),
            "score": score,
            "snippet": snippet.strip(),
        })

    # Sort by best score (desc), tie-break by name; return top limit
    results.sort(key=lambda r: (-r["score"], r["name"]))
    return results[:limit]

@mcp.tool(
    name="update_note",
    description=(
        "Update a Markdown note. Modes: "
        "replace (old_string -> new_string), "
        "overwrite (content replaces file), "
        "append (content added to end). "
        "Set create_if_missing=true to create the file for overwrite/append."
    ),
)
def update_note(
    name: str,
    mode: str = "replace",
    old_string: str | None = None,
    new_string: str | None = None,
    content: str | None = None,
    create_if_missing: bool = False,
) -> dict:
    """
    Update a note on disk and return a summary:
    {
      "name": "file.md",
      "mode": "replace|overwrite|append",
      "replacements": 3,
      "bytes_written": 123
    }
    """
    path = _safe_note_path(name)
    mode = mode.lower().strip()
    if mode not in {"replace", "overwrite", "append"}:
        raise ValueError("mode must be one of: replace, overwrite, append")

    # Ensure notes directory exists and file existence rules
    _assert_notes_dir()
    exists = path.exists()
    if mode == "replace" and not exists:
        raise ValueError(f"Note not found for replace: {name}")
    if mode in {"overwrite", "append"} and not exists and not create_if_missing:
        raise ValueError(
            f"Note not found: {name}. Set create_if_missing=true to create it."
        )

    bytes_written = 0
    replacements = 0

    if mode == "replace":
        if not old_string:
            raise ValueError("old_string is required for replace mode")
        if new_string is None:
            raise ValueError("new_string is required for replace mode")

        text = _read_text(path)
        replacements = text.count(old_string)
        if replacements == 0:
            # Nothing to change; return early.
            return {
                "name": path.name,
                "mode": mode,
                "replacements": 0,
                "bytes_written": 0,
                "message": "No occurrences found; file unchanged.",
            }
        updated = text.replace(old_string, new_string)
        bytes_written = _atomic_write(path, updated)

    elif mode == "overwrite":
        if content is None:
            raise ValueError("content is required for overwrite mode")
        bytes_written = _atomic_write(path, content)

    else:  # append
        if content is None:
            raise ValueError("content is required for append mode")
        # Create file if missing and allowed
        if not exists and create_if_missing:
            path.write_text("", encoding="utf-8")
        with path.open("a", encoding="utf-8") as f:
            f.write(content)
            bytes_written = len(content.encode("utf-8"))

    return {
        "name": path.name,
        "mode": mode,
        "replacements": replacements,
        "bytes_written": bytes_written,
        "message": "Note updated successfully.",
    }


mcp_app = mcp.streamable_http_app()

if __name__ == "__main__":
    mcp.run()
