from learn import deck
import csv

# card structure
  class flashcard:
    def __init__(term, defin, ls, ease, lastint, duedate):
      self.term = term
      self.defin = defin
      self.ls = ls
      self.ease = ease
      self.lastint = lastint
      self.duedate = duedate

# initialisation function
def init(deck):
  reader = csv.reader(open('.csv.mnak', 'r')) 
  
  # import csv into deck
  for row in reader:
    fc = row.split(", ")
    for ocard in deck:
      if ocard.term == fc[0]:
        deck.remove(ocard) # remove old copy of card
    deck.append(flashcard(fc[0], fc[1], fc[2], fc[3], fc[4], fc[5]))
