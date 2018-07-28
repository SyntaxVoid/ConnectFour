# John Gresl 7/26/2018
import Connect4Logic
import Connect4GUIStartup
import Connect4GUI

if __name__ == "__main__":
    setup_vars = {}
    while True:
        setup = Connect4GUIStartup.Connect4GUIStartup(**setup_vars)
        setup_vars = setup.outd
        if setup_vars is None:
            break
        game = Connect4Logic.Connect4Logic(**setup_vars)
        GUIgame = Connect4GUI.Connect4GUI(game)
        if not GUIgame.play_again_bool:
            break