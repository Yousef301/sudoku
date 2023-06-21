from one_player_mode import OPM
from two_players_mode import TPM

if __name__ == '__main__':  # Build the game
    print("\033[1m \t\t\t\t\t  'Welcome to sudoku'")
    print("\t\t\t\t\t  Chose playing mode\nOne Player Mode [OPM]\t\t\t\t\tTwo Player Mode [TPM]")
    choice = input("Your choice: ").upper()
    while choice not in ["OPM", "ONE PLAYER MODE", "TPM", "TWO PLAYER MODE"]:
        choice = input("Your choice: ").upper()
    if choice in ["OPM", "ONE PLAYER MODE"]:
        game = OPM()
        game.run_game()
    else:
        game = TPM()
        game.run_game()
