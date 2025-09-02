from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="File Management MCP",
    debug=True,
    log_level="INFO",
    stateless_http=True
)

BASE_DIR = Path(__file__).resolve().parent
ALLOWED_FILES = {"data.txt, mcp.txt"}  # keep it simple & safe

def _resolve(doc_id: str) -> Path:
    """Resolve a doc_id to an allowed file within BASE_DIR."""
    p = (BASE_DIR / doc_id).resolve()
    # deny path traversal or unknown files
    if p.parent != BASE_DIR:
        raise ValueError(f"Access denied or unknown file: {doc_id}")
    return p

# It doesn't read or write file on disk but only in memory while the server runs
docs = {
    "data.txt": "This contain data related to Maaz Khan expertise",
    "mcp.txt": "This contains information about MCP"
}

@mcp.tool(
    name="read_file",
    description="This tool reads the content of the file"
)
def read_file(file_name: str) -> str:
    path = _resolve(file_name)
    try:
        return path.read_text(encoding='utf-8')
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_name}")

@mcp.tool(
    name="edit_file",
    description="This tool edits the content of the file"
)
def edit_file(file_name: str, old_content:str, new_content: str)->str:
    path = _resolve(file_name)
    if not path.exists():
        raise ValueError("File not found")
    
    content = path.read_text(encoding='utf-8')
    updated = content.replace(old_content, new_content)

    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(updated, encoding='utf-8')
    tmp.replace(path)

    return f"Successfully updated document {docs[file_name]}"

@mcp.tool(
        name="write_file",
        description="This tool writes the content of the file"""
)
def write_file(file_name: str, content: str, mode: str = "overwrite") -> str:
    path = _resolve(file_name)
    if mode not in ["overwrite", "append"]:
        raise ValueError("Invalid mode. Must be 'overwrite' or 'append'")
    if mode == "overwrite" and path.exists():
        path.write_text(content, encoding='utf-8')

    else:
        with path.open("a", encoding="utf-8") as f:
            f.write(content)

    return f"Wrote to {file_name} with mode={mode}"


@mcp.resource("docs://documents", mime_type="application/json")
def list_docs()->list[str]:
    """List allowed text files in the working directory."""
    existing = [p.name for p in BASE_DIR.glob("*.txt")]
    # Only show files that are allowed
    return [name for name in existing if name in ALLOWED_FILES]

mcp_app = mcp.streamable_http_app()

if __name__ == "__main__":
    mcp.run()
