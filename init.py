import os
import csv

# variables:
# learning steps (ls, range from 0-2)
# ease (the value that the intervals increase everytime "good" is picked, default 2.5x)
# last interval (the interval given for the last time the card was touched)
# due date (the next date at which the card will be reviewed)

# card structure
class flashcard:
  def __init__(self, term, defin, ls, ease, lastint, duedate):
    self.term = term
    self.defin = defin
    self.ls = ls
    self.ease = ease
    self.lastint = lastint
    self.duedate = duedate

# initialisation function
def init(deck):
  reader = csv.reader(open(os.getcwd()+'/export/csv.mnak', 'r')) 
  
  # import csv into deck
  for row in reader:
    for ocard in deck:
      if ocard.term == row[0]:
        deck.remove(ocard) # remove old copy of card
    deck.append(flashcard(row[0], row[1], int(row[2]), float(row[3]), float(row[4]), row[5]))
