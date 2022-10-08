import datetime
import init
from math import ceil

def learn(deck):
  # variables:
  # learning steps (intervals when a card is first learned, 1m 10m 1d by default)
  learnsteps = ["1", "10", 1]
  # easy interval (time between picking easy and reviewing the card for the first time)
  easyint = 4
  # easy bonus (bonus multiplier to ease when easy picked, default 1.3)
  easybonus = 1.3
  # hard bonus (multiplier from last value, default 1.2)
  hardint = 1.2
  
  # FUNCTIONS
  # function to generate intervals
  def genints(card):
    match card.ls:
      case 0:
        return ["1", "6", "10", easyint]
      case 1:
        return ["1", "10", 1, easyint]
      case 2:
        return ["10", ceil(card.lastint * card.ease, 0), ceil(card.lastint * card.ease), ceil(card.lastint * card.ease * card.easybonus)]
  
  # function to print out intervals
  def printno(no):
    if type(no) == str:
      return(no + "m")
    elif type(no) == int:
      return(str(no) + "d")
  
  # function to schedule a new card
  def newint(card):
    # prompting user
    print("~~~~~~~~~~~~~~~~~~~~")
    input(f"term: {card.term}\n")
    print(f"definition: {card.defin}\n")
    option = int(input("enter 1-4 for:" + 
    f"\n1. again ({printno(genints(card)[0])})" + 
    f"\n2. hard ({printno(genints(card)[1])})" +
    f"\n3. good ({printno(genints(card)[2])})" +
    f"\n4. easy ({printno(genints(card)[3])})\n\n"))-1
    print("card delayed by:", printno(genints(card)[option]))
    if type(genints(card)[option]) == str:
      # rescheduling card
      try:
        queue[int(genints(card)[option])].append(card)
      except:
        while len(queue) < int(genints(card)[option])+1:
          queue.append([])
      queue[-1].append(card)
    else:
      # change data in deck
      for ocard in deck:
        if ocard.term == card.term:
          deck.remove(ocard) # remove old copy of card
      card.duedate = str(datetime.datetime(int(card.duedate[0:4]), int(card.duedate[5:7]), int(card.duedate[8:10])) + datetime.timedelta(days=genints(card)[option]))
      print("1 card less!")
      deck.append(card) # add new copy of card
    queue[0].remove(card) # remove card from queue
    match option:
        case 0:
            card.ls = 0
        case 1:
            pass
        case 2:
            card.ls += 1
        case 3:
            card.ls = 2
    
  # count cards
  def cardnum():
    count = 0
    for x in queue:
      count += len(x)
    return count


  # SESSION
  # making queue
  queue = [[]]
  for card in deck:
    if card.duedate == str(datetime.date.today()):
      queue[0].append(card)
  
  # begin!
  print(f"hello! welcome to your learning session.\ntoday's card count: {cardnum()}.")
  
  while queue != []:
    for card in queue[0]:
      newint(card)
      if cardnum() > 0:
        print("remaining cards:", cardnum())
        if input("continue? (Y/n)") == "n":
          break
      else:
        print("good job! you finished the deck.")
    if queue[0] == []:
      queue.pop(0)
