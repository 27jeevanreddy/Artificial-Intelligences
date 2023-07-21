import copy
import random
import sys
import time

class class_design_main_4connect_game:
    def __init__(self):
        self.template_game_board_design = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn, self.player1Score, self.player2Score, self.pieceCount, self.gameFile, self.utility  = 1, 0, 0, 0, None, None
        random.seed()
    def game_auto_play_using_AI(self, depth, computing_state):
        self.generate_Next_Successors(depth - 1, computing_state)
        column = self.select_best_move_functions(computing_state)
        result = self.play_game_piece(column)
        if not result:self.game_auto_play_using_AI(depth, computing_state)
        else:print('\n\nmove %d: Player %d, column %d\n' % (self.pieceCount, self.currentTurn, column+1))
        return
    def select_best_move_functions(self, computing_state):
        alpha, beta = -999, 999
        temp_value_v = self.performing_alpha_beta_function(computing_state, alpha, beta)
        for child in self.children:
            if child.utility == temp_value_v:return child.column
    def play_game_piece(self, column):
        if not self.template_game_board_design[0][column]:
            temp_range = range(5, -1, -1)
            for i in list(temp_range):         
                if not self.template_game_board_design[i][column]:
                    temp = self.currentTurn
                    self.template_game_board_design[i][column], self.pieceCount  = temp, self.pieceCount + 1
                    return 1
    def performing_mini_maxi_function(self, computing_state):
        if self.utility is not None:return self.utility
        elif self.currentTurn == computing_state:
            temp_value_v = -999
            for child in self.children:temp_value_v = max(temp_value_v, child.performing_mini_maxi_function(computing_state))
        else:
            temp_value_v = 999
            for child in self.children: temp_value_v = min(temp_value_v, child.performing_mini_maxi_function(computing_state))
        self.utility = temp_value_v
        return self.utility
    def generate_Next_Successors(self, depth, computing_state):
        if depth >= 0 and self.pieceCount < 42:
            self.children = []
            for gameColumn in range(0, 7):
                if not self.template_game_board_design[0][gameColumn]:
                    child = class_design_main_4connect_game()
                    child.template_game_board_design = copy.deepcopy(self.template_game_board_design)
                    if self.currentTurn == 1:child.currentTurn = 2
                    elif self.currentTurn == 2:child.currentTurn = 1
                    child.evaluation, child.pieceCount = 0, self.pieceCount + 1
                    if computing_state == self.currentTurn:
                        self.eval(computing_state)
                        child.evaluation = self.bestMove["utility"]
                        child.template_game_board_design[self.bestMove["row"]][self.bestMove["column"]] = self.currentTurn
                        child.column = self.bestMove["column"]
                        self.children.append(child)
                        break
                    else:
                        for i in range(5, -1, -1):
                            if not child.template_game_board_design[i][gameColumn]:
                                child.template_game_board_design[i][gameColumn] = self.currentTurn
                                child.column = gameColumn
                                self.children.append(child)
                                break
            for child in self.children:child.generate_Next_Successors(depth - 1, computing_state)       
        else: 
            self.count_total_score()
            if computing_state == 1:self.utility = self.player1Score - self.player2Score + self.evaluation
            else:self.utility = self.player2Score - self.player1Score + self.evaluation
    def performing_alpha_beta_function(self, computing_state, alpha, beta):
        if self.utility is not None:
            return self.utility
        elif self.currentTurn == computing_state:
            temp_value_v = -999
            for child in self.children:
                temp_value_v = max(temp_value_v, child.performing_alpha_beta_function(computing_state, alpha, beta))
                if alpha >= beta:
                    self.utility = temp_value_v
                    return self.utility
                else:alpha = max(alpha, temp_value_v)
        else:
            temp_value_v = 999
            for child in self.children:
                temp_value_v = min(temp_value_v, child.performing_alpha_beta_function(computing_state, alpha, beta))
                if beta <= alpha:
                    self.utility = temp_value_v
                    return self.utility
                else:beta = min(temp_value_v, beta)
        self.utility = temp_value_v
        return self.utility
    def eval(self, computer):
        if computer == 1:opposition = 2
        else:opposition = 1
        playableMoves = []
        for column in range(0, 7):
            if not self.template_game_board_design[0][column]:
                for row in range(5, -1, -1):
                    if not self.template_game_board_design[row][column]:
                        playableMoves.append({"row": row,"column": column})
                        break
        if len(playableMoves) > 0:
            self.loose, self.win, self.probMax, self.looseBestMove, self.winBestMove, self.probMove = -1, -1, -1, None, None, None
            self.randomMove = playableMoves[random.randrange(0, len(playableMoves))] 
            for move in playableMoves:
                looseCounter, winCounter, probCounter = 0, 0, 0
                if move["column"] - 3 >= 0:column_min = move["column"] - 3
                else:column_min = 0
                if move["column"] + 3 <= 6:column_max = move["column"] + 3
                else:column_max = 6
                current_row = self.template_game_board_design[move["row"]][:]
                current_row[move["column"]] = opposition
                for i in range(column_min, column_max - 2, 1):
                    if current_row[i:i+4] == [opposition]*4:looseCounter += 1
                current_row[move["column"]] = computer
                for i in range(column_min, column_max - 2, 1):
                    if current_row[i:i+4] == [computer]*4:winCounter += 1
                    try:
                        if current_row[i:i+4].index(opposition) >= 0: pass
                    except: probCounter += 1
                if move["row"] + 3 <= 5:
                    if self.template_game_board_design[move["row"] + 3][move["column"]] == opposition and self.template_game_board_design[move["row"] + 2][move["column"]] == opposition and self.template_game_board_design[move["row"] + 1][move["column"]] == opposition: looseCounter += 1
                    if self.template_game_board_design[move["row"] + 3][move["column"]] == computer and self.template_game_board_design[move["row"] + 2][move["column"]] == computer and self.template_game_board_design[move["row"] + 1][move["column"]] == computer: winCounter += 1
                    probArray = []
                    probArray.append(self.template_game_board_design[move["row"] + 3][move["column"]])
                    probArray.append(self.template_game_board_design[move["row"] + 2][move["column"]])
                    probArray.append(self.template_game_board_design[move["row"] + 1][move["column"]])
                    try:
                        if probArray.index(opposition) >= 0:pass
                    except:probCounter += 1
                r_start, c_start, i = move["row"], move["column"], -3
                while i != 0 and r_start != 0 and c_start != 0:r_start, c_start, i = r_start - 1, c_start - 1, i-1
                r_end, c_end, i = move["row"], move["column"], 3
                while i != 0 and r_end != 5 and c_end != 6:r_end, c_end, i = r_end + 1, c_end + 1, i-1
                r_start_save, r_end_save, c_start_save, c_end_save = r_start, r_end, c_start, c_end
                current_map = copy.deepcopy(self.template_game_board_design)
                current_map[move["row"]][move["column"]] = computer
                while r_start <= r_end - 3:
                    if current_map[r_start][c_start] == computer and current_map[r_start+1][c_start+1] == computer and current_map[r_start+2][c_start+2] == computer and current_map[r_start+3][c_start+3] == computer: winCounter += 1 
                    probArray = []
                    probArray.append(current_map[r_start][c_start])
                    probArray.append(current_map[r_start+1][c_start+1])
                    probArray.append(current_map[r_start+2][c_start+2])
                    probArray.append(current_map[r_start+3][c_start+3])
                    r_start, c_start = r_start + 1, c_start + 1
                    try:
                        if probArray.index(opposition) >= 0:pass
                    except: probCounter += 1
                r_start, r_end, c_start, c_end = r_start_save, r_end_save, c_start_save, c_end_save
                current_map = copy.deepcopy(self.template_game_board_design)
                current_map[move["row"]][move["column"]] = opposition
                while r_start <= r_end - 3:
                    if current_map[r_start][c_start] == opposition and current_map[r_start+1][c_start+1] == opposition and current_map[r_start+2][c_start+2] == opposition and current_map[r_start+3][c_start+3] == opposition:looseCounter += 1 
                    r_start, c_start = r_start + 1, c_start + 1
                r_start, c_start, i = move["row"], move["column"], -3
                while i != 0 and r_start != 0 and c_start != 6:r_start, c_start, i = r_start - 1, c_start + 1, i-1
                r_end, c_end, i = move["row"], move["column"], 3
                while i != 0 and r_end != 5 and c_end != 0:r_end, c_end, i = r_end + 1, c_end - 1, i-1
                r_start_save, r_end_save, c_start_save, c_end_save = r_start, r_end, c_start, c_end       
                current_map = copy.deepcopy(self.template_game_board_design)
                current_map[move["row"]][move["column"]] = computer
                while r_start <= r_end - 3:
                    if current_map[r_start][c_start] == computer and current_map[r_start+1][c_start-1] == computer and current_map[r_start+2][c_start-2] == computer and current_map[r_start+3][c_start-3] == computer: winCounter += 1 
                    probArray = []
                    probArray.append(current_map[r_start][c_start])
                    probArray.append(current_map[r_start+1][c_start-1])
                    probArray.append(current_map[r_start+2][c_start-2])
                    probArray.append(current_map[r_start+3][c_start-3])
                    r_start, c_start = r_start + 1, c_start - 1
                    try:
                        if probArray.index(opposition) >= 0:pass
                    except:probCounter += 1
                r_start, r_end, c_start, c_end = r_start_save, r_end_save, c_start_save, c_end_save
                current_map = copy.deepcopy(self.template_game_board_design)
                current_map[move["row"]][move["column"]] = opposition
                while r_start <= r_end - 3:
                    if current_map[r_start][c_start] == opposition and current_map[r_start+1][c_start-1] == opposition and current_map[r_start+2][c_start-2] == opposition and current_map[r_start+3][c_start-3] == opposition:looseCounter += 1 
                    r_start, c_start = r_start + 1, c_start - 1
                if looseCounter != 0 and looseCounter > self.loose:self.loose, self.looseBestMove = looseCounter, move
                if winCounter != 0 and winCounter > self.win:self.win, self.winBestMove = winCounter, move
                if probCounter != 0 and probCounter > self.probMax:self.probMax, self.probMove = probCounter, move
            if self.win >= self.loose and self.win != -1:self.bestMove = {"row" : self.winBestMove["row"],"column" : self.winBestMove["column"],"utility" : self.win * 4}
            elif self.win < self.loose:self.bestMove = {"row" : self.looseBestMove["row"],"column" : self.looseBestMove["column"],"utility" : self.loose * 4}
            elif self.probMax > 0:self.bestMove = {"row" : self.probMove["row"],"column" : self.probMove["column"],"utility" : self.probMax}
            else:self.bestMove = {"row" : self.randomMove["row"],"column" : self.randomMove["column"],"utility" : 0}
        else:self.bestMove = None
    
    def count_total_score(self):
        self.player1Score = 0
        self.player2Score = 0
        self.count_1()
        self.count_2()
        self.count_3()
    
    def count_1(self):
        for row in self.template_game_board_design:
            if row[0:4] == [1]*4: self.player1Score += 1
            if row[1:5] == [1]*4: self.player1Score += 1
            if row[2:6] == [1]*4: self.player1Score += 1
            if row[3:7] == [1]*4: self.player1Score += 1
            if row[0:4] == [2]*4: self.player2Score += 1
            if row[1:5] == [2]*4: self.player2Score += 1
            if row[2:6] == [2]*4: self.player2Score += 1
            if row[3:7] == [2]*4: self.player2Score += 1
        
    def count_2(self):
        for j in range(7):
            if (self.template_game_board_design[0][j] == 1 and self.template_game_board_design[1][j] == 1 and self.template_game_board_design[2][j] == 1 and self.template_game_board_design[3][j] == 1): self.player1Score += 1
            if (self.template_game_board_design[1][j] == 1 and self.template_game_board_design[2][j] == 1 and self.template_game_board_design[3][j] == 1 and self.template_game_board_design[4][j] == 1): self.player1Score += 1
            if (self.template_game_board_design[2][j] == 1 and self.template_game_board_design[3][j] == 1 and self.template_game_board_design[4][j] == 1 and self.template_game_board_design[5][j] == 1): self.player1Score += 1
            if (self.template_game_board_design[0][j] == 2 and self.template_game_board_design[1][j] == 2 and self.template_game_board_design[2][j] == 2 and self.template_game_board_design[3][j] == 2): self.player2Score += 1
            if (self.template_game_board_design[1][j] == 2 and self.template_game_board_design[2][j] == 2 and self.template_game_board_design[3][j] == 2 and self.template_game_board_design[4][j] == 2): self.player2Score += 1
            if (self.template_game_board_design[2][j] == 2 and self.template_game_board_design[3][j] == 2 and self.template_game_board_design[4][j] == 2 and self.template_game_board_design[5][j] == 2): self.player2Score += 1
        
    def count_3(self):
        if (self.template_game_board_design[2][0] == 1 and self.template_game_board_design[3][1] == 1 and self.template_game_board_design[4][2] == 1 and self.template_game_board_design[5][3] == 1): self.player1Score += 1
        if (self.template_game_board_design[1][0] == 1 and self.template_game_board_design[2][1] == 1 and self.template_game_board_design[3][2] == 1 and self.template_game_board_design[4][3] == 1): self.player1Score += 1
        if (self.template_game_board_design[2][1] == 1 and self.template_game_board_design[3][2] == 1 and self.template_game_board_design[4][3] == 1 and self.template_game_board_design[5][4] == 1): self.player1Score += 1
        if (self.template_game_board_design[0][0] == 1 and self.template_game_board_design[1][1] == 1 and self.template_game_board_design[2][2] == 1 and self.template_game_board_design[3][3] == 1): self.player1Score += 1
        if (self.template_game_board_design[1][1] == 1 and self.template_game_board_design[2][2] == 1 and self.template_game_board_design[3][3] == 1 and self.template_game_board_design[4][4] == 1): self.player1Score += 1
        if (self.template_game_board_design[2][2] == 1 and self.template_game_board_design[3][3] == 1 and self.template_game_board_design[4][4] == 1 and self.template_game_board_design[5][5] == 1): self.player1Score += 1
        if (self.template_game_board_design[0][1] == 1 and self.template_game_board_design[1][2] == 1 and self.template_game_board_design[2][3] == 1 and self.template_game_board_design[3][4] == 1): self.player1Score += 1
        if (self.template_game_board_design[1][2] == 1 and self.template_game_board_design[2][3] == 1 and self.template_game_board_design[3][4] == 1 and self.template_game_board_design[4][5] == 1): self.player1Score += 1
        if (self.template_game_board_design[2][3] == 1 and self.template_game_board_design[3][4] == 1 and self.template_game_board_design[4][5] == 1 and self.template_game_board_design[5][6] == 1): self.player1Score += 1
        if (self.template_game_board_design[0][2] == 1 and self.template_game_board_design[1][3] == 1 and self.template_game_board_design[2][4] == 1 and self.template_game_board_design[3][5] == 1): self.player1Score += 1
        if (self.template_game_board_design[1][3] == 1 and self.template_game_board_design[2][4] == 1 and self.template_game_board_design[3][5] == 1 and self.template_game_board_design[4][6] == 1): self.player1Score += 1
        if (self.template_game_board_design[0][3] == 1 and self.template_game_board_design[1][4] == 1 and self.template_game_board_design[2][5] == 1 and self.template_game_board_design[3][6] == 1): self.player1Score += 1
        if (self.template_game_board_design[0][3] == 1 and self.template_game_board_design[1][2] == 1 and self.template_game_board_design[2][1] == 1 and self.template_game_board_design[3][0] == 1): self.player1Score += 1
        if (self.template_game_board_design[0][4] == 1 and self.template_game_board_design[1][3] == 1 and self.template_game_board_design[2][2] == 1 and self.template_game_board_design[3][1] == 1): self.player1Score += 1
        if (self.template_game_board_design[1][3] == 1 and self.template_game_board_design[2][2] == 1 and self.template_game_board_design[3][1] == 1 and self.template_game_board_design[4][0] == 1): self.player1Score += 1
        if (self.template_game_board_design[0][5] == 1 and self.template_game_board_design[1][4] == 1 and self.template_game_board_design[2][3] == 1 and self.template_game_board_design[3][2] == 1): self.player1Score += 1
        if (self.template_game_board_design[1][4] == 1 and self.template_game_board_design[2][3] == 1 and self.template_game_board_design[3][2] == 1 and self.template_game_board_design[4][1] == 1): self.player1Score += 1
        if (self.template_game_board_design[2][3] == 1 and self.template_game_board_design[3][2] == 1 and self.template_game_board_design[4][1] == 1 and self.template_game_board_design[5][0] == 1): self.player1Score += 1
        if (self.template_game_board_design[0][6] == 1 and self.template_game_board_design[1][5] == 1 and self.template_game_board_design[2][4] == 1 and self.template_game_board_design[3][3] == 1): self.player1Score += 1
        if (self.template_game_board_design[1][5] == 1 and self.template_game_board_design[2][4] == 1 and self.template_game_board_design[3][3] == 1 and self.template_game_board_design[4][2] == 1): self.player1Score += 1
        if (self.template_game_board_design[2][4] == 1 and self.template_game_board_design[3][3] == 1 and self.template_game_board_design[4][2] == 1 and self.template_game_board_design[5][1] == 1): self.player1Score += 1
        if (self.template_game_board_design[1][6] == 1 and self.template_game_board_design[2][5] == 1 and self.template_game_board_design[3][4] == 1 and self.template_game_board_design[4][3] == 1): self.player1Score += 1
        if (self.template_game_board_design[2][5] == 1 and self.template_game_board_design[3][4] == 1 and self.template_game_board_design[4][3] == 1 and self.template_game_board_design[5][2] == 1): self.player1Score += 1
        if (self.template_game_board_design[2][6] == 1 and self.template_game_board_design[3][5] == 1 and self.template_game_board_design[4][4] == 1 and self.template_game_board_design[5][3] == 1): self.player1Score += 1
        if (self.template_game_board_design[2][0] == 2 and self.template_game_board_design[3][1] == 2 and self.template_game_board_design[4][2] == 2 and self.template_game_board_design[5][3] == 2): self.player2Score += 1
        if (self.template_game_board_design[1][0] == 2 and self.template_game_board_design[2][1] == 2 and self.template_game_board_design[3][2] == 2 and self.template_game_board_design[4][3] == 2): self.player2Score += 1
        if (self.template_game_board_design[2][1] == 2 and self.template_game_board_design[3][2] == 2 and self.template_game_board_design[4][3] == 2 and self.template_game_board_design[5][4] == 2): self.player2Score += 1
        if (self.template_game_board_design[0][0] == 2 and self.template_game_board_design[1][1] == 2 and self.template_game_board_design[2][2] == 2 and self.template_game_board_design[3][3] == 2): self.player2Score += 1
        if (self.template_game_board_design[1][1] == 2 and self.template_game_board_design[2][2] == 2 and self.template_game_board_design[3][3] == 2 and self.template_game_board_design[4][4] == 2): self.player2Score += 1
        if (self.template_game_board_design[2][2] == 2 and self.template_game_board_design[3][3] == 2 and self.template_game_board_design[4][4] == 2 and self.template_game_board_design[5][5] == 2): self.player2Score += 1
        if (self.template_game_board_design[0][1] == 2 and self.template_game_board_design[1][2] == 2 and self.template_game_board_design[2][3] == 2 and self.template_game_board_design[3][4] == 2): self.player2Score += 1
        if (self.template_game_board_design[1][2] == 2 and self.template_game_board_design[2][3] == 2 and self.template_game_board_design[3][4] == 2 and self.template_game_board_design[4][5] == 2): self.player2Score += 1
        if (self.template_game_board_design[2][3] == 2 and self.template_game_board_design[3][4] == 2 and self.template_game_board_design[4][5] == 2 and self.template_game_board_design[5][6] == 2): self.player2Score += 1
        if (self.template_game_board_design[0][2] == 2 and self.template_game_board_design[1][3] == 2 and self.template_game_board_design[2][4] == 2 and self.template_game_board_design[3][5] == 2): self.player2Score += 1
        if (self.template_game_board_design[1][3] == 2 and self.template_game_board_design[2][4] == 2 and self.template_game_board_design[3][5] == 2 and self.template_game_board_design[4][6] == 2): self.player2Score += 1
        if (self.template_game_board_design[0][3] == 2 and self.template_game_board_design[1][4] == 2 and self.template_game_board_design[2][5] == 2 and self.template_game_board_design[3][6] == 2): self.player2Score += 1
        if (self.template_game_board_design[0][3] == 2 and self.template_game_board_design[1][2] == 2 and self.template_game_board_design[2][1] == 2 and self.template_game_board_design[3][0] == 2): self.player2Score += 1
        if (self.template_game_board_design[0][4] == 2 and self.template_game_board_design[1][3] == 2 and self.template_game_board_design[2][2] == 2 and self.template_game_board_design[3][1] == 2): self.player2Score += 1
        if (self.template_game_board_design[1][3] == 2 and self.template_game_board_design[2][2] == 2 and self.template_game_board_design[3][1] == 2 and self.template_game_board_design[4][0] == 2): self.player2Score += 1
        if (self.template_game_board_design[0][5] == 2 and self.template_game_board_design[1][4] == 2 and self.template_game_board_design[2][3] == 2 and self.template_game_board_design[3][2] == 2): self.player2Score += 1
        if (self.template_game_board_design[1][4] == 2 and self.template_game_board_design[2][3] == 2 and self.template_game_board_design[3][2] == 2 and self.template_game_board_design[4][1] == 2): self.player2Score += 1
        if (self.template_game_board_design[2][3] == 2 and self.template_game_board_design[3][2] == 2 and self.template_game_board_design[4][1] == 2 and self.template_game_board_design[5][0] == 2): self.player2Score += 1
        if (self.template_game_board_design[0][6] == 2 and self.template_game_board_design[1][5] == 2 and self.template_game_board_design[2][4] == 2 and self.template_game_board_design[3][3] == 2): self.player2Score += 1
        if (self.template_game_board_design[1][5] == 2 and self.template_game_board_design[2][4] == 2 and self.template_game_board_design[3][3] == 2 and self.template_game_board_design[4][2] == 2): self.player2Score += 1
        if (self.template_game_board_design[2][4] == 2 and self.template_game_board_design[3][3] == 2 and self.template_game_board_design[4][2] == 2 and self.template_game_board_design[5][1] == 2): self.player2Score += 1
        if (self.template_game_board_design[1][6] == 2 and self.template_game_board_design[2][5] == 2 and self.template_game_board_design[3][4] == 2 and self.template_game_board_design[4][3] == 2): self.player2Score += 1
        if (self.template_game_board_design[2][5] == 2 and self.template_game_board_design[3][4] == 2 and self.template_game_board_design[4][3] == 2 and self.template_game_board_design[5][2] == 2): self.player2Score += 1
        if (self.template_game_board_design[2][6] == 2 and self.template_game_board_design[3][5] == 2 and self.template_game_board_design[4][4] == 2 and self.template_game_board_design[5][3] == 2): self.player2Score += 1

