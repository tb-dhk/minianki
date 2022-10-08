import os
import csv

def save(deck):
  writecsv = csv.writer(open(os.getcwd()+'/export/csv.mnak', 'w'))
  writetxt = open(os.getcwd()+'/export/readme.txt', 'w')

  # save to 
  for x in deck:
    writecsv.writerow([x.term, x.defin, x.ls, x.ease, x.lastint, x.duedate])
    writetxt.write(x.term + "    " + x.defin)
