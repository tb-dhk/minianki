import datetime
import csv
import os
import random
import math
import pandas as pd

deck = []

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# import learning variables
class vari:
    def __init__(self, name, value, format, exp):
        self.name = name
        self.value = value
        self.format = format
        self.exp = exp

vars = []
variables = []

readvari = csv.reader(open(os.getcwd()+'/.userdata/learnvars.csv', 'r'))
for x in readvari:
  match x[2]: 
    case "float":
      vars.append(vari(x[0], float(x[1]), x[2], x[3]))
      variables.append([x[0], float(x[1]), x[2], x[3]])
    case "int": 
      vars.append(vari(x[0], int(x[1]), x[2], x[3]))
      variables.append([x[0], int(x[1]), x[2], x[3]])
    case "bool": 
      vars.append(vari(x[0], bool(x[1]), x[2], x[3]))
      variables.append([x[0], bool(x[1]), x[2], x[3]])  

# IMPT

def impt():
  # make a deck
  reader = open('import.txt', 'r').readlines()
  writer = csv.writer(open(os.getcwd()+'/.userdata/sched.mnak', 'a'))
  writer2 = csv.writer(open(os.getcwd()+'/.userdata/nsched.mnak', 'a'))
  impted = 0

  # import new cards into deck
  for row in reader:
    writer.writerow(row.strip().split("    ") + [0,variables[7][1],0,datetime.date.today(),False])
    writer2.writerow(row.strip().split("    "))
    impted += 1

  if impted == 0:
    print("    no cards imported. maybe check import.txt?")
  else:
    print(f"    {impted} card(s) imported.")

# INIT

# variables:
# learning steps (ls, range from 0-2)
# ease (the value that the intervals increase everytime "good" is picked, default 2.5x)
# last interval (the interval given for the last time the card was touched)
# due date (the next date at which the card will be reviewed)

# card structure
class flashcard:
  def __init__(self, term, defin, ls, ease, lastint, duedate, suspended):
    self.term = term
    self.defin = defin
    self.ls = ls
    self.ease = ease
    self.lastint = lastint
    self.duedate = duedate
    self.suspended = suspended

# initialisation function
def init(deck):
  reader = csv.reader(open(os.getcwd()+'/.userdata/sched.mnak', 'r'))  

  # import csv into deck
  for row in reader:
    if row == [] or row[0] == "" or len(row) != 7:
      print("empty card")
      continue
    for card in deck:
      if card.term == row[0]:
        deck.remove(card)
    deck.append(flashcard(row[0], row[1], int(row[2]), float(row[3]), float(row[4]), row[5], row[6]))
       
# LEARN

def learn(deck):
  # variables:
  # learning steps (intervals when a card is first learned, 1m 10m 1d by default)
  learnsteps = [str(variables[2][1]), str(variables[3][1]), variables[4][1]]
  # easy interval (time between picking easy and reviewing the card for the first time)
  easyint = variables[5][1]
  # easy bonus (bonus multiplier to ease when easy picked, default 1.3)
  easybonus = variables[8][1]
  # hard bonus (multiplier from last value, default 1.2)
  hardint = variables[9][1]
  
  # FUNCTIONS
  # function to generate intervals
  def genints(card):
    match int(card.ls):
      case 0:
        ints = [learnsteps[0], str(round((float(learnsteps[0])+float(learnsteps[1]))/2)), learnsteps[1], easyint]
      case 1:
        ints = learnsteps + [easyint]
      case 2:
        ints = ["10", math.ceil(card.lastint * hardint), math.ceil(card.lastint * card.ease), math.ceil(card.lastint * card.ease * easybonus)]
      case _:
        card.ls = 0
        ints = [learnsteps[0], str((int(learnsteps[0])+int(learnsteps[1]))/2), learnsteps[1], easyint]
    for x in ints:
      if type(x) == int and x > variables[6][1]:
        x = variables[6][1]
    return ints
  
  # function to print out intervals
  def printno(no):
    if type(no) == str:
      return(no + "m")
    elif type(no) == int:
      return(str(no) + "d")
  
  # function to schedule a new card
  def newint(card):
    # prompting user
    print("    ~~~~~~~~~~~~~~~~~~~~")
    input(f"    term: {card.term}\n    ")
    print(f"    definition: {card.defin}\n")
    print("    enter 1-4 for:" + 
    f"\n    1. again ({printno(genints(card)[0])})" + 
    f"\n    2. hard ({printno(genints(card)[1])})" +
    f"\n    3. good ({printno(genints(card)[2])})" +
    f"\n    4. easy ({printno(genints(card)[3])})\n")

    while 1:
      try:
        option = int(input("    "))-1 
      except:
        print("    invalid. try again.")
      else:
        if option < 1 or option > 4:
          print("    invalid. try again.")
        else:
          print("\n    card delayed by:", printno(genints(card)[option]), "\n")
          if type(genints(card)[option]) == str:
            # rescheduling card
            try:
              queue[int(genints(card)[option])].append(card)
            except:
              while len(queue) < int(genints(card)[option])+1:
                queue.append([])
              queue[-1].append(card)
            finally:
               queue[0].remove(card)
          else:
            # change data in deck
            for ocard in deck:
              if ocard.term == card.term:
                deck.remove(ocard) # remove old copy of card
            card.duedate = str(datetime.datetime(int(card.duedate[0:4]), int(card.duedate[5:7]), int(card.duedate[8:10])) + datetime.timedelta(days=genints(card)[option]))
            card.lastint = genints(card)[option]
            print("    1 card less!")
            deck.append(card) # add new copy of card
            queue[0].remove(card) # remove card from queue
          match option:
            case 0:
              card.ls = 0
            case 1:
              pass
            case 2:
              if card.ls < 2:
                card.ls += 1
            case 3:
              card.ls = 2
              card.ease *= easybonus
        break

