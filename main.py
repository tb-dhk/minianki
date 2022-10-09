import minianki
#from impt import impt
#from init import init
#from learn import learn
#from save import save
#from settings import settings
import os

deck = []

# learning variables:
# learning steps (intervals when a card is first learned, 1m 10m 1d by default)
learnsteps = ["1", "10", 1]
# easy interval (time between picking easy and reviewing the card for the first time)
easyint = 4
# easy bonus (bonus multiplier to ease when easy picked, default 1.3)
easybonus = 1.3
# hard bonus (multiplier from last value, default 1.2)
hardint = 1.2

def help():
  print("""
  list of commands:
  import: import cards in import.txt to the main database.
  export: view instructions on how to export.
  init: initialise or synchronise the program with the database.
  learn: an anki-esque learning session.
  save: save your progress/scheduling and cards to the database.
  settings: customise learning variables. (work in progress)
  help: view this message again.
  exit (or Ctrl+C): end the program.
  """)
  
print("""welcome to minianki!""")
help()

# console-like env
while 1:
  command = input(">>> ")
  match command:
    case "import":
      minianki.impt(deck)
    case "init":
      minianki.init(deck)
    case "learn":
      minianki.learn(deck)
    case "save":
      minianki.save(deck)
    case "settings":
      minianki.settings()
    case "guide":
      minianki.guide()
    case "help":
      help()
    case "shua":
      print("hewwo :>")
    case "kiki":
      print("<3")
    case "":
      pass
    case " ":
      pass
    case "exit":
      print
      break
    case _:
      "invalid command. try again!"
