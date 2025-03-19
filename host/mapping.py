from typing import Optional, Tuple

def locationMapping(
    inputLocation: Tuple[int, int], 
    inputSize: Tuple[int, int], 
    outputSize: Tuple[int, int], 
    inputOffset: Optional[Tuple[int, int]] = None,
    outputOffset: Optional[Tuple[int, int]] = None, 
    inputClippingSize: Optional[Tuple[int, int]] = None
) -> Tuple[int, int]:
    """Map tablet position to screen position base on config

    Args:
        input (Tuple[int, int]): Raw Pos from Tablet
        inputSize (Tuple[int, int]): Tablet Size
        inputOffset (Tuple[int, int]): Tablet Area Offset
        outputSize (Tuple[int, int]): Screen Area Size
        outputOffset (Tuple[int, int], optional): Area Offset. Defaults to (0, 0).

    Returns:
        Tuple[int, int]: Mapped Position
    """
    # Convert input tuple to list
    output = list(inputLocation)
    # Process input clipping
    if inputClippingSize:
        output[0] = min(inputClippingSize[0], output[0])
        output[1] = min(inputClippingSize[1], output[1])
    # Process input offset
    if inputOffset:
        output[0] -= inputOffset[0]
        output[1] -= inputOffset[1]
    # Process Mapping
    output[0] = int(output[0] / inputSize[0] * outputSize[0])
    output[1] = int(output[1] / inputSize[1] * outputSize[1])
    # Process output offset
    if outputOffset:
        output[0] += outputOffset[0]
        output[1] += outputOffset[1]
    
    return (
        max(0, min(output[0], outputSize[0])), 
        max(0, min(output[1], outputSize[1]))
    )
