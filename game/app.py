from sys import exit
from time import sleep, time
from typing import Any, Callable, Optional

from pyglet.gl import *
from pyglet.graphics import Batch
from pyglet.window import Window, key

from .model import Board


def set_framerate(rate: float) -> Callable:
    """ Set the framerate for a function. """
    frame_interval = 1 / rate if rate > 0 else 0.03

    def limiter(func: Callable) -> Callable:
        """ Initialize the limiter. """
        last = time()

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """ Perform the limiting. """
            nonlocal last

            # Perform the frame limiting.
            last, timestep = time(), time() - last
            sleep_time = 0 if timestep > frame_interval else frame_interval - timestep
            sleep(sleep_time)

            # Call the function.
            return func(*args, **kwargs)
        return wrapper
    return limiter


# noinspection PyAbstractClass
class App(Window):
    """ The applet which runs Conway's Game of Life. """
    box_size = 6  # in pixels.

    def __init__(self, width: int = 200, height: int = 120, *, seed: Optional[int] = None):
        """
        :param width: The width of the board (in number of cells).
        :param height: The height of the board (in number of cells).
        :param seed: A seed to the random number generator used by numpy.
        """
        self._window_size = ((width + 1) * self.box_size, (height + 1) * self.box_size)
        super().__init__(*self._window_size)
        self.board = Board(width, height, seed=seed)

    def on_key_press(self, symbol, modifiers):
        """ Use the SPACE key as a quick reset button. """
        if symbol & key.SPACE:
            self.board.new()
        if symbol & key.ESCAPE:
            self.on_close()

    def on_close(self):
        """ Close the window gracefully. """
        exit()

    def render(self):
        """ Render the board onto the screen. """
        # Clear the old board.
        self.clear()

        # Draw the board in a single batch.
        batch = Batch()
        batch = self.draw_board(batch)
        batch.draw()

        # Send to screen.
        self.flip()

    def draw_board(self, batch: Batch) -> Batch:
        """ Draw the game board (in a single batch). """
        delta = (self.box_size // 2) - 1
        offset = self.box_size

        def construct_cell(x: int, y: int):
            """ Returns the coordinates of a box centered at (x, y). """
            x, y = (x + 1) * offset, (y + 1) * offset
            return (
                x + delta, y + delta,
                x, y + delta,
                x, y,
                x + delta, y,
            )

        # Construct all the cells in one batch.
        cell_coords = [coord for x_index, y_index in self.board.alive for coord in construct_cell(x_index, y_index)]
        cell_count = len(cell_coords) // 2
        indices = range(cell_count)

        batch.add_indexed(cell_count, GL_QUADS, None, indices, ('v2i', cell_coords))
        return batch

    def run(self):
        """ Run the application in manual mode. """
        @set_framerate(2000)
        def run_():
            """ Run in a help function to limit framerate. """
            self.render()
            self.dispatch_events()
            self.board.update()

        while True:
            run_()
