import pyautogui
from pygame import *

width = 500
height = 500
gap = 14
block_size = (width - 5 * gap) / 4

cell_colour = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}


def textColour(value):
    if value >= 8:
        return 249, 246, 242
    else:
        return 119, 110, 101


def main():
    init()
    screen = display.set_mode((height, width))
    display.set_caption('2048 Game')

    background = Surface(screen.get_size())
    background = background.convert()
    background.fill((187, 173, 160))

    while 1:
        for e in event.get():
            if e.type == QUIT:
                return

            screen.blit(background, (0, 0))
            drawGrid(background)
            drawCell(0, 0, 2, background)
            drawCell(0, 1, 4, background)
            drawCell(2, 2, 32, background)
            drawCell(1, 1.5, 16, background)
            display.flip()


def drawGrid(background):
    grid = []

    for y in range(0, 4):
        for x in range(0, 4):
            rect = Rect(x * (block_size + gap) + gap, (y * (block_size + gap) + gap), block_size, block_size)
            grid.append(rect)

    for rect in grid:
        AAfilledRoundedRect(background, rect, (205, 193, 179), 0.1)


def drawCell(cell_x, cell_y, value, background):
    rect = Rect(cell_x * (block_size + gap) + gap, (cell_y * (block_size + gap) + gap), block_size, block_size)
    AAfilledRoundedRect(background, rect, cell_colour.get(value), 0.1)
    number = font.Font("fonts/arialbd.ttf", 55)
    Text_Surf, TextRect = text_objects(str(value), number, textColour(value))
    TextRect.center = (int(rect.x + 0.5 * block_size), int(rect.y + 0.5 * block_size))
    background.blit(Text_Surf, TextRect)


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def AAfilledRoundedRect(surface, rect, colour, radius=0.4):
    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect = Rect(rect)
    colour = Color(*colour)
    alpha = colour.a
    colour.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = Surface(rect.size, SRCALPHA)

    circle = Surface([min(rect.size) * 3] * 2, SRCALPHA)
    draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

    rectangle.fill(colour, special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle, pos)


if __name__ == '__main__':
    main()
