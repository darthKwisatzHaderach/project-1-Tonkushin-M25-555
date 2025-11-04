#!/usr/bin/env python3
from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import get_input, move_player, take_item, use_item, show_inventory
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)

game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Значения окончания игры
    'steps_taken': 0  # Количество шагов
}


def main():
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


def process_command(game_state: dict, command_line: str) -> None:
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


if __name__ == "__main__":
    main()
