#!/usr/bin/env python3
from .utils import describe_current_room, show_help, solve_puzzle, attempt_open_treasure
from .player_actions import get_input, show_inventory, move_player, take_item, use_item
from .constants import COMMANDS


def process_command(game_state: dict, command_line: str) -> None:
    """Разбирает введенную строку и исполняет соответствующую команду."""
    parts = command_line.strip().split()
    if not parts:
        return
    cmd = parts[0].lower()
    arg = " ".join(parts[1:]) if len(parts) > 1 else ""

    match cmd:
        case 'help':
            show_help(COMMANDS)
        case 'look':
            describe_current_room(game_state)
        case 'inventory':
            show_inventory(game_state)
        case 'go':
            if not arg:
                print("Укажите направление: north/south/east/west")
            else:
                move_player(game_state, arg.lower())
        case 'take':
            if not arg:
                print("Укажите предмет, который хотите взять.")
            else:
                take_item(game_state, arg)
        case 'use':
            if not arg:
                print("Укажите предмет, который хотите использовать.")
            else:
                use_item(game_state, arg)
        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case 'quit' | 'exit':
            game_state['game_over'] = True
        case 'north' | 'south' | 'east' | 'west':
            move_player(game_state, cmd)
        case _:
            print("Неизвестная команда. Введите 'help' для помощи.")


def main() -> None:
    """Точка входа: инициализация состояния, приветствие, основной цикл игры."""
    print("Добро пожаловать в Лабиринт сокровищ!")
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0,
    }
    describe_current_room(game_state)
    show_help(COMMANDS)
    while not game_state['game_over']:
        command_line = get_input("> ")
        process_command(game_state, command_line)


if __name__ == "__main__":
    main()


