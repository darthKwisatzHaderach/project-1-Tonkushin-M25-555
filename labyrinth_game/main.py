#!/usr/bin/env python3
from labyrinth_game.player_actions import get_input, move_player, take_item, use_item
from labyrinth_game.utils import describe_current_room, show_help

game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Значения окончания игры
    'steps_taken': 0  # Количество шагов
}


def main():
    print('Добро пожаловать в Лабиринт сокровищ!')

    while game_state['game_over'] is not True:
        describe_current_room(game_state)
        process_command(game_state, get_input(game_state))


def process_command(game_state, command):
    parts = command.lower().split()
    if not parts:
        return None

    command_name = parts[0]
    args = parts[1:]

    match command_name:
        case 'look':
            describe_current_room(game_state)
        case 'use':
            use_item(game_state, args[0])
        case 'go':
            move_player(game_state, args[0])
        case 'take':
            take_item(game_state, args[0])
        case 'inventory':
            print(f"{game_state['player_inventory']}")
        case 'help':
            show_help()
        case 'quit':
            return 'quit'
    return None


if __name__ == "__main__":
    main()
