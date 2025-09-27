from labyrinth_game.constants import ROOMS


def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory is not None:
        for item in inventory:
            print(item)


def get_input(prompt="> "):
    try:
        return NotImplementedError
    except (KeyboardInterrupt, EOFError):
        print('\nВыход из игры.')
        return 'quit'


def move_player(game_state, direction):
    current_room = game_state['current_room']
    current_room_stats = ROOMS[current_room]

    if direction in current_room_stats['exits']:
        new_room = current_room_stats['exits'][direction]
        game_state['current_room'] = new_room
        game_state['steps_taken'] += 1
        return True
    else:
        print('Нельзя пойти в этом направлении.')
        return False


def take_item(game_state, item_name):
    current_room = game_state['current_room']
    current_room_stats = ROOMS[current_room]

    if item_name in current_room_stats['items']:
        game_state['player_inventory'] += item_name
        current_room_stats['items'] -= item_name
        print(f'Вы подняли: {item_name}')
        return True
    else:
        print('Такого предмета здесь нет.')
        return False


def use_item(game_state, item_name):
    if item_name not in game_state['player_inventory']:
        print('У вас нет такого предмета.')

    match item_name:
        case 'torch':
            print('Стало светлее')
        case 'sword':
            print('Вы чувствуете себя увереннее')
        case 'bronze box':
            print('Вы открываете шкатулку')
            if 'rusty_key' not in game_state['player_inventory']:
                print('Получен ржавый ключ')
                game_state['player_inventory'] += 'rusty_key'
        case _:
            print('Вы не знаете как использовать этот предмет')
