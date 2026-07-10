"""Turn a black-and-white image into a 3D-printable stamp (STL).

A stamp works in reverse of a normal print: the raised parts of the surface
are what pick up paint and transfer it to paper. So the dark regions of the
input image become the raised relief, everything else stays flush with the
base plate, and the design is mirrored left-to-right so the *stamped* result
reads the same way as the original image.

The generated mesh is a watertight, per-pixel "stepped" heightmap: a flat base
plate with vertical-walled relief rising out of it, which prints cleanly
without supports.
"""

from __future__ import annotations

import argparse
import struct
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image


@dataclass
class StampConfig:
    """Physical parameters for the generated stamp, all in millimetres."""

    width_mm: float = 60.0
    """Target width of the stamp footprint. Height follows the image aspect."""

    base_thickness: float = 3.0
    """Thickness of the solid backing plate under the whole stamp."""

    relief_height: float = 2.5
    """How far the inked design rises above the base plate."""

    threshold: int = 128
    """Grayscale cutoff (0-255). Pixels darker than this become relief."""

    invert: bool = False
    """Treat light pixels as the design instead of dark ones."""

    mirror: bool = True
    """Flip left-right so the printed impression matches the source image."""

    max_pixels: int = 400
    """Longest edge is downsampled to at most this many pixels."""


def load_mask(image_path: str | Path, config: StampConfig) -> np.ndarray:
    """Load an image and return a boolean mask where True == raised design."""
    img = Image.open(image_path).convert("L")
    img = _downsample(img, config.max_pixels)
    if config.mirror:
        img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    pixels = np.asarray(img, dtype=np.uint8)
    # Dark pixels (below threshold) are the design that carries paint.
    mask = pixels < config.threshold
    if config.invert:
        mask = ~mask
    return mask


def _downsample(img: Image.Image, max_pixels: int) -> Image.Image:
    """Shrink the image so its longest edge is at most ``max_pixels``."""
    longest = max(img.size)
    if longest <= max_pixels:
        return img
    scale = max_pixels / longest
    new_size = (max(1, round(img.width * scale)), max(1, round(img.height * scale)))
    return img.resize(new_size, Image.Resampling.LANCZOS)


def heightmap_from_mask(mask: np.ndarray, config: StampConfig) -> np.ndarray:
    """Build a per-pixel top-surface height array from the design mask."""
    heights = np.full(mask.shape, config.base_thickness, dtype=np.float64)
    heights[mask] += config.relief_height
    return heights


def _stamp_triangles(heights: np.ndarray, pixel_size: float) -> np.ndarray:
    """Build a watertight triangle mesh (N, 3, 3) from a stepped heightmap.

    Each pixel is a flat-topped column standing on a shared base plate. Faces
    are emitted for the tops, the single flat bottom, the outer walls, and the
    vertical steps wherever two neighbouring pixels differ in height.
    """
    rows, cols = heights.shape
    tris: list[list[tuple[float, float, float]]] = []

    def quad(a, b, c, d):
        # Two triangles for a planar quad, wound a->b->c and a->c->d.
        tris.append([a, b, c])
        tris.append([a, c, d])

    # X runs along columns, Y along rows. Flip Y so image-row-0 sits at the
    # back and the model is right-side-up in the printer's coordinate frame.
    def px(x):
        return x * pixel_size

    def py(y):
        return (rows - y) * pixel_size

    # Top and bottom face of every pixel. Keeping the bottom per-pixel (rather
    # than one big quad) means its edges line up with the per-pixel walls, so
    # the mesh stays watertight with no T-junctions.
    for y in range(rows):
        for x in range(cols):
            z = heights[y, x]
            quad(
                (px(x), py(y), z),
                (px(x + 1), py(y), z),
                (px(x + 1), py(y + 1), z),
                (px(x), py(y + 1), z),
            )
            # Bottom of the same column, wound the other way for a -Z normal.
            quad(
                (px(x), py(y), 0.0),
                (px(x), py(y + 1), 0.0),
                (px(x + 1), py(y + 1), 0.0),
                (px(x + 1), py(y), 0.0),
            )

    # Vertical walls: outer border plus interior steps between differing heights.
    for y in range(rows):
        for x in range(cols):
            h = heights[y, x]
            # Left edge (neighbour at x-1).
            hl = heights[y, x - 1] if x > 0 else 0.0
            if h > hl:
                quad(
                    (px(x), py(y), hl),
                    (px(x), py(y + 1), hl),
                    (px(x), py(y + 1), h),
                    (px(x), py(y), h),
                )
            # Right edge (neighbour at x+1).
            hr = heights[y, x + 1] if x < cols - 1 else 0.0
            if h > hr:
                quad(
                    (px(x + 1), py(y), h),
                    (px(x + 1), py(y + 1), h),
                    (px(x + 1), py(y + 1), hr),
                    (px(x + 1), py(y), hr),
                )
            # Back edge (neighbour at y-1).
            hb = heights[y - 1, x] if y > 0 else 0.0
            if h > hb:
                quad(
                    (px(x), py(y), h),
                    (px(x + 1), py(y), h),
                    (px(x + 1), py(y), hb),
                    (px(x), py(y), hb),
                )
            # Front edge (neighbour at y+1).
            hf = heights[y + 1, x] if y < rows - 1 else 0.0
            if h > hf:
                quad(
                    (px(x), py(y + 1), hf),
                    (px(x + 1), py(y + 1), hf),
                    (px(x + 1), py(y + 1), h),
                    (px(x), py(y + 1), h),
                )

    return np.asarray(tris, dtype=np.float32)


