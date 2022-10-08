from init import deck
import datetime
import csv

# variables:
# learning steps (ls, range from 0-2)
# ease (the value that the intervals increase everytime "good" is picked, default 2.5x)
# last interval (the interval given for the last time the card was touched)
# due date (the next date at which the card will be reviewed)

# card structure
class card:
  def __init__(term, defin, ls, ease, lastint, duedate):
    self.term = term
    self.defin = defin
    self.ls = ls
    self.ease = ease
    self.lastint = lastint
    self.duedate = duedate

# make a deck
deck = []
reader = csv.reader(open('import.txt', 'r'))
writer = csv.writer(open('.csv.mnak', 'w'))


# import new cards into deck
for row in reader:
  ccs = row.split("  ")
  writer.writerow(ccs[0], ccs[1], 0, 2.5, 0, datetime.today())
