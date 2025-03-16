from typing import Tuple

def locationMapping(
    input: Tuple[int, int], 
    inputSize: Tuple[int, int], 
    outputSize: Tuple[int, int], 
    offset: Tuple[int, int] = (0, 0)
):
    return (
        (int(input[0] / inputSize[0] * outputSize[0]) + offset[0]), 
        (int(input[1] / inputSize[1] * outputSize[1]) + offset[1])
    )
