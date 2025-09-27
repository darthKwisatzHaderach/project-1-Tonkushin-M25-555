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
