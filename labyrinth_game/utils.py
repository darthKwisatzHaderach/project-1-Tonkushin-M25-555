from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
    current_room = game_state['current_room']
    current_room_stats = ROOMS[current_room]

    print(f'== {current_room} ==')
    print(current_room_stats['description'])

    print('Заметные предметы:')

    for item in current_room_stats['items']:
        print(f'{item}')

    print('Выходы:')

    for direction, target_room in current_room_stats['exits'].items():
        print(f'{direction}: {target_room}')

    if current_room_stats['puzzle'] is not None:
        print('Кажется, здесь есть загадка (используйте команду solve).')
