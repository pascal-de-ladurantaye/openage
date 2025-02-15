# Copyright 2019-2022 the openage authors. See copying.md for legal info.
#
# pylint: disable=too-many-arguments

"""
Terrain definition file.
"""
from __future__ import annotations
import typing


from enum import Enum

from ..data_definition import DataDefinition

FORMAT_VERSION = '1'


class LayerMode(Enum):
    """
    Possible values for the mode of a layer.
    """
    OFF = 'off'     # layer is not animated
    LOOP = 'loop'   # animation loops indefinitely


class TerrainMetadata(DataDefinition):
    """
    Collects terrain metadata and can format it
    as a .terrain custom format
    """

    def __init__(self, targetdir: str, filename: str):
        super().__init__(targetdir, filename)

        self.scalefactor = 1.0
        self.image_files: dict[int, dict[str, typing.Any]] = {}
        self.blendtable: dict[str, typing.Any] = None
        self.layers: dict[int, dict[str, typing.Any]] = {}
        self.frames: list[dict[str, int]] = []

    def add_image(self, img_id: int, filename: str) -> None:
        """
        Add an image and the relative file name.

        :param img_id: Image identifier.
        :type img_id: int
        :param filename: Path to the image file.
        :type filename: str
        """
        self.image_files[img_id] = {
            "image_id": img_id,
            "filename": filename,
        }

    def add_layer(
        self,
        layer_id: int,
        mode: LayerMode = None,
        position: int = None,
        time_per_frame: float = None,
        replay_delay: float = None
    ) -> None:
        """
        Define a layer for the rendered texture.

        :param layer_id: Layer identifier.
        :type layer_id: int
        :param mode: Animation mode (off, loop).
        :type mode: LayerMode
        :param position: Layer position.
        :type position: int
        :param time_per_frame: Time spent on each frame.
        :type time_per_frame: float
        :param replay_delay: Time delay before replaying the animation.
        :type replay_delay: float
        """
        self.layers[layer_id] = {
            "layer_id": layer_id,
            "mode": mode,
            "position": position,
            "time_per_frame": time_per_frame,
            "replay_delay": replay_delay,
        }

    def add_frame(
        self,
        frame_idx: int,
        layer_id: int,
        img_id: int,
        xpos: int,
        ypos: int,
        xsize: int,
        ysize: int,
        priority: int,
        blend_mode: int
    ) -> None:
        """
        Add frame with all its spacial information.

        :param frame_idx: Index of the frame in the animation.
        :type frame_idx: int
        :param layer_id: ID of the layer to which the frame belongs.
        :type layer_id: int
        :param img_id: ID of the image used by this frame.
        :type img_id: int
        :param xpos: X position of the frame on the image canvas.
        :type xpos: int
        :param ypos: Y position of the frame on the image canvas.
        :type ypos: int
        :param xsize: Width of the frame.
        :type xsize: int
        :param ysize: Height of the frame.
        :type ysize: int
        :param priority: Priority for blending.
        :type priority: int
        :param blend_mode: Used for looking up the blending pattern index in the blending table.
        :type blend_mode: int
        """
        self.frames.append(
            {
                "frame_idx": frame_idx,
                "layer_id": layer_id,
                "img_id": img_id,
                "xpos": xpos,
                "ypos": ypos,
                "xsize": xsize,
                "ysize": ysize,
                "priority": priority,
                "blend_mode": blend_mode,
            }
        )

    def set_blendtable(self, table_id: int, filename: str) -> None:
        """
        Set the blendtable and the relative filename.

        :param img_id: Table identifier.
        :type img_id: int
        :param filename: Path to the blendtable file.
        :type filename: str
        """
        self.blendtable = {
            "table_id": table_id,
            "filename": filename,
        }

    def set_scalefactor(self, factor: typing.Union[int, float]) -> None:
        """
        Set the scale factor of the texture.

        :param factor: Factor by which sprite images are scaled down at default zoom level.
        :type factor: float
        """
        self.scalefactor = float(factor)

    def dump(self) -> str:
        output_str = ""

        # header
        output_str += "# openage terrain definition file\n\n"

        # version
        output_str += f"version {FORMAT_VERSION}\n\n"

        # image files
        for image in self.image_files.values():
            output_str += f"imagefile {image['image_id']} {image['filename']}\n"

        output_str += "\n"

        # blendtable reference
        output_str += f"blendtable {self.blendtable['table_id']} {self.blendtable['filename']}\n\n"

        # scale factor
        output_str += f"scalefactor {self.scalefactor}\n\n"

        # layer definitions
        for layer in self.layers.values():
            output_str += f"layer {layer['layer_id']}"

            if layer["mode"]:
                output_str += f" mode={layer['mode'].value}"

            if layer["position"]:
                output_str += f" position={layer['position']}"

            if layer["time_per_frame"]:
                output_str += f" time_per_frame={layer['time_per_frame']}"

            if layer["replay_delay"]:
                output_str += f" replay_delay={layer['replay_delay']}"

            output_str += "\n"

        output_str += "\n"

        # frame definitions
        for frame in self.frames:
            output_str += f'frame {" ".join(str(param) for param in frame.values())}\n'

        return output_str

    def __repr__(self):
        return f'TerrainMetadata<{self.filename}>'
