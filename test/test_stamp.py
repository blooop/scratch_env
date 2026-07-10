import shutil
import struct
import tempfile
from pathlib import Path
from unittest import TestCase

import numpy as np
from PIL import Image

from python_template.stamp import (
    StampConfig,
    heightmap_from_mask,
    image_to_stamp_stl,
    load_mask,
    write_binary_stl,
    _stamp_triangles,
    _triangle_normals,
)


def _read_binary_stl(path):
    """Return (triangle_count, triangles) from a binary STL file."""
    with open(path, "rb") as fh:
        fh.read(80)
        (count,) = struct.unpack("<I", fh.read(4))
        tris = []
        for _ in range(count):
            fh.read(12)  # normal
            verts = [struct.unpack("<3f", fh.read(12)) for _ in range(3)]
            fh.read(2)  # attribute byte count
            tris.append(verts)
    return count, np.asarray(tris, dtype=np.float32)


class TestStamp(TestCase):
    def _write_image(self, array_uint8):
        path = Path(self.tmpdir) / "img.png"
        Image.fromarray(array_uint8, mode="L").save(path)
        return path

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_heightmap_levels(self):
        mask = np.array([[True, False], [False, True]])
        config = StampConfig(base_thickness=3.0, relief_height=2.0)
        heights = heightmap_from_mask(mask, config)
        self.assertEqual(heights[0, 0], 5.0)
        self.assertEqual(heights[0, 1], 3.0)
        self.assertEqual(heights[1, 1], 5.0)

    def test_mask_dark_is_design(self):
        # Left column black (0), right column white (255).
        array = np.array([[0, 255], [0, 255]], dtype=np.uint8)
        img_path = self._write_image(array)
        # mirror flips left-right, so the black column lands on the right.
        mask = load_mask(img_path, StampConfig(mirror=True))
        self.assertTrue(mask[:, 1].all())
        self.assertFalse(mask[:, 0].any())

    def test_invert(self):
        array = np.array([[0, 255]], dtype=np.uint8)
        img_path = self._write_image(array)
        normal = load_mask(img_path, StampConfig(mirror=False, invert=False))
        inverted = load_mask(img_path, StampConfig(mirror=False, invert=True))
        np.testing.assert_array_equal(normal, ~inverted)

    def test_single_raised_pixel_mesh_is_a_box(self):
        # One pixel, raised: top(2) + bottom(2) + 4 walls(2 each) = 12 triangles.
        heights = np.array([[5.0]])
        tris = _stamp_triangles(heights, pixel_size=1.0)
        self.assertEqual(tris.shape, (12, 3, 3))
        # Box spans the full relief height.
        self.assertAlmostEqual(tris[:, :, 2].max(), 5.0)
        self.assertAlmostEqual(tris[:, :, 2].min(), 0.0)

    def test_normals_are_unit_length(self):
        heights = np.array([[3.0, 5.0], [5.0, 3.0]])
        tris = _stamp_triangles(heights, pixel_size=2.0)
        normals = _triangle_normals(tris)
        lengths = np.linalg.norm(normals, axis=1)
        np.testing.assert_allclose(lengths, 1.0, atol=1e-5)

    def test_end_to_end_writes_valid_stl(self):
        array = np.array(
            [[0, 0, 255], [255, 0, 255], [0, 0, 0]],
            dtype=np.uint8,
        )
        img_path = self._write_image(array)
        stl_path = Path(self.tmpdir) / "stamp.stl"
        config = StampConfig(width_mm=30.0, base_thickness=2.0, relief_height=1.5)
        triangles = image_to_stamp_stl(img_path, stl_path, config)

        count, read_tris = _read_binary_stl(stl_path)
        self.assertEqual(count, len(triangles))
        self.assertGreater(count, 0)
        # Footprint width should match the requested physical width.
        self.assertAlmostEqual(read_tris[:, :, 0].max(), 30.0, places=3)
        # Tallest point = base + relief.
        self.assertAlmostEqual(read_tris[:, :, 2].max(), 3.5, places=3)

    def test_blank_image_raises(self):
        array = np.full((3, 3), 255, dtype=np.uint8)
        img_path = self._write_image(array)
        stl_path = Path(self.tmpdir) / "blank.stl"
        with self.assertRaises(ValueError):
            image_to_stamp_stl(img_path, stl_path, StampConfig())

    def test_write_binary_stl_roundtrip(self):
        tris = np.array(
            [[[0, 0, 0], [1, 0, 0], [0, 1, 0]]],
            dtype=np.float32,
        )
        stl_path = Path(self.tmpdir) / "tri.stl"
        write_binary_stl(stl_path, tris)
        count, read_tris = _read_binary_stl(stl_path)
        self.assertEqual(count, 1)
        np.testing.assert_allclose(read_tris, tris)
