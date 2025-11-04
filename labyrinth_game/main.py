#!/usr/bin/env python3
from labyrinth_game.player_actions import get_input, move_player, take_item, use_item
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
    show_help()
    while not game_state['game_over']:
        command_line = get_input("> ")
        process_command(game_state, command_line)


def process_command(game_state, command):
    parts = command.lower().split()
    if not parts:
        return None

    command_name = parts[0]
    args = parts[1:]

    match command_name:
        case 'help':
            show_help()
        case 'look':
            describe_current_room(game_state)
        case 'inventory':
            print(f"{game_state['player_inventory']}")
        case 'go':
            if not args:
                print("Укажите направление: north/south/east/west")
            else:
                move_player(game_state, args[0].lower())
        case 'take':
            if not args:
                print("Укажите предмет, который хотите взять.")
            else:
                take_item(game_state, args[0])
        case 'use':
            if not args:
                print("Укажите предмет, который хотите использовать.")
            else:
                use_item(game_state, args[0])
        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case 'quit' | 'exit':
            game_state['game_over'] = True
        case _:
            print("Неизвестная команда. Введите 'help' для помощи.")
    return None


if __name__ == "__main__":
    main()