def game_interactive_mode(current_game_board, depth, computer):
    if current_game_board.pieceCount == 42:    
        current_game_board.count_total_score()
        if computer == 1:
            print('Score: Computer (Player 1) = %d, Human (Player 2) = %d\n' % (current_game_board.player1Score, current_game_board.player2Score))
            if current_game_board.player1Score < current_game_board.player2Score:print ("Congratulations, you WIN!")
            elif current_game_board.player1Score > current_game_board.player2Score:print ("Oops, you lost")
            else:print ("You were good. It is a draw")
        else:
            print('Score: Human (Player 1) = %d, Computer (Player 2) = %d\n' % (current_game_board.player1Score, current_game_board.player2Score))
            if current_game_board.player1Score > current_game_board.player2Score:print ("Congratulations, you WIN!")
            elif current_game_board.player1Score < current_game_board.player2Score: print ("Oops, you lost")
            else:print ("You were good. It is a draw")
        print ('BOARD FULL ..!')
        print()
        print("Game Over!")
        sys.exit(0)
    if depth == 0:
        print ('Give a depth greater than 0')
        sys.exit(0)
    if computer == current_game_board.currentTurn:
        outFile = "computer.txt"
        current_game_board.game_auto_play_using_AI(depth, computer)
        print (' -----------------')
        for i in range(6):print(current_game_board.template_game_board_design[i])
        print (' -----------------')
        current_game_board.count_total_score()
        if computer == 1:print('Score: Computer (Player 1) = %d, Human (Player 2) = %d\n' % (current_game_board.player1Score, current_game_board.player2Score))
        else:print('Score: Human (Player 1) = %d, Computer (Player 2) = %d\n' % (current_game_board.player1Score, current_game_board.player2Score))
    else:
        outFile = "human.txt"
        column = int(input("What column do you want to play at (from 1 to 7): "))
        if type(column) == int:
            if column > 0 and column <= 7:
                result = current_game_board.play_game_piece(column - 1)
                if not result:
                    print ("No moves on column "+ str(column) + ". Try Again")
                    game_interactive_mode(current_game_board, depth, computer)
                else:
                    if computer == 1:print('Score: Computer (Player 1) = %d, Human (Player 2) = %d\n' % (current_game_board.player1Score, current_game_board.player2Score))
                    else:print('Score: Human (Player 1) = %d, Computer (Player 2) = %d\n' % (current_game_board.player1Score, current_game_board.player2Score))
            else:
                print ("Invalid Move. Try Again")
                game_interactive_mode(current_game_board, depth, computer)
    current_game_board.gameFile = open(outFile, 'w')
    for row in current_game_board.template_game_board_design:
        current_game_board.gameFile.write(''.join(str(col) for col in row) + '\r\n')
    current_game_board.gameFile.write('%s\r\n' % str(current_game_board.currentTurn))
    nextGame = class_design_main_4connect_game()
    nextGame.template_game_board_design = copy.deepcopy(current_game_board.template_game_board_design)
    nextGame.pieceCount = current_game_board.pieceCount
    nextGame.evaluation = 0
    current_game_board.gameFile.close()
    if current_game_board.currentTurn == 1:
        nextGame.currentTurn = 2
        current_game_board.currentTurn = 2
    else:
        nextGame.currentTurn = 1
        current_game_board.currentTurn = 1
    game_interactive_mode(nextGame, depth, computer)

