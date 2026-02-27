# imports
import time
import msvcrt

# functions
def set_pixel(screen, x, y, char):
    screen[y][x] = char
def attempt_movement(dx, dy):
    player = get_entity('player')

    new_x = player['x'] + dx
    new_y = player['y'] + dy

    if 1 <= new_x <= screen_width-2 and 1 <= new_y <= screen_height-2:
        player['x'] = new_x
        player['y'] = new_y
def get_entity(name):
    for e in entities:
        if e['name'] == name:
            return e
def get_key():
    if not msvcrt.kbhit():
        return None

    key = msvcrt.getch()

    if key == b'\xe0':
        key = msvcrt.getch()
        return {
            b'H':'up',
            b'P':'down',
            b'K':'left',
            b'M':'right'
        }.get(key)

    if key == b'\x1b':
        return 'esc'

    return None
def translate(language, key):
    return texts[language][key]
    

# variables
## game
screen_width = 21
screen_height = 15
logic_fps = 27
fps = 27
step = 1 / logic_fps
previous_time = time.time()
accumulator = 0.0
delta = 0.0
frame_count = 0
game_state = 'start'
## language
language = 'unset'
languages = ['EN', 'CH']
texts = {
    'EN': {
        'tutorial1':"Arrow keys to move.",
        'tutorial2':"ESC to exit.",
        'exit':"Stopped by user."
    },
    'CH': {
        'tutorial1':"使用方向键移动。",
        'tutorial2':"使用ESC键退出。",
        'exit':"被玩家停止。"
    }
}
## entities
entities = [
    {'name':"player", 'x':10, 'y':7, 'char':"A"}
]
## textures
textures = {
    'empty':".",
    'full':"#",
    'vertical':"│",
    'horizontal':"─",
    'topleft':"┌",
    'topright':"┐",
    'bottomleft':"└",
    'bottomright':"┘",
}


print('\033c', end='')

# define game loop elements
def update():
    # movement
    global game_state, key

    if key == 'left':
        attempt_movement(-1, 0)
    elif key == 'right':
        attempt_movement(1, 0)
    elif key == 'up':
        attempt_movement(0, -1)
    elif key == 'down':
        attempt_movement(0, 1)
    elif key == 'esc':
        game_state = 'end'

def draw():
    # clear screen
    print('\033[H', end='', flush=True)

    # set screen
    screen = [[textures['empty']] * screen_width for _ in range(screen_height)]
    ## screen borders
    screen[0] = [textures['horizontal']] * screen_width
    screen[-1] = [textures['horizontal']] * screen_width
    for row in screen:
       row[0] = textures['vertical']
       row[-1] = textures['vertical']
    ## set corners
    set_pixel(screen, 0, 0, textures['topleft'])
    set_pixel(screen, screen_width-1, 0, textures['topright'])
    set_pixel(screen, 0, screen_height-1, textures['bottomleft'])
    set_pixel(screen, screen_width-1, screen_height-1, textures['bottomright'])

    # entities
    for entity in entities:
        screen[entity['y']][entity['x']] = entity['char']

    # print screen
    for row in screen:
        print(' '.join(row))
    print(translate(language, 'tutorial1'))
    print(translate(language, 'tutorial2'))
    print()
    print(str(frame_count))


# game loop
while True:
    # quit loop
    if game_state == 'end':
        print('\033c', end='')
        print(translate(language, 'exit'))
        break
    if game_state == 'start':
        print('\033c', end='')
        language = input("> Choose your language: EN - English\n> 设定语言： CH - 中文\n\n> ").upper()

        if language in languages:
            game_state = 'game'
        else:
            print("Invalid language.")
    if game_state == 'game':
        accumulator += time.time() - previous_time
        key = get_key()
        while accumulator >= step:
            update()
            accumulator -= step
        draw()

    frame_count += 1
    previous_time = time.time()

    time.sleep(1 / fps)