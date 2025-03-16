from typing import Tuple

from debug import debugPrint
import config

def reversePos(mapped_pos: Tuple[int, int]) -> Tuple[int, int]:
    """Reverse Area Mapping

    Args:
        mapped_pos (Tuple[int, int]): Input Position after mapping

    Returns:
        Tuple[int, int]: Reversed Position
    """
    center_x = config.areaOffset[0] + config.areaSize[0] / 2
    center_y = config.areaOffset[1] + config.areaSize[1] / 2
    reversed_pos = (
        int(2 * center_x - mapped_pos[0]),
        int(2 * center_y - mapped_pos[1])
    )
    debugPrint("Pos Reversed: ", reversed_pos)
    return reversed_pos
