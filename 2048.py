from pygame import *
import random as r
import copy
import math as m

width = 500
height = 500
gap = 14
block_size = (width - 5 * gap) / 4
game_board = []
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3
start_time = 0
animation_status = 0
is_animating = False
animation_ghost = []
animation_time = 100
max_scale = 0.15

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


class Cell:
    def __init__(self, x_coord, y_coord, value):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.value = value
        self.combined = False
        self.x_old = None
        self.x_old = None


def text_colour(value):
    if value >= 8:
        return 249, 246, 242
    else:
        return 119, 110, 101


def main():
    global is_animating
    global start_time
    global animation_status
    global animation_ghost
    init()
    screen = display.set_mode((height, width))
    display.set_caption('2048 Game')
    background = Surface(screen.get_size())
    background = background.convert()
    background.fill((187, 173, 160))
    lost = False
    fill_board()
    clock = time.Clock()
    while 1:
        for e in event.get():
            if e.type == QUIT:
                return
            if e.type == KEYDOWN and not is_animating:
                if e.key == K_RIGHT:
                    move(DIR_RIGHT)
                if e.key == K_UP:
                    move(DIR_UP)
                if e.key == K_DOWN:
                    move(DIR_DOWN)
                if e.key == K_LEFT:
                    move(DIR_LEFT)
                if e.key == K_r:
                    lost = False
                    fill_board()
                if e.key == K_l:
                    lost = True
            if lose_game():
                lost = True

        if is_animating:
            animation_status = (time.get_ticks() - start_time) / animation_time
        if animation_status >= 1:
            animation_status = 0
            is_animating = False
            animation_ghost = []
            for cell in game_board:
                cell.combined = False
            gen_cell()

        background.fill((187, 173, 160))
        draw_grid(background)
        draw_board(background)
        if lost:
            draw_lose(background)
        screen.blit(background, (0, 0))
        display.flip()


###############################################

def gen_cell():
    added = 0
    if len(game_board) == 16:
        return None
    while added < 1:
        cell_x = r.randint(0, 3)
        cell_y = r.randint(0, 3)

        already_exists = False
        for cell in game_board:
            if cell.x_coord == cell_x and cell.y_coord == cell_y:
                already_exists = True
        if already_exists:
            continue

        if r.random() < 0.25:
            value = 4
        else:
            value = 2
        game_board.append(Cell(cell_x, cell_y, value))
        added += 1


def draw_cell(cell_x, cell_y, value, background, scale=1.0):
    scale_change = ((scale - 1) * block_size) / 2
    rect = Rect(cell_x * (block_size + gap) + gap - scale_change, (cell_y * (block_size + gap) + gap) - scale_change,
                block_size + 2 * scale_change, block_size + 2 * scale_change)
    AAfilledRoundedRect(background, rect, cell_colour.get(value), 0.1)
    number = font.Font("fonts/arialbd.ttf", 55)
    text_surf, text_rect = text_objects(str(value), number, text_colour(value))
    text_rect.center = (int(rect.x + 0.5 * block_size + scale_change), int(rect.y + 0.5 * block_size + scale_change))
    background.blit(text_surf, text_rect)


def draw_grid(background):
    grid = []

    for y in range(0, 4):
        for x in range(0, 4):
            rect = Rect(x * (block_size + gap) + gap, (y * (block_size + gap) + gap), block_size, block_size)
            grid.append(rect)

    for rect in grid:
        AAfilledRoundedRect(background, rect, (205, 193, 179), 0.1)


def draw_board(background):
    if is_animating:
        scale = m.sin(animation_status * m.pi) * max_scale + 1
        for cell in animation_ghost:
            x_position = cell.x_coord * animation_status + cell.x_old * (1 - animation_status)
            y_position = cell.y_coord * animation_status + cell.y_old * (1 - animation_status)
            draw_cell(x_position, y_position, cell.value, background)
        for cell in game_board:
            x_position = cell.x_coord * animation_status + cell.x_old * (1 - animation_status)
            y_position = cell.y_coord * animation_status + cell.y_old * (1 - animation_status)
            if cell.combined:
                draw_cell(x_position, y_position, cell.value, background, scale)
            else:
                draw_cell(x_position, y_position, cell.value, background)
    else:
        for cell in game_board:
            draw_cell(cell.x_coord, cell.y_coord, cell.value, background)


