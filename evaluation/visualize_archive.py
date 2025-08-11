# evaluation/visualize_archive.py
from __future__ import annotations

from datetime import datetime, UTC
from pathlib import Path

try:
    import svgwrite  # type: ignore
except Exception:
    svgwrite = None  # allow import to succeed even if svgwrite isn't installed


def draw_phase_lattice(filename: str | None = None) -> str:
    """
    Minimal SVG lattice with proper arrow markers (func IRI).
    Returns the output path as a string.
    """
    ts = datetime.now(UTC).isoformat().replace(":", "-")
    outfile = filename or f"phase_lattice_{ts}.svg"
    outpath = Path(outfile)

    if svgwrite is None:
        # Fallback: write a basic SVG so callers still get a file.
        outpath.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="120">'
            '<rect x="0" y="0" width="320" height="120" fill="white" stroke="black"/>'
            '<text x="12" y="24">phase lattice (svgwrite missing)</text>'
            "</svg>",
            encoding="utf-8",
        )
        return str(outpath)

    dwg = svgwrite.Drawing(str(outpath), size=("480px", "200px"))

    # Define arrow and reference via func IRI
    arrow = dwg.marker(id="arrow", insert=(6, 3), size=(10, 10), orient="auto")
    arrow.add(dwg.path(d="M0,0 L0,6 L9,3 z"))
    dwg.defs.add(arrow)

    nodes = {
        "ALIVE": (60, 40),
        "JAM":   (200, 40),
        "MEM":   (60, 120),
        "VAC":   (200, 120),
    }
    for label, (x, y) in nodes.items():
        dwg.add(dwg.rect(insert=(x-28, y-18), size=(56, 36), fill="white", stroke="black"))
        dwg.add(dwg.text(label, insert=(x-22, y+5), font_size="14px"))

    def edge(a: str, b: str):
        (x1, y1) = nodes[a]
        (x2, y2) = nodes[b]
        dwg.add(
            dwg.line(
                start=(x1 + 28, y1),
                end=(x2 - 28, y2),
                stroke="black",
                stroke_width=2,
                marker_end=arrow.get_funciri(),  # <- correct use
            )
        )

    edge("ALIVE", "JAM")
    edge("ALIVE", "MEM")
    edge("JAM", "VAC")
    edge("MEM", "VAC")

    dwg.save()
    return str(outpath)
