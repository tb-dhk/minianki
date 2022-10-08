from init import deck
import csv

fileformat = input("would you like to export in .csv or .txt format?")
match fileformat:
  case ".csv":
    # if exporting to csv
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

  case ".txt":
    # if exporting to txt
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
