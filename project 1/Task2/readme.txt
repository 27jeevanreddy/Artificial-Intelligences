Name: JEEVAN REDDY BODAPATLA
UTA ID: 1001949287
PROGRAMMING LANGUAGE: PYTHON

How the Code is Structured:
1. Class class_design_main_4connect_game() - Class to handle all the data variables and functions related to board game. 
	1> __init__() - Constructor code to initialize required variables. 
	2> game_auto_play_using_AI() - Function to initiate the AI move. 
	3> select_best_move_functions() - Function to find the best move possible according to the current sttae of the board. 
	4> play_game_piece() - Function to make a move. 
	5> performing_mini_maxi_function() - Function to perform required minmax calculations. 
	6> generate_Next_Successors() - Function to find the next successor in the game and check it. 
	7> performing_alpha_beta_function() - Function to perform all alphabet calculations. 
	8> eval() - Function for final evaluation of move. 
	9> count_total_score() - Function to check total score. 
	10> count_1() - Function to check horizontal score. 
	11> count_2() - Function to check vertical score. 
	12> count_3() - Function to check diagonal score. 
2. game_interactive_mode() - Function to initiate the interactive mode of the game. 
3. __main__() - main driver code of complete program.

How to execute:
1. Open Command Prompt.
2.Set the path in the command prompt to the file location of Task 2

Part 1 - Interactive Mode
	->python maxconnect4.py interactive input1.txt human_next 3
	->python maxconnect4.py interactive input1.txt computer_next 3

Part 2 - One-Move Mode
	-> python maxconnect4.py one-move input1.txt output1.txt 2