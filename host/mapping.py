from typing import Tuple

def locationMapping(
    input: Tuple[int, int], 
    inputSize: Tuple[int, int], 
    outputSize: Tuple[int, int], 
    offset: Tuple[int, int] = (0, 0)
) -> Tuple[int, int]:
    """Map tablet position to screen position base on config

    Args:
        input (Tuple[int, int]): Raw Pos from Tablet
        inputSize (Tuple[int, int]): Tablet Size
        outputSize (Tuple[int, int]): Screen Area Size
        offset (Tuple[int, int], optional): Area Offset. Defaults to (0, 0).

    Returns:
        Tuple[int, int]: Mapped Position
    """
    return (
        (int(input[0] / inputSize[0] * outputSize[0]) + offset[0]), 
        (int(input[1] / inputSize[1] * outputSize[1]) + offset[1])
    )
