reverseMode = False
next_toggle_time = time.time() + random.uniform(5, 10)


current_time = time.time()
        if current_time >= next_toggle_time:
            reverseMode = not reverseMode
            mode_str = "ENABLED" if reverseMode else "DISABLED"
            debugPrint(f"[TROLL MODE] Reverse mode toggled {mode_str}")
            next_toggle_time = current_time + random.uniform(5, 10)


if reverseMode:
                center_x = areaOffset[0] + areaSize[0] / 2
                center_y = areaOffset[1] + areaSize[1] / 2
                mapped_coords = (
                    int(2 * center_x - mapped_coords[0]),
                    int(2 * center_y - mapped_coords[1])
                )
                debugPrint("MOVE (reversed):", mapped_coords)
            else:
                debugPrint("MOVE (mapped):", mapped_coords)