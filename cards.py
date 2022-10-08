import datetime

# variables:
# learning steps (ls, range from 0-2)
# ease (the value that the intervals increase everytime "good" is picked, default 2.5x)
# last interval (the interval given for the last time the card was touched)
# due date (the next date at which the card will be reviewed)

class card:
  def __init__(term, defin, ls, ease, lastint, duedate):
    self.term = term
    self.defin = defin
    self.ls = ls
    self.ease = ease
    self.lastint = lastint
    self.duedate = duedate

# sample deck
# deck = [card("term1", "defin1", 0, 2.5, 0, date(2023, 1, 1)), 
#         card("term2", "defin2", 2, 2.5, 3, date(2023, 1, 1)), 
#         card("term3", "defin3", 2, 2.5, 4, date(2023, 1, 1))]