def _triangle_normals(triangles: np.ndarray) -> np.ndarray:
    """Compute a unit normal per triangle."""
    v0, v1, v2 = triangles[:, 0], triangles[:, 1], triangles[:, 2]
    normals = np.cross(v1 - v0, v2 - v0)
    lengths = np.linalg.norm(normals, axis=1, keepdims=True)
    lengths[lengths == 0] = 1.0
    return normals / lengths


def write_binary_stl(path: str | Path, triangles: np.ndarray) -> None:
    """Write triangles (N, 3, 3) to a binary STL file."""
    triangles = np.asarray(triangles, dtype=np.float32)
    normals = _triangle_normals(triangles).astype(np.float32)
    count = triangles.shape[0]
    with open(path, "wb") as fh:
        fh.write(b"\x00" * 80)  # 80-byte header, conventionally left blank.
        fh.write(struct.pack("<I", count))
        for i in range(count):
            fh.write(struct.pack("<3f", *normals[i]))
            for vertex in triangles[i]:
                fh.write(struct.pack("<3f", *vertex))
            fh.write(struct.pack("<H", 0))  # attribute byte count.


def image_to_stamp_stl(
    image_path: str | Path,
    stl_path: str | Path,
    config: StampConfig | None = None,
) -> np.ndarray:
    """Convert a black-and-white image into an STL stamp file.

    Returns the triangle array so callers/tests can inspect the mesh.
    """
    config = config or StampConfig()
    mask = load_mask(image_path, config)
    if not mask.any():
        raise ValueError(
            "No design pixels found. Check the --threshold, or try --invert "
            "if your image has a light design on a dark background."
        )
    cols = mask.shape[1]
    pixel_size = config.width_mm / cols
    heights = heightmap_from_mask(mask, config)
    triangles = _stamp_triangles(heights, pixel_size)
    write_binary_stl(stl_path, triangles)
    return triangles


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a 3D-printable stamp (STL) from a black-and-white image.",
    )
    parser.add_argument("image", help="Path to the input black-and-white image.")
    parser.add_argument(
        "-o",
        "--output",
        help="Output STL path (defaults to the image name with a .stl suffix).",
    )
    defaults = StampConfig()
    parser.add_argument("--width", type=float, default=defaults.width_mm, help="Stamp width in mm.")
    parser.add_argument(
        "--base", type=float, default=defaults.base_thickness, help="Base plate thickness in mm."
    )
    parser.add_argument(
        "--relief", type=float, default=defaults.relief_height, help="Relief height in mm."
    )
    parser.add_argument(
        "--threshold", type=int, default=defaults.threshold, help="Grayscale threshold (0-255)."
    )
    parser.add_argument(
        "--invert", action="store_true", help="Use light pixels as the design instead of dark."
    )
    parser.add_argument(
        "--no-mirror",
        action="store_true",
        help="Do not mirror the design (the impression will be reversed).",
    )
    parser.add_argument(
        "--max-pixels",
        type=int,
        default=defaults.max_pixels,
        help="Downsample so the longest edge is at most this many pixels.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = args.output or str(Path(args.image).with_suffix(".stl"))
    config = StampConfig(
        width_mm=args.width,
        base_thickness=args.base,
        relief_height=args.relief,
        threshold=args.threshold,
        invert=args.invert,
        mirror=not args.no_mirror,
        max_pixels=args.max_pixels,
    )
    triangles = image_to_stamp_stl(args.image, output, config)
    print(f"Wrote {output} ({len(triangles)} triangles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
