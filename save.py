import csv

def save():
  writer1 = txt.writer(open('txt.mnak', 'w'))
  writer2 = csv.writer(open('csv.mnak', 'w'))
  
  # save to 
  for x in deck:
    writer1.writerow(x.term + "  " + x.defin)
    writer2.writerow([x.term, x.defin, x.ls, x.ease, x.lastint, x.duedate])