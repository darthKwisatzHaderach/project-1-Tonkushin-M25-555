from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
    room_key = game_state['current_room']
    room = ROOMS[room_key]
    print(f"\n== {room_key.upper()} ==")
    print(room['description'])
    if room['items']:
        print("Заметные предметы:", ", ".join(room['items']))
    exits = ", ".join(sorted(room['exits'].keys()))
    print("Выходы:", exits if exits else "нет")
    if room.get('puzzle'):
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    room_key = game_state['current_room']
    room = ROOMS[room_key]
    puzzle = room.get('puzzle')
    if not puzzle:
        print("Загадок здесь нет.")
        return
    question, answer = puzzle
    print(question)
    user = input("Ваш ответ: ").strip().lower()
    if user == str(answer).strip().lower():
        print("Верно! Вы решили загадку.")
        room['puzzle'] = None
        if 'treasure_key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('treasure_key')
            print("Вы получили: treasure_key")
    else:
        print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
    room_key = game_state['current_room']
    if room_key != 'treasure_room':
        print("Здесь нечего открывать.")
        return
    room = ROOMS[room_key]
    if 'treasure_chest' not in room['items']:
        print("Сундук уже открыт.")
        return
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return
    puzzle = room.get('puzzle')
    if not puzzle:
        print("Кодов здесь нет.")
        return
    print("Сундук заперт. Кажется, его можно открыть кодом. Ввести код? (да/нет)")
    choice = input("> ").strip().lower()
    if choice != "да":
        print("Вы отступаете от сундука.")
        return
    _, answer = puzzle
    code = input("Введите код: ").strip()
    if code == str(answer):
        print("Код верный! Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        print("Неверный код.")

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
