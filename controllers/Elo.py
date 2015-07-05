import webapp2
import math

from models.MemberModel import *

#returns tuple (Expected_win_rate_of_A, Expected_win_rate_of_B)
def calculate_expected(playerA_rank, playerB_rank):
  Expected_win_A = (1)/(1 + math.pow(10, ((playerB_rank - playerA_rank)/400.0)))
  Expected_win_B = (1)/(1 + math.pow(10, ((playerA_rank - playerB_rank)/400.0))) 
  return (Expected_win_A, Expected_win_B)

#return the new rank for a player
def calculate_new_rank(player_rank, expected, score):
  k = 24
  if(player_rank < 2100):
    k = 32
  if(player_rank > 2400):
    k = 16
  return player_rank + k*(score - expected)

#get the new rank and update the rank for each player based on who won or lost
def report_and_rank(winner, loser):
  expected_values = calculate_expected(winner.rank, loser.rank)
  winner_score = expected_values[0]
  loser_score = expected_values[1]
  winner.rank = int(round(calculate_new_rank(winner.rank, expected_values[0], 1), 0))
  loser.rank = int(round(calculate_new_rank(loser.rank, expected_values[1], 0), 0))