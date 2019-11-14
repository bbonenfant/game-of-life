from typing import Iterator, Optional, Tuple

import numpy as np
from numpy import count_nonzero
from scipy.ndimage.filters import generic_filter


class Board:
    """ A board of cells. """

    def __init__(self, width: int, height: int, *, seed: Optional[int] = None):
        """
        :param width: The width of the board (in number of cells).
        :param height: The height of the board (in number of cells).
        :param seed: A seed to the random number generator used by numpy.
        """
        self.width = width
        self.height = height
        self.shape = (self.width, self.height)

        # Seed the App.
        np.random.seed(seed)

        self.board = self.generate_board(self.shape)

    @property
    def alive(self) -> Iterator[Tuple[int, int]]:
        """ Yields the indices, (x, y), of the cells which are alive. """
        yield from zip(*self.board.nonzero())

    @staticmethod
    def generate_board(shape: Tuple[int, int]) -> np.ndarray:
        """ Generate a random board ("seed" in the Game of Life terminology). """
        return np.random.choice([False, True], shape)

    def new(self):
        """ Set the board to a random new game (set a new "seed"). """
        self.board = self.generate_board(self.shape)

    def update(self):
        """ Update the board to the next generation. """
        window_size = (3, 3)
        center = np.prod(window_size) // 2

        def alive(neighborhood: np.ndarray):
            """
                Determine if a cell at the center of the specified neighborhood is alive next generation.
            :param neighborhood: A 1D array of the points that describe a neighborhood of cells,
                                    with the cell in question at the center of this array.
            :return determination:
            """
            # If the cell is not alive, then it will only become alive if the score is 3.
            # If the center cell is alive, it will remain alive if neither over- nor under-populated.
            return count_nonzero(neighborhood) == 3 if not neighborhood[center] else 2 < count_nonzero(neighborhood) < 5

        self.board = generic_filter(self.board, alive, size=window_size, mode='wrap')
