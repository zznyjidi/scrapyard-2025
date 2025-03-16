import time, random
import thread_lock
from media.sensor import Sensor
from media.display import Display
from media.media import MediaManager

# Initialize hardware components
sensor = Sensor()
sensor.reset()
sensor.set_framesize(width=800, height=480)
sensor.set_pixformat(Sensor.RGB565)

Display.init(Display.ST7701, to_ide=True)
MediaManager.init()

# Start sensor to obtain an image buffer.
sensor.run()

def get_blank_image():
    """Creates and returns a blank image with a black background."""
    img = sensor.snapshot()
    img.draw_rectangle(0, 0, 800, 480, color=(0, 0, 0), thickness=0, fill=True)
    return img

def display_ascii(lines, scale=4, x=20, start_y=20, line_spacing_factor=10):
    """Displays ASCII art on the screen with specified formatting."""
    img = get_blank_image()
    y = start_y
    for line in lines:
        img.draw_string_advanced(x, y, scale, line, color=(255, 255, 255))
        y += int(scale * line_spacing_factor)
    Display.show_image(img)

def build_bubble_art(quote):
    """Builds an ASCII speech bubble around the given quote."""
    border = "+" + "-" * (len(quote) + 18) + "+"
    bubble = [
        border,
        "| " + quote + " |",
        border
    ]
    return bubble

quotes = [
    "Look at you, trying your best.",
    "Do you really think you can succeed?",
    "You're making it worse, just like always.",
    "I hope you're proud of yourself... not.",
    "Getting over it? More like tripping over it.",
    "Well, that was a splendid disaster!",
    "If incompetence was art, you'd be Picasso.",
    "You're the reason even failure looks good.",
    "Keep going... so you can have more to fail at.",
    "Poor Me Blues — Edna Hicks",
    "Goin' Down the Road Feeling Bad — Cliff Carlisle",
    "Born To Lose — Tedd Daffan Texans",
    "Don't hate the player, hate the game"
]

@thread_lock.with_lock
def displayLoop():
    """Runs an infinite loop displaying random quotes on the screen."""
    while True:
        current_quote = random.choice(quotes)
        ascii_art = build_bubble_art(current_quote)
        display_ascii(ascii_art, scale=35, x=20, start_y=20, line_spacing_factor=6)
        time.sleep(5)
