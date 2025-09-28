from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
    current_room = game_state['current_room']
    current_room_stats = ROOMS[current_room]

    print(f'== {current_room.upper()} ==')
    print(current_room_stats['description'])

    print('Заметные предметы:')

    for item in current_room_stats['items']:
        print(f'{item}')

    print('Выходы:')

    for direction, target_room in current_room_stats['exits'].items():
        print(f'{direction}: {target_room}')

    if current_room_stats['puzzle'] is not None:
        print('Кажется, здесь есть загадка (используйте команду solve).')


def solve_puzzle(game_state):
    current_room = game_state['current_room']
    current_room_stats = ROOMS[current_room]

    if current_room_stats['puzzle'] is None:
        print('Загадок здесь нет.')
        return
    else:
        print(current_room_stats['puzzle'][0])
        answer = input('Ваш ответ: ').strip()
        print(f'Ваш ответ: {answer}')
        if answer == current_room_stats['puzzle'][1]:
            print('Верно!')
            ROOMS[current_room]['puzzle'] = None
            match current_room:
                case 'trap_room':
                    if 'rusty key' in ROOMS[current_room]['items']:
                        game_state['player_inventory'].append('rusty key')
                        ROOMS[current_room]['items'].remove('rusty key')
        else:
            print('Неверно. Попробуйте снова.')
            return

def attempt_open_treasure(game_state):
    if game_state['current_room'] == 'treasure_room':
        if 'treasure_chest' in ROOMS['treasure_room']['items']:
            print('Вы применяете ключ, и замок щёлкает. Сундук открыт!')
            ROOMS['treasure_room']['items'].remove('treasure_chest')
            print('В сундуке сокровище! Вы победили!')
            game_state['game_over'] = True
        else:
            print('Сундук уже открыт или отсутствует.')

# labyrinth_game/utils.py
def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
