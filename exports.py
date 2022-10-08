from learn import deck
import csv

fileformat = input("would you like to export with scheduling? Y/n")
match fileformat:
  case ".txt":
    # if without scheduling
    reader = csv.reader(open('.txt.mnak', 'w'))
    writer = csv.writer(open('.txt.mnak', 'w'))
    
    # check if exports file has any data
    try:
      reader[0]
    except:
      writer.writerow(["term", "defin"])
    finally:
      for x in deck:
        writer.writerow([x.term, x.defin])

  case _:
    # if with scheduling
    reader = csv.reader(open('.csv.mnak', 'w'))
    writer = csv.writer(open('.csv.mnak', 'w'))
    
    # check if exports file has any data
    try:
      reader[0]
    except:
      writer.writerow(["term", "defin", "ls", "ease", "lastint", "duedate"])
    finally:
      for x in deck:
        writer.writerow([x.term, x.defin, x.ls, x.ease, x.lastint, x.duedate])
