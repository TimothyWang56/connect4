from connect4v2 import Connect4
from players import Human_Player, AI_Player

# p1_chosen = False
# while not p1_chosen:
#     player_one = input("P1 - Human/AI: ").lower()
#     if player_one == "human":
#         p1 = Human_Player()
#         p1_chosen = True
#     elif player_one == "ai":
#         p1 = AI_Player()
#         p1_chosen = True
#     else:
#         print("Not a valid choice. Try again.")

# p2_chosen = False
# while not p2_chosen:
#     player_two = input("P2 - Human/AI: ").lower()
#     if player_two == "human":
#         p2 = Human_Player()
#         p2_chosen = True
#     elif player_two == "ai":
#         p2 = AI_Player()
#         p2_chosen = True
#     else:
#         print("Not a valid choice. Try again.")

game = Connect4()
game.run_game()
# game.play_game()