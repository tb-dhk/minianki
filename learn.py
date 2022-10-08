from init import card
from main import deck
import math

# variables:
# learning steps (intervals when a card is first learned, 1m 10m 1d by default)
learnsteps = ["1", "10", 1]
# easy interval (time between picking easy and reviewing the card for the first time)
easyint = 4
# easy bonus (bonus multiplier to ease when easy picked, default 1.3)
easybonus = 1.3
# hard bonus (multiplier from last value, default 1.2)
hardint = 1.2

# FUNCTIONS
# function to generate intervals
def genints(card):
  match card.ls:
    case 0:
      return ["1", "6", "10", easyint]
    case 1:
      return ["1", "10", 1, easyint]
    case 2:
      return ["10", ceil(card.lastint * card.ease, 0), ceil(card.lastint * card.ease), ceil(card.lastint * card.ease * card.easybonus)]

# function to print out intervals
def printno(no):
  match type(no):
    case str:
      return(no + "m")
    case int:
      return(str(no) + "d")

# function to schedule a new card
def newint(card):
  # prompting user
  input(card.term)
  print(card.defin)
  option = input(f"""
  enter 1-4 for:
  1. again ({printno(genints(card)[0])})
  2. hard ({printno(genints(card)[1])})
  3. good ({printno(genints(card)[2])})
  4. easy ({printno(genints(card)[3])})
  """)
  if type(genints(card)[option]) == str:
    # rescheduling card
    try:
      queue[int(genints(card)[option])].append(card)
    except:
      while len(queue) < int(genints(card)[option])+1:
        queue.append([])
      queue[-1].append(card)
  else:
    # change data in deck
    for ocard in deck:
      if ocard.term == card.term:
        deck.remove(ocard) # remove old copy of card
    deck.append(card) # add new copy of card
    queue[0].remove(card) # remove card from queue

# SESSION
# making queue
queue = [[]]
for card in deck:
  if card.duedate = date.today():
    queue.append(card)

# begin!
while queue != []:
  for card in queue[0]:
    newint(card)
  if queue[0] == []:
    queue.pop(0)
