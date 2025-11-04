from .constants import ROOMS
from .utils import describe_current_room, random_event


def get_input(prompt: str = "> ") -> str:
    """Безопасное чтение ввода. На Ctrl+C/EOF возвращает 'quit'."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state: dict) -> None:
    """Печатает содержимое инвентаря или сообщение об отсутствии предметов."""
    inv = game_state['player_inventory']
    if inv:
        print("Инвентарь:", ", ".join(inv))
    else:
        print("Инвентарь пуст.")


def move_player(game_state: dict, direction: str) -> None:
    """Перемещение по направлению: проверка выхода, ключа в treasure_room, события."""
    current = game_state['current_room']
    exits = ROOMS[current]['exits']
    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return
    target = exits[direction]
    if target == 'treasure_room' and 'rusty_key' not in game_state['player_inventory']:
        print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        return
    if target == 'treasure_room':
        print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
    game_state['current_room'] = target
    game_state['steps_taken'] += 1
    describe_current_room(game_state)
    random_event(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    """Поднять предмет из комнаты в инвентарь (сундук слишком тяжел)."""
    room = ROOMS[game_state['current_room']]
    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return
    if item_name in room['items']:
        game_state['player_inventory'].append(item_name)
        room['items'].remove(item_name)
        print("Вы подняли:", item_name)
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state: dict, item_name: str) -> None:
    """Использование предметов с простыми эффектами (факел, меч, шкатулка)."""
    inv = game_state['player_inventory']
    if item_name not in inv:
        print("У вас нет такого предмета.")
        return
    match item_name:
        case 'torch':
            print("Вы зажигаете факел. Стало светлее и уютнее.")
        case 'sword':
            print("Вы сжимаете меч — чувствуете уверенность и силу.")
        case 'bronze_box':
            if 'rusty_key' not in inv:
                inv.append('rusty_key')
                print("Вы открыли бронзовую шкатулку и нашли rusty_key!")
            else:
                print("В шкатулке пусто.")
        case _:
            print("Вы не знаете, как использовать этот предмет.")