if __name__ == '__main__':
    start=time.time()
    argv = sys.argv
    if len(argv) != 5:
        print ('Four command-line arguments are needed:')
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)
    game_mode, inFile = argv[1:3]
    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)
    current_game_board = class_design_main_4connect_game() 
    current_game_board.gameFile = open(inFile, 'r')
    file_lines = current_game_board.gameFile.readlines()
    current_game_board.template_game_board_design = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    current_game_board.currentTurn = int(file_lines[-1][0])
    current_game_board.evaluation = 0
    current_game_board.gameFile.close()
    print ('\nMaxConnect-4 game\n')
    print ('Game state before move:')
    print (' -----------------')
    for i in range(6):print(current_game_board.template_game_board_design[i])
    print (' -----------------')
    current_game_board.pieceCount = sum(1 for row in current_game_board.template_game_board_design for piece in row if piece)
    current_game_board.count_total_score()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (current_game_board.player1Score, current_game_board.player2Score))
    print(argv)
    if game_mode == 'interactive':
        if argv[3] == "computer_next":
            computer = current_game_board.currentTurn
            print("1",computer)
        elif argv[3] == "human_next":
            if current_game_board.currentTurn == 1:computer = 2
            else:computer = 1
        game_interactive_mode(current_game_board, int(argv[4]),computer)
    else: 
        outFile = argv[3]
        current_game_board.gameFile = open(outFile, 'w')
        depth = int(argv[4])
        if current_game_board.pieceCount == 42:    
            print ('BOARD FULL\n\nGame Over!\n')
            sys.exit()
        if depth == 0:
            print ('Give a depth greater than 0')
            sys.exit(0)
        current_game_board.game_auto_play_using_AI(depth, current_game_board.currentTurn) 
        print ('Game Board State After Move:')
        print (' -----------------')
        for i in range(6):print(current_game_board.template_game_board_design[i])
        print (' -----------------')
        current_game_board.count_total_score()
        print('Score: Player 1 = %d, Player 2 = %d\n' % (current_game_board.player1Score, current_game_board.player2Score))
        if current_game_board.currentTurn == 1:
            current_game_board.currentTurn = 2
        elif current_game_board.currentTurn == 2:
            current_game_board.currentTurn = 1
        for row in current_game_board.template_game_board_design:
            current_game_board.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        current_game_board.gameFile.write('%s\r\n' % str(current_game_board.currentTurn))
        current_game_board.gameFile.close()    
    end=time.time()
    tt=end-start
    print("Total Execution time in seconds:",tt)