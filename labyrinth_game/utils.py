import math

from .constants import (
    EVENT_PROBABILITY,
    RANDOM_EVENT_KINDS,
    ROOMS,
    TRAP_DEATH_THRESHOLD,
    TRAP_ROLL_MODULO,
)


def show_help(commands: dict) -> None:
    """Печатает доступные команды с описаниями, выровненными по колонке."""
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<16} - {desc}")


def describe_current_room(game_state: dict) -> None:
    """Выводит заголовок, описание, предметы, выходы и наличие загадки."""
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


def pseudo_random(seed: int, modulo: int) -> int:
    """Детерминированный генератор [0, modulo) на базе sin/floor без random."""
    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(frac * modulo)


def trigger_trap(game_state: dict) -> None:
    """Срабатывание ловушки: теряем предмет или возможна смерть при пустом инвентаре."""
    print("Ловушка активирована! Пол стал дрожать...")
    inv = game_state['player_inventory']
    if inv:
        idx = pseudo_random(game_state['steps_taken'] + len(inv), len(inv))
        lost = inv.pop(idx)
        print(f"Вы потеряли предмет: {lost}")
    else:
        roll = pseudo_random(game_state['steps_taken'], TRAP_ROLL_MODULO)
        if roll < TRAP_DEATH_THRESHOLD:
            print("Вы сорвались в пропасть. Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вы едва удержались и уцелели.")


def random_event(game_state: dict) -> None:
    """Редкие случайные события при перемещении: находка, шорох, ловушка в темноте."""
    if pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY) != 0:
        return
    kind = pseudo_random(game_state['steps_taken'] + 1, RANDOM_EVENT_KINDS)
    room = ROOMS[game_state['current_room']]
    if kind == 0:
        print("На полу блестит монетка. Вы замечаете 'coin'.")
        if 'coin' not in room['items']:
            room['items'].append('coin')
    elif kind == 1:
        print("Где-то рядом слышен шорох...")
        if 'sword' in game_state['player_inventory']:
            print("Вы поднимаете меч — существо отступает.")
    else:
        room_name = game_state['current_room']
        has_torch = 'torch' not in game_state['player_inventory']
        if room_name == 'trap_room' and has_torch:
            print("Темно и опасно... Кажется, впереди ловушка.")
            trigger_trap(game_state)


def solve_puzzle(game_state: dict) -> None:
    """Решение загадки текущей комнаты; награды зависят от комнаты."""
    from .player_actions import get_input

    room_key = game_state['current_room']
    room = ROOMS[room_key]
    puzzle = room.get('puzzle')
    if not puzzle:
        print("Загадок здесь нет.")
        return
    question, answer = puzzle
    print(question)
    user = get_input("Ваш ответ: ").strip().lower()
    normalized_answer = str(answer).strip().lower()
    alt = {"10": {"10", "десять"}}
    valid_answers = alt.get(normalized_answer, {normalized_answer})
    if user in valid_answers:
        print("Верно! Вы решили загадку.")
        room['puzzle'] = None
        reward = None
        if room_key == 'hall':
            reward = 'treasure_key'
        elif room_key == 'library':
            reward = 'coin'
        if reward and reward not in game_state['player_inventory']:
            game_state['player_inventory'].append(reward)
            print(f"Вы получили: {reward}")
    else:
        print("Неверно. Попробуйте снова.")
        if room_key == 'trap_room':
            trigger_trap(game_state)


def attempt_open_treasure(game_state: dict) -> None:
    from .player_actions import get_input  # noqa: E501

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
    print(
        "Сундук заперт. Кажется, его можно открыть кодом. "
        "Ввести код? (да/нет)"
    )
    choice = get_input("> ").strip().lower()
    if choice != "да":
        print("Вы отступаете от сундука.")
        return
    _, answer = puzzle
    code = get_input("Введите код: ").strip()
    if code == str(answer):
        print("Код верный! Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        print("Неверный код.")
