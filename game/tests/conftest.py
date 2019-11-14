from typing import List, Iterator

import numpy as np
import pytest


from .data.oscillators import BEACON, BLINKER, ONE_TWO_THREE, TOAD
from .data.spaceships import GLIDER
from .data.still_lifes import BEEHIVE, BLOCK, BOAT, LOAF, TUB


def pad_frames(frames: List[np.ndarray]) -> Iterator[np.ndarray]:
    """ Pad the frames with a buffer to prevent the wrapping sides from interacting. """
    frame_shape = frames[0].shape
    new_shape = (frame_shape[0] + 4, frame_shape[1] + 4)
    injection_slice = (slice(2, -2), slice(2, -2))
    for frame in frames:
        new_frame = np.zeros(new_shape)
        new_frame[injection_slice] = frame
        yield new_frame


@pytest.fixture(name="oscillator", params=[BEACON, BLINKER, ONE_TWO_THREE, TOAD])
def _oscillator(request) -> List[np.ndarray]:
    """ Fixture which yields padded Oscillators. """
    # Pad the frames and yield.
    frames = list(pad_frames(request.param))
    yield frames


@pytest.fixture(name="spaceship", params=[GLIDER])
def _spaceship(request) -> List[np.ndarray]:
    """ Fixture which yields Spaceships. """
    # Pad the frames and yield.
    frames = list(pad_frames(request.param))
    yield frames


@pytest.fixture(name="still_life", params=[BEEHIVE, BLOCK, BOAT, LOAF, TUB])
def _still_life(request) -> List[np.ndarray]:
    """ Fixture which yields Still Lives. """
    # Pad the frames and yield.
    frames = list(pad_frames([request.param, request.param]))
    yield frames
