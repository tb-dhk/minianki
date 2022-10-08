import csv

deck = []
reader = csv.reader(open('.csv.mnak', 'r'))

# card structure
class flashcard:
  def __init__(term, defin, ls, ease, lastint, duedate):
    self.term = term
    self.defin = defin
    self.ls = ls
    self.ease = ease
    self.lastint = lastint
    self.duedate = duedate

# import csv into deck
for row in reader:
  ccs = row.split(", ")
deck.append(flashcard(ccs[0], ccs[1], ccs[2], ccs[3], ccs[4], ccs[5]))
