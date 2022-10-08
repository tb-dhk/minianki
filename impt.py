import datetime
import csv

def impt(deck):
  # make a deck
  reader = csv.reader(open('import.txt', 'r'))
  writer = csv.writer(open('csv.mnak', 'w'))
  
  # import new cards into deck
  for row in reader:
    writer.writerow([row[0], row[1], 0, 2.5, 0, datetime.date.today()])
