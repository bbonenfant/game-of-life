from typing import List

import numpy as np

from ..model import Board


class TestGameOfLife:
    """ Test some simple games to ensure that the expected progression of generations works. """

    @staticmethod
    def initialize_board(frames: List[np.ndarray]) -> Board:
        """ Initialize a board with the first frame of the provided frames. """
        # Construct the board, initialed as the first frame.
        frame_shape = frames[0].shape
        game = Board(*frame_shape)
        game.board = frames[0]
        return game

    def test_oscillators(self, oscillator):
        """ Test the Oscillators. """
        # Arrange
        game = self.initialize_board(oscillator)

        # Act & Assert
        for frame in oscillator:
            np.testing.assert_equal(game.board, frame)
            game.update()

    def test_spaceships(self, spaceship):
        """ Test the Spaceships. """
        # Arrange
        game = self.initialize_board(spaceship)

        # Act & Assert
        for frame in spaceship:
            np.testing.assert_equal(game.board, frame)
            game.update()

    def test_still_lives(self, still_life):
        """ Test the Still Lives. """
        # Arrange
        game = self.initialize_board(still_life)

        # Act & Assert
        for frame in still_life:
            np.testing.assert_equal(game.board, frame)
            game.update()