# count cards
  def cardnum():
    count = 0
    for x in queue:
      count += len(x)
    return count
  init(deck)
  # SESSION
  # making queue
  init(deck)
  queue = [[]]
  newcount = 0
  revcount = 0
  for card in deck:
    if card.duedate == str(datetime.date.today()) and card.suspended == "False":
      queue[0].append(card)
      match card.ls:
        case 2:
          revcount += 1
        case _:
          newcount += 1
    if newcount >= variables[0][1] or revcount >= variables[1][1]:
      break
  if variables[10][1] == "True":
    random.shuffle(queue[0])
  
  # begin!
  print(f"    hello! welcome to your learning session.")
  
  if cardnum() == 0:
    print("    no cards today. maybe check import.txt?")
  else:
    print(f"    today's card count: {cardnum()}")

  while queue != []:
    for card in queue[0]:
      newint(card)
      if cardnum() > 0:
        print("    remaining cards:", cardnum())
        if input("    continue? (Y/n)") == "n":
          break
      else:
        print("    good job! you finished the deck.")
    if queue[0] == []:
      queue.pop(0)

# SAVE

def save(deck):
  writecsv = csv.writer(open(os.getcwd()+'/.userdata/sched.mnak', 'w'))
  writetxt = open(os.getcwd()+'/.userdata/nsched.mnak', 'w')
  saved = 0

  # save to 
  for x in deck:
    writecsv.writerow([x.term, x.defin.strip(), x.ls, x.ease, x.lastint, x.duedate, x.suspended])
    writetxt.write(x.term + "    " + x.defin)
    saved += 1

  print(f"    {saved} card(s) saved.")

# SETTINGS

def settings():
  while 1: 
    string = "\n    variables: \n"
    for x in range(len(vars)):
      varia = vars[x]
      string = string + f"    ~~~~~~~~~~~~~~~~~~~~\n    {varia.name} ({str(x)}): {str(varia.value)}  \n    {varia.exp } \n" 
    string = string + "    ~~~~~~~~~~~~~~~~~~~~\n"
    print("    " + string)
    comm = input("    enter any number to change the value of its corresponding variable or 'exit' to save and exit settings.\n    _______\n    >>> ")
    match comm:
      case 'exit':
        break
      case _:
        try:
          comm = int(comm)
          varia = vars[comm]
        except:
          print("    invalid command. try again!")
        else:
          print("    " + varia.name + " (" + str(int(comm)) + ") - " + varia.exp + "\n    current value: " + str(varia.value))
          while 1:
            newval = input("    enter new value: ")
            try:
              match varia.format:
                case "float":
                  newval = float(newval)
                case "int":
                  newval = int(newval)
                case "bool":
                  match newval:
                    case "False":
                      newval = False
                    case "True":
                      newval = True
                    case _:
                      raise TypeError('value could not be converted to bool')
            except:
              print("    invalid. try again")
            else:
              varia.value = newval
              break
          writevari = csv.writer(open(os.getcwd()+'/.userdata/learnvars.csv', 'w'))
          for x in vars:
            writevari.writerow([x.name, x.value, x.format, x.exp])

# GUIDE
def guide():
  guidelist = {
    "faq" : "see frequently asked questions.",
    "imexportguide" : "see instructions on how to import and export data."
  }
  for x in guidelist:
    print("    " + x + ": " + guidelist[x])
  while 1:
    comm = input("\n    enter the name of the guide you want to see, 'help' to see the list of guides again or 'exit' to exit guides.\n    ______\n    >>> ")
    match comm:
      case "help":
        for x in guidelist:
          print("    " + x + ": " + guidelist[x])
      case "exit":
        break
      case _:
        try:
          f = open(os.getcwd()+'/.guides/'+comm+'.txt', 'r')
        except:
          print("    invalid. try again")
        else:
          print("\n    ~~~~~~~~~~~~~~~~~~~~")
          for line in f.readlines():
            print("    " + line)
          f.close()
          print("    ~~~~~~~~~~~~~~~~~~~~")
