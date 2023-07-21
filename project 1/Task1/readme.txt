Name: JEEVAN REDDY BODAPATLA
UTA ID: 1001949287
PROGRAMMING LANGUAGE: PYTHON


How the code is structured:

1. Search() - Main Function to control the search, is to call the specific function according to the parameter received using conditional statements. 
2. Read_Input_File() - Function to read input file and save it. 
3. TakeHeuristic_() - Function to read the heuristic file and save it. 
4. UninformedSearch() - Function to perform uninformed search. 
5. InformedSearch() - Function to perform informed search. 
6. FinalPathGen() - Function to generate the final path between the starting and the ending node. 
7. __main__() - Maion driver code of complete program.


How to run the code:

1. Open Command Prompt.
2.Set the path in the command prompt to the file location of Task 1 

UNIFORMED SEARCH:
Run the command as:
   "python find_route.py input.txt Bremen Kassel"

INFORMED SEARCH:
Run the command as:

    "python find_route.py input.txt Bremen Kassel h_kassel.txt"