def draw_lose(background):
    rect = Rect(gap, gap, width - 2 * gap, height - 2 * gap)
    AAfilledRoundedRect(background, rect, (140, 140, 140, 140), 0.1 * block_size / (width - 2 * gap))
    fonta = font.Font("fonts/arialbd.ttf", 65)
    text_surf, text_rect = text_objects('You Lose', fonta, (64, 64, 64))
    text_rect.center = (width / 2, (height / 2) - 30)
    background.blit(text_surf, text_rect)
    score = 0
    for cell in game_board:
        score += cell.value
    fonta = font.Font("fonts/arialbd.ttf", 55)
    text_surf, text_rect = text_objects('Score: {}'.format(score), fonta, (64, 64, 64))
    text_rect.center = (width / 2, (height / 2) + 30)
    background.blit(text_surf, text_rect)


def lose_game():
    # check copy of the board if it is full
    global animation_ghost
    global animation_status
    global is_animating
    global game_board
    if len(game_board) == 16:
        current_state = copy.deepcopy(game_board)
        move(DIR_UP, True)
        move(DIR_RIGHT, True)
        move(DIR_LEFT, True)
        move(DIR_DOWN, True)
        animation_status = 0
        is_animating = False
        animation_ghost = []
        for cell in game_board:
            cell.combined = False
        if len(game_board) == 16:
            game_board = current_state
            return True
        else:
            game_board = current_state
    return False


def text_objects(text, input_font, colour):
    text_surface = input_font.render(text, True, colour)
    return text_surface, text_surface.get_rect()


def fill_board():
    game_board.clear()
    gen_cell()
    gen_cell()

    return None


# is the board full for now -> change to can't make move


def move(direction, silent=False):
    global start_time
    global is_animating
    global animation_ghost
    if not silent:
        is_animating = True
        start_time = time.get_ticks()
    if direction == DIR_UP:
        coords = [(x, y) for y in range(1, 4, 1) for x in range(0, 4)]
        x_offset = 0
        y_offset = -1
    elif direction == DIR_RIGHT:
        coords = [(x, y) for x in range(2, -1, -1) for y in range(0, 4)]
        x_offset = 1
        y_offset = 0
    elif direction == DIR_DOWN:
        coords = [(x, y) for y in range(2, -1, -1) for x in range(0, 4)]
        x_offset = 0
        y_offset = 1
    elif direction == DIR_LEFT:
        coords = [(x, y) for x in range(1, 4, 1) for y in range(0, 4)]
        x_offset = -1
        y_offset = 0
    else:
        return None

    for cell in game_board:
        cell.x_old = cell.x_coord
        cell.y_old = cell.y_coord

    for _ in range(4):
        for x, y in coords:
            current_index = get_at_coord(x, y)
            if current_index == -1:
                continue
            next_index = get_at_coord(x + x_offset, y + y_offset)

            if next_index == -1:
                game_board[current_index].x_coord += x_offset
                game_board[current_index].y_coord += y_offset
            elif game_board[current_index].value == game_board[next_index].value and (
                    not game_board[current_index].combined and not game_board[next_index].combined):
                game_board[next_index].value *= 2
                game_board[next_index].combined = True
                game_board[current_index].x_coord += x_offset
                game_board[current_index].y_coord += y_offset
                animation_ghost.append(game_board[current_index])
                game_board.pop(current_index)

    return None


def get_at_coord(x_coor, y_coor):
    for i, cell in enumerate(game_board):
        if x_coor == cell.x_coord and y_coor == cell.y_coord:
            return i
    return -1


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
