import tkinter as tk
import random


# mainīt virknes garumu - 383 rinda
class Node:  # klase lai izveidot koka elementu (root, child)
    def __init__(self, state, is_max, player_symbol, depth):  # ,comp_points
        self.player_symbol = player_symbol
        self.state = state  # state būtībā ir char masīvs no simbolu virknes
        self.is_max = is_max  # kad veidojam node padodam True/False(speletājs ir maksimizētājs vai ne)
        self.children = []  # saglabājam virsotnes nākamo līmeni
        self.computer_points_n = None
        self.depth = depth


class GameTree:  # klase lai ģenerēt koku
    def __init__(self, root_state, depth,
                 player):  # konstruktors, kas veido GameTree objektus, # root_state - sākuma simbolu virkne
        self.computer_points = 0
        self.human_points = 0
        self.arr_for_comp_points = {}  # vārdnīca, glabājam datora iegūstamos punktus par gājienu
        self.nodes = []  # visas virsotnes
        self.root = Node(root_state, True, False,
                         depth)  # veido koka sakni, True nozime ka pirmais speletajs ir maksimizētajs
        self.nodes.append(self.root)  # pievienojam kokam sakni
        self.turn = 0  # spēli uzsāk spēlētājs ar O
        self.player = player
        self.make_children(self.root, depth, self.turn)  # izsaucam make_ch lai izveidot koku
        # game.print_tree(self.root, 0)

    def make_children(self, node, depth, turn):  # izveidojam virsotnes / koku
        # print(depth)  # depth parametrs katru līmeni samazinās
        if depth == 0:
            return
        states = self.generate_possible_states(list(node.state), turn)
        for state in states:  # katrā iterācijā dziļumu samazinam
            child = Node(list(state), not node.is_max, not node.player_symbol, depth)  # veidojam Node klases objektu
            node.children.append(child)
            child.player_symbol = not node.player_symbol
            self.make_children(child, depth - 1, (
                        turn + 1) % 2)  # rekursīvi izsaucam make_children - (depth - 1) un arī mainam spēlētāju -  (turn + 1) % 2

    def update_turn(self, turn):
        self.turn = turn

    def generate_possible_states(self, current_state,
                                 turn):  # metode ģenerē visus iespējamos stāvokļus no dotas virknes atkarībā no spelētāja
        possible_states = []
        player_symbol = 'O' if turn % 2 == 0 else 'X'
        opponent_symbol = 'X' if turn % 2 == 0 else 'O'

        for i in range(len(current_state) - 1):

            if current_state[i:i + 2] == [opponent_symbol, opponent_symbol]:  # izgriež no masīva daļu
                new_state = current_state[:i] + [player_symbol] + current_state[
                                                                  i + 2:]  # līdz i viss paliek, tālāk samaina elementus
                possible_states.append(new_state)
                self.computer_points = 2  # punkti vārdnīcai
                # print(new_state, self.computer_points)
                self.arr_for_comp_points[''.join(new_state)] = self.computer_points

            if current_state[i:i + 2] == [opponent_symbol, player_symbol]:
                new_state = current_state[:i] + [player_symbol] + current_state[i + 2:]
                possible_states.append(new_state)
                self.human_points = -1  # punkti vārdnīcai
                # print(new_state, self.computer_points)
                self.arr_for_comp_points[''.join(new_state)] = self.human_points  # pievienojam

        return possible_states

    def minimax(self, node, depth, is_max, turn, current_player):

        if depth == 0 or len(node.children) == 0:
            return self.evaluate(node, turn, current_player)
        for ch in node.children:
            # print(ch.state)
            self.evaluate(ch, self.turn, current_player)
            # print(ch.state)

        if is_max:
            max_eval = float('-inf')  # vismazākais iespējamais skaitlis
            for child in node.children:
                eval = self.minimax(child, depth - 1, False, turn, current_player)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for child in node.children:
                eval = self.minimax(child, depth - 1, True, turn, current_player)
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate(self, node, turn, current_player):  # nosakam labāko virsotni
        h_eval = 0
        if turn and current_player:  # player o 1 and its comp
            if list(node.state)[0] == 'X':  # ja pirmais elements O
                h_eval += 1
            if game.computer >= game.human:  # ja datoram vairāk punktu nekā cilvēkam
                h_eval += 2
            return h_eval

        if not turn and current_player:  # player x and its computer
            if list(node.state)[0] == 'O':
                h_eval += 1
            if game.human >= game.computer:
                h_eval += 2
            return h_eval

    def find_node_by_state(self, node, target_state):

        if node is None:
            return None

        if str(node.state) == str(target_state):
            return node

        for child in node.children:
            result = self.find_node_by_state(child, target_state)
            if result:
                return result

        return None


