import math
from queue import Queue
from typing import Dict, Any

import arcade

from utils.path import MapGraph
from utils.vector import Vec2


class Canvas(arcade.Window):
    """
    Canvas which displays Vec2 objects.
    Designed as an GUI extension for AOC
    """

    def __init__(self, scale=10, margin=50, debug=False):
        super().__init__(resizable=True)
        self._vectors: Dict[Vec2, Any] = dict()
        self._fig_spr: Dict[Vec2, arcade.Sprite] = dict()

        self._sprites = arcade.SpriteList()
        self._remove_queue = Queue()

        self._input_queue = Queue()
        self._scale = scale
        self._margin = margin

        self._debug = debug
        self._debug_text = ""

    def add(self, fig: Vec2):
        self._vectors[fig] = 0

    def set(self, fig: Vec2, data: int):
        self._vectors[fig] = data

    def remove(self, fig: Vec2):
        # remove from update and drawing first
        del self._vectors[fig]

        # Remove private information and sprites
        if fig in self._fig_spr:
            spr: arcade.Sprite = self._fig_spr.get(fig)
            self._remove_queue.put(spr)
            del self._fig_spr[fig]

    def create_new_sprite(self, fig: Vec2):
        return arcade.Sprite()

    def get_key_event(self):
        return self._input_queue.get()

    def on_key_press(self, symbol: int, modifiers: int):
        self._input_queue.put(symbol)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        left, right, bottom, top = self.get_viewport()
        x = math.ceil((x - right) / self._scale)
        y = math.ceil((y - bottom) / self._scale)
        self._debug_text = f"Mouse at {x=}{y=}"

    def on_update(self, delta_time: float):
        while not self._remove_queue.empty():
            rem: arcade.Sprite = self._remove_queue.get_nowait()
            rem.remove_from_sprite_lists()

        for fig, tex in list(self._vectors.items()):
            spr = self._fig_spr.get(fig)

            if spr is None:
                spr = self.create_new_sprite(fig)
                self._fig_spr[fig] = spr
                self._sprites.append(spr)
            self.sprite_update(fig, spr, tex)

    def sprite_update(self, vec: Vec2, spr: arcade.Sprite, tex: int):
        """
        Updates pos, and tex_index
        """
        spr.center_x = vec.x * self._scale
        spr.center_y = vec.y * self._scale
        spr.set_texture(tex)

        spr.width = self._scale
        spr.height = self._scale

    def on_draw(self):
        """
        Draws internal sprite list
        """
        arcade.start_render()
        self._sprites.draw()

        self.draw_textures()

        self.apply_margine()

        if self._debug_text:
            left, right, bottom, top = self.get_viewport()
            arcade.draw_text(
                self._debug_text, left + 10, bottom + 5, color=arcade.color.RED
            )

    def apply_margine(self):
        min_x, max_x = 0, 0
        min_y, max_y = 0, 0
        for sprite in self._sprites:
            min_x = min(sprite.center_x, min_x)
            max_x = max(sprite.center_x, max_x)
            min_y = min(sprite.center_y, min_y)
            max_y = max(sprite.center_y, max_y)
        margin = self._margin
        # self.set_viewport(min_x - margin, max_x + margin, max_y + margin, min_y - margin)
        self.set_viewport(
            min_x - margin, max_x + margin, min_y - margin, max_y + margin
        )

    def draw_textures(self):
        """
        Overwrite this method to draw textures while on_draw.
        """
        pass


class MapDisplay(arcade.Window):
    """
    WIP
    Visualize a MapGraph, provide easy addable actions to triger updates or simulation ticks.
    """

    def __init__(self, graph: MapGraph):
        self.graph = graph
        self.sprites = arcade.SpriteList()

    def on_update(self, dt):
        pass

    def on_draw(self):
        """
        Draws internal sprite list
        """
        arcade.start_render()
        self._sprites.draw()

        self.draw_textures()

        self.apply_margine()

        if self._debug_text:
            left, right, bottom, top = self.get_viewport()
            arcade.draw_text(
                self._debug_text, left + 10, bottom + 5, color=arcade.color.RED
            )