class Game:

    def __init__(self):

        self.symbols_array = None
        self.game_tree = None
        self.turn = 0
        self.human = 0
        self.computer = 0
        self.current_player = None
        self.moves_count = 0
        self.found_node = None

        self.root = tk.Tk()
        self.root.title("13.komandas spēle")
        self.root.geometry("600x800")
        self.root.configure(bg="#B5C2B7")

        self.label_computer = tk.Label(self.root, text="Choose the first player")
        self.label_computer.configure(bg="#B5C2B7")
        self.label_computer.pack()

        self.button_computer = tk.Button(self.root, text="Computer", command=self.set_computer_first)
        self.button_computer.configure(bg="#2D2327", fg="#B5C2B7")
        self.button_computer.pack()

        self.button_human = tk.Button(self.root, text="Human", command=self.set_player_first)

        self.button_human.configure(bg="#2D2327", fg="#B5C2B7")
        self.button_human.pack()
        #
        # self.label_choose = tk.Label(self.root, text="Choose the algorithm")
        # self.label_choose.configure(bg="#B5C2B7")
        # self.label_choose.pack()

        # self.button_choose_minmax = tk.Button(self.root, text="Minimax", command=self.select_minimax)
        # self.button_choose_minmax.configure(bg="#2D2327", fg="#B5C2B7")
        # self.button_choose_minmax.pack()

        # self.button_choose_alfabeta = tk.Button(self.root, text="Alfa-Beta", command=self.select_alfabeta)
        # self.button_choose_alfabeta.configure(bg="#2D2327", fg="#B5C2B7")
        # self.button_choose_alfabeta.pack()

        self.human_label = tk.Label(self.root, text="Human has " + str(self.human) + " points")
        self.human_label.configure(bg="#B5C2B7")
        self.human_label.pack()

        self.computer_label = tk.Label(self.root, text="Computer has " + str(self.computer) + " points")
        self.computer_label.configure(bg="#B5C2B7")
        self.computer_label.pack()

        self.generate_button = tk.Button(self.root, text="Generate", command=self.generate_handler)

        self.generate_button.configure(bg="#2D2327", fg="#B5C2B7")
        self.generate_button.pack()
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.configure(bg="#B5C2B7")
        self.result_label.pack()

        self.error_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.error_label.configure(bg="#B5C2B7")
        self.error_label.pack()

        self.cm = tk.Label(self.root, text="", font=("Arial", 14))
        self.cm.configure(bg="#B5C2B7")
        self.cm.pack()

        self.pl = tk.Label(self.root, text="", font=("Arial", 14))
        self.pl.configure(bg="#B5C2B7")
        self.pl.pack()

        self.win = tk.Label(self.root, text="", font=("Arial", 14))
        self.win.configure(bg="#B5C2B7")
        self.win.pack()

        self.papildus_lauki = []

    def update_points(self):
        self.human_label.configure(text="Human has " + str(self.human) + " points")
        self.computer_label.configure(text="Computer has " + str(self.computer) + " points")

    def generate_and_display(self, length):
        try:
            length = int(length)  # parbauda vai ir skaitlis
        except ValueError:
            self.result_label.config(text="You must enter an integer!")
            return

        if 15 <= length <= 25:
            self.symbols = ''.join([random.choice(['X', 'O']) for _ in range(
                length)])  # tagad virkne generējas šeit, jo iepriekšēja vietā length parametrs nemainījās
            # un vienmēr ģenerējās virkne ar 20 elementiem(izsaukums programmas beigās). Tagad ņem parametru no ievades
            self.result_label.config(text="Generated string: " + ''.join(self.symbols))
            self.symbols_array = Node(self.symbols, True, True, 0)
            if not self.papildus_lauki and not self.game_tree:
                self.game_tree = GameTree(self.symbols, 3, self.turn)  # 3 norāda dziļumu
                self.create_fields_for_move()  # lai cilvēks var ievadīt vērtības
                self.current_player = True  # comp
                self.computer_move(True, self.game_tree.root, self.turn, self.current_player)

        else:
            self.result_label.config(text="Number must be between 15 and 25.")

    def create_fields_for_move(self):
        self.input_label2 = tk.Label(self.root, text="Enter the number of the first element")
        self.input_label2.configure(bg="#B5C2B7")
        self.input_label2.pack()

        self.entry2 = tk.Entry(self.root)
        self.entry2.pack(pady=20)
        self.papildus_lauki.append(self.entry2)

        self.input_label3 = tk.Label(self.root, text="Enter the number of the second element")
        self.input_label3.configure(bg="#B5C2B7")
        self.input_label3.pack()

        self.entry3 = tk.Entry(self.root)
        self.entry3.pack(pady=20)
        self.papildus_lauki.append(self.entry3)

        self.button2 = tk.Button(self.root, text="Replace", command=self.replace_elements)
        self.button2.configure(bg="#2D2327", fg="#B5C2B7")
        self.button2.pack()
        self.papildus_lauki.append(self.button2)

    def points_result(self, kartas_nr1, kartas_nr2):
        # Pārbaudīt, vai gājiens ir derīgs
        if kartas_nr1 == kartas_nr2:
            return False

        if self.symbols_array.state[kartas_nr1] == 'O' and self.symbols_array.state[kartas_nr2] == 'O':
            self.human += 2
        elif self.symbols_array.state[kartas_nr1] == 'O' and self.symbols_array.state[kartas_nr2] == 'X':
            self.computer -= 1
        self.update_points()

    def computer_move(self, is_max, node, turn, current_player):

        # for ch in node.children:
        #   print(ch.state,"ch st")

        best_move = None
        if is_max:
            best_score = float('-inf')  # maksimizētājam
        else:
            best_score = float('inf')  # minimizētājam
        if (len(node.children)) == 0:  # kad beidzas children
            best_move = node
            self.cm.config(text="cm no childrens: " + ''.join(best_move.state))
        else:

            for child in node.children:
                score = self.game_tree.minimax(child, 3, False, turn, current_player)

                # ja vērtējums labāks nekā esošais, tad atjaunot labāko gājienu un vērtējumu

                if is_max:
                    if score > best_score:
                        best_score = score
                        best_move = child

                else:
                    if score < best_score:
                        best_score = score
                        best_move = child

            self.symbols_array = best_move
            # Atjaunojiet esošo virkni ar jauno virkni
            self.cm.config(text="Computer made a move: " + ''.join(best_move.state))
        self.game_tree.generate_possible_states(node.state, self.turn)

        for state, points in self.game_tree.arr_for_comp_points.items():
            if ''.join(state) == ''.join(best_move.state):
                if points == -1:
                    self.human -= 1
                else:
                    self.computer += 2
        self.update_points()
        self.turn = (self.turn + 1) % 2
        return best_move

    def replace_elements(self):
        # kods, kas aizvietos divus elementus
        # parveido ievadito par skaitli un -1, jo masīvā elementi sākas no 0
        try:
            kartas_nr1 = int(self.entry2.get()) - 1
            kartas_nr2 = int(self.entry3.get()) - 1
        except ValueError:
            self.error_label.config(text="You must enter an integer!")
            return

        if kartas_nr1 == kartas_nr2:
            self.error_label.config(text="Error, can't change the elements!")
            return
        self.found_node = self.game_tree.find_node_by_state(self.game_tree.root, self.symbols_array.state)
        if kartas_nr1 >= 0 and kartas_nr1 < len(self.symbols_array.state) and kartas_nr2 >= 0 and kartas_nr2 < len(
                self.symbols_array.state) and abs(
            kartas_nr1 - kartas_nr2) == 1:  # pārbauda vai elementi ir blakus un vai lielāks pa 0
            if self.symbols_array.state[kartas_nr1] == 'X' and self.symbols_array.state[kartas_nr2] == 'X' or \
                    self.symbols_array.state[kartas_nr1] == 'X' and self.symbols_array.state[kartas_nr2] == 'O':
                self.points_result(kartas_nr1, kartas_nr2)  # izsauc metodi, kas aprēķina spēlētāju punktus
                self.symbols_array.state[kartas_nr1] = 'O'  # aizvieto elementu
                del self.symbols_array.state[kartas_nr2]
                next_string = ''.join(self.symbols_array.state)
                self.result_label.configure(text="New string: " + next_string)
                self.update_points()  # Lai rāda, cik katram punktu, vienmēr
                self.clear_error_message()

                self.entry2.delete(0, tk.END)
                self.entry3.delete(0, tk.END)

                if self.symbols_array.depth == 1:
                    self.found_node = self.game_tree.find_node_by_state(self.game_tree.root, self.symbols_array.state)
                    self.game_tree = GameTree(self.found_node.state, 3, self.turn)
                    self.computer_move(True, self.found_node, self.turn, self.current_player)
                    self.update_points()
                    return

                self.computer_move(True, self.symbols_array, self.turn, self.current_player)


            elif self.symbols_array.state[kartas_nr1] == 'O' and self.symbols_array.state[kartas_nr2] == 'O' or \
                    self.symbols_array.state[kartas_nr1] == 'O' and self.symbols_array.state[kartas_nr2] == 'X':
                self.points_result(kartas_nr1, kartas_nr2)  # izsauc metodi, kas aprēķina spēlētāju punktus
                self.symbols_array.state[kartas_nr1] = 'X'
                del self.symbols_array.state[kartas_nr2]

                next_string = ''.join(self.symbols_array.state)
                self.result_label.configure(text="New string: " + next_string)
                self.update_points()
                self.clear_error_message()
                # notīra ievades laukus
                self.entry2.delete(0, tk.END)
                self.entry3.delete(0, tk.END)

                if self.symbols_array.depth == 1:
                    self.game_tree = GameTree(self.symbols_array.state, 3, self.turn)
                    self.found_node = self.game_tree.find_node_by_state(self.game_tree.root, self.symbols_array.state)
                    self.computer_move(True, self.found_node, self.turn, self.current_player)
                    self.update_points()
                    return

                self.computer_move(True, self.symbols_array, self.turn, self.current_player)
            else:
                self.result_label.configure(text="error")
        else:
            self.error_label.config(text="Error, can't change the elements!")
        self.turn = (self.turn + 1) % 2  # mainam spēlētāju
        self.update_points()

        self.computer_move(True, self.symbols_array, self.turn, self.current_player)

    def set_computer_first(self):  # nospiežot pogu computer iestata, ka dators sāks spēli
        self.button_computer.config(state="disabled", bg="#A9A9A9")
        self.button_human.config(state="normal", bg="#2D2327")

        self.generate_and_display(random.randint(15, 25))

    def set_player_first(self):  # nospiežot pogu human iestata, ka cilvēks sāks spēli
        self.button_human.config(state="disabled", bg="#A9A9A9")
        self.button_computer.config(state="normal", bg="#2D2327")

        entry_label = tk.Label(self.root,
                               text="Enter a number between 15 and 25:")  # izvada virknes garuma ievades lauku
        entry_label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()

    def generate_handler(self):
        length = int(self.entry.get())
        self.generate_and_display(length)

    def human_handler(self):
        self.generate_button.pack()

    # def select_minimax(self):  # pogas algoritma izvēlei
    #     self.button_choose_minmax.config(state="disabled", bg="#A9A9A9")
    #     self.button_choose_alfabeta.config(state="normal", bg="#2D2327")

    # def select_alfabeta(self):
    #     self.button_choose_alfabeta.config(state="disabled", bg="#A9A9A9")
    #     self.button_choose_minmax.config(state="normal", bg="#2D2327")

    def is_over(self):
        # Pārbaude vai spēle ir beigusies
        return len(self.symbols) <= 1

    def play(self):
        self.root.mainloop()

    # def print_tree(self, node,
    #                depth=0):  # izprintē koku konsolē (izprintē pēc kārtas katru iespējamo stāvokli ko var iegūt no saknes un tās pēctečus)
    #     print("  " * depth + str(node.state))
    #     for child in node.children:
    #         self.print_tree(child, depth + 1)

    def clear_error_message(self):
        self.error_label.config(text="")


game = Game()
game.play()
