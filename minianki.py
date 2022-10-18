import datetime
import csv
import os
import random
import math
import subprocess
from colors import color
import plotext as plt

os.chdir(os.path.dirname(os.path.realpath(__file__)))

print("\ninitialising minianki...")
subprocess.run(["git", "init"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["git", "branch", "-m", "main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["git", "update-index", "--assume-unchanged", ".mnakdata/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.run(["git", "remote", "add", "minianki", "https://github.com/shuu-wasseo/minianki"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("")

verno =  "1.2"

# import learning variables
class vari:
    def __init__(self, name, value, format, exp):
        self.name = name
        self.value = value
        self.format = format
        self.exp = exp

vars = []
variables = []

readvari = csv.reader(open(os.getcwd()+'/.mnakdata/config.mnak', 'r'))
for x in readvari:
    match x[2]: 
        case "float":
            vars.append(vari(x[0], float(x[1]), x[2], x[3]))
            variables.append([x[0], float(x[1]), x[2], x[3]])
        case "int": 
            vars.append(vari(x[0], int(x[1]), x[2], x[3]))
            variables.append([x[0], int(x[1]), x[2], x[3]])
        case "bool":
            if x[1] == "True":
                vars.append(vari(x[0], True, x[2], x[3]))
                variables.append([x[0], True, x[2], x[3]])  
            if x[1] == "False":
                vars.append(vari(x[0], False, x[2], x[3]))
                variables.append([x[0], False, x[2], x[3]])


prefs = {}

readprefs = csv.reader(open(os.getcwd()+'/.mnakdata/prefs.mnak'))
for x in readprefs:
    prefs[x[0]] = x[1]

# INIT

# variables:
# learning steps (ls, range from 0-2)
# ease (the value that the intervals increase everytime "good" is picked, default 2.5x)
# last interval (the interval given for the last time the card was touched)
# due date (the next date at which the card will be reviewed)

# card structure
class flashcard:
    def __init__(self, term, defin, ls, ease, lastint, duedate, suspended, againcount, status, tags, flags):
        self.term = term
        self.defin = defin
        self.ls = ls
        self.ease = ease
        self.lastint = lastint
        self.duedate = duedate
        self.suspended = suspended
        self.againcount = againcount
        self.status = status
        self.tags = tags
        self.flags = flags

# initialisation function
stat = []

def init(deck):
    readdeck = csv.reader(open(os.getcwd()+'/.mnakdata/sched.mnak', 'r'))
    readstats = csv.reader(open(os.getcwd()+'/.mnakdata/stats.mnak', 'r'))
    # import csv into deck
    defaultcard = ["","",0,variables[7][1],0,datetime.datetime.today(),False,0,"new",[],[]] 
    for row in readdeck:
        if row == [] or row[0] == "":
            continue
        else:
            if len(row) < len(defaultcard):
                row = row + defaultcard[len(row):] 
            else:
                for card in deck:
                    if type(card.duedate) == str:
                        card.duedate = datetime.datetime.fromisoformat(card.duedate)
                    try:
                        card.duedate = card.duedate.date()
                    except:
                        pass
                    if card.term == row[0] and datetime.datetime.combine(card.duedate, datetime.time(0,0)) <= datetime.datetime.fromisoformat(row[5]):
                        deck.remove(card)
                    else:
                        continue
            # format tags and flags
            tags = row[9][1:-1].split("'")
            flags = row[10][1:-1].split("'")
            for x in tags:
                if x in ["'", '"', ", "]:
                    tags.remove(x)
                else:
                    x = x[1:-1]
            for x in flags:
                if x in ["'", '"', ", "]:
                    flags.remove(x)
                else:
                    x = x[1:-1]
            deck.append(flashcard(row[0], row[1], int(row[2]), float(row[3]), float(row[4]), row[5], row[6], int(row[7]), row[8], tags, flags))
    # remove duplicates
    for card in deck:
        if type(card.duedate) == str:
            card.duedate = datetime.datetime.fromisoformat(card.duedate)
        try:
            card.duedate = card.duedate.date()
        except:
            pass
    for card1 in deck:
        for card2 in deck:
            if card1.term == card2.term and card1 != card2:
                if card1.duedate < card2.duedate:
                    deck.remove(card1)
                else:
                    deck.remove(card2)
    # import and update stats   
    for row in readstats:
        stat.append(row)
    
    # first row: number of reviews in last 30 days
    for x in range(len(stat[0])):
        if x != 0:
            stat[0][x] = int(stat[0][x])
    form30da = datetime.datetime.fromisoformat(stat[0][0]).date()
    tdy = datetime.datetime.today().date()
    th30d = datetime.timedelta(days=30)
    newstats0 = [(tdy - th30d).isoformat()]
        
    if form30da != tdy - th30d:
        if (tdy - form30da).days > 60:            
            for x in range(31):
                newstats0.append(0)
        else:
            newstats0 = newstats0 + stat[0][(tdy - form30da).days - 30:]
            while len(newstats0) < 32:
                newstats0.append(0)
        stat[0] = newstats0

#IMPT

def impt():
    print("")
    # make a deck
    reader = open('impt.txt', 'r').readlines()
    writer = csv.writer(open(os.getcwd()+'/.mnakdata/sched.mnak', 'a'))
    writer2 = open(os.getcwd()+'/.mnakdata/nsched.mnak', 'a')
    impted = 0 
    
    separator = input(r"    enter your separator: (default separator is four spaces, enter \t for tab and \n for newline) ")

    separator = separator.replace(r"\t", "\t")
    separator = separator.replace(r"\n", "\n")

    # import new cards into deck
    for row in reader:
        if row.strip() != "" and row[0].strip() != "":
            writer.writerow(row.strip().split(separator) + [0,variables[7][1],0,datetime.date.today(),False,0,"new"])
            writer2.write(str(row.strip().split(separator)) + "\n")
            impted += 1

    if impted == 0:
        print("    no cards imported. maybe enter a separator or check impt.txt?")
    else:
        print(f"    {impted} card(s) imported.")

# LEARN

def learn(deck):
    print("")
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
        color(f"\n    1. again ({printno(genints(card)[0])})", prefs["again"]) + 
        color(f"\n    2. hard ({printno(genints(card)[1])})", prefs["hard"]) +
        color(f"\n    3. good ({printno(genints(card)[2])})", prefs["good"]) +
        color(f"\n    4. easy ({printno(genints(card)[3])})", prefs["easy"]) + "\n")

        while 1:
            try:
                option = int(input("    "))-1 
            except:
                print("    invalid. try again.")
            else:
                if option < 0 or option > 3:
                    print("    invalid. try again.")
                else:
                    print("\n    card delayed by:", printno(genints(card)[option]), "\n")
                    if type(genints(card)[option]) == str:
                        card.status = "learn"
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
                        card.status = "rev"
                        # change data in deck
                        for ocard in deck:
                            if ocard.term == card.term:
                                deck.remove(ocard) # remove old copy of card
                        card.duedate = card.duedate + datetime.timedelta(days=genints(card)[option])
                        card.lastint = genints(card)[option]
                        print("    new due date:", str(card.duedate)[0:10])
                        print("    1 card less!")
                        deck.append(card) # add new copy of card
                        queue[0].remove(card) # remove card from queue
                    match option:
                        case 0:
                            card.status = "learn"
                            card.ls = 0
                            card.againcount += 1
                            if card.againcount == variables[11][1]: # autosuspend leech
                                card.suspended = True
                                card.againcount = 0
                                print("    card marked as leech. suspended")
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

    # SESSION
    # making queue
    queue = [[]]
    newcount = 0
    revcount = 0

    if variables[12][1]:
        for card in deck:
            if str(card.duedate).strip() == str(datetime.date.today()).strip() and card.suspended == "False" and card.ls == 2:
                queue[0].append(card)
                revcount += 1
            if revcount >= variables[1][1]:
                break
        for card in deck:
            if str(card.duedate).strip() == str(datetime.date.today()).strip() and card.suspended == "False" and card.ls != 2:
                queue[0].append(card)
                newcount += 1
            if revcount + newcount >= variables[1][1]:
                break
    else:
        for card in deck:
            if str(card.duedate).strip() == str(datetime.date.today()).strip() and card.suspended == "False":
                queue[0].append(card)
                match card.ls:
                    case 2:
                        revcount += 1
                    case _:
                        newcount += 1
            if newcount >= variables[0][1] or revcount >= variables[1][1]:
                break
    if variables[10][1]:
        random.shuffle(queue[0])
    
    # begin!
    print(f"    hello! welcome to your learning session.")
    
    if cardnum() == 0:
        print("    no cards today. maybe check impt.txt?")
    else:
        print(f"    today's card count: {cardnum()}")

    exitlearn = False

    def countcards(queue):
        new = 0
        learn0 = 0
        learn1 = 0
        rev = 0
        for x in queue:
            for card in x:
                match card.status:
                    case "new":
                        new += 1
                    case "learn":
                        if card.ls == 0:
                            learn0 += 1
                        elif card.ls == 1:
                            learn1 += 1
                    case "rev":
                        rev += 1
        return color(new, prefs["cardcountnew"]) + " + " + color(learn0, prefs["cardcountlearn"]) + " + " + color(learn1, prefs["cardcountlearn"]) + " + " + color(rev, prefs["cardcountrev"])
    
    while queue != []:
        for card in queue[0]:
            newint(card)
            if cardnum() > 0:
                print("    " + countcards(queue))
                print("    remaining cards:", cardnum())
                if input("    continue? (Y/n) ") == "n":
                    print("    exiting learn mode...")
                    exitlearn = True
                    break
            else:
                print("    good job! you finished the deck.")
        if exitlearn:
            break
        if queue[0] == []:
            queue.pop(0)

# SAVE

def save(deck):
    writecsv = csv.writer(open(os.getcwd()+'/.mnakdata/sched.mnak', 'w'))
    writetxt = open(os.getcwd()+'/.mnakdata/nsched.mnak', 'w')
    writestats = csv.writer(open(os.getcwd()+'/.mnakdata/stats.mnak', 'w'))
    saved = 0

    # save to 
    for x in deck:
        try:
            x.duedate = datetime.datetime.fromisoformat(x.duedate).date()
        except:
            x.duedate = x.duedate
        for tag in x.tags:
            if tag == "":
                x.tags.remove(tag)
        for flag in x.flags:
            if flag == "":
                x.flags.remove(flag)
        writecsv.writerow([x.term, x.defin.strip(), x.ls, x.ease, x.lastint, x.duedate, x.suspended, x.againcount, x.status, x.tags, x.flags])
        writetxt.write(x.term + "    " + x.defin + "\n")
        saved += 1

    # also save stats
    for x in stat:
        writestats.writerow(x)

# SETTINGS

def settings():
    while 1: 
        string = "\n    variables: \n"
        for x in range(len(vars)):
            varia = vars[x]
            string = string + f"    ~~~~~~~~~~~~~~~~~~~~\n    {varia.name} ({str(x)}): {str(varia.value)}  \n    {varia.exp } \n" 
        string = string + "    ~~~~~~~~~~~~~~~~~~~~\n"
        print("    " + string)
        comm = input("    enter any number to change the value of its corresponding variable or 'exit' to save and exit this menu.\n    _______\n    >>> ")
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
                    writevari = csv.writer(open(os.getcwd()+'/.mnakdata/config.mnak', 'w'))
                    for x in vars:
                        writevari.writerow([x.name, x.value, x.format, x.exp])

def preferences():
    while 1: 
        count = 0
        string = "\n    options/preferences: \n"
        for x in prefs:
            pref = prefs[x]
            string = string + f"    ~~~~~~~~~~~~~~~~~~~~\n    {x} ({str(count)}): {pref}  \n" 
            count += 1
        string = string + "    ~~~~~~~~~~~~~~~~~~~~\n"
        print("    " + string)
        comm = input("    enter any number to change the value of its corresponding variable or 'exit' to save and exit this menu.\n    _______\n    >>> ")
        match comm:
            case 'exit':
                break
            case _:
                try:
                    comm = int(comm)
                    cpref = list(prefs)[comm]
                except:
                    print("    invalid command. try again!")
                else:
                    print("    " + cpref + " (" + str(int(comm)) + ")" + "\n    current value: " + str(prefs[cpref]))
                    while 1:
                        prefs[cpref] = input("    enter new value: ")
                        break
                    writeprefs = csv.writer(open(os.getcwd()+'/.mnakdata/prefs.csv', 'w'))
                    for x in prefs:
                        writeprefs.writerow([x, prefs[x]])

# GUIDE
def guide():
    guidelist = {
        "faq" : "see frequently asked questions.",
        "imexportguide" : "see instructions on how to import and export data."
    }
    for x in guidelist:
        print("    " + x + ": " + guidelist[x])
    while 1:
        comm = input("""\n    enter: \n    - the name of the guide you want to see\n    - 'help' to see the list of guides again\n    - 'exit' to exit guides\n    ______\n    >>> """)
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

# deck
def deck(deck):
    init(deck)
    save(deck)
    
    # print out deck
    nocards = 0
    
    def digs(no):
        if no == 0:
            return 1
        else:
            return math.floor(math.log(no, 10))+1

    def susstr(card):
        if card.suspended == "True":
            return " (suspended)"
        else:
            return ""
    
    def printcards(deck):
        # print out with line numbers
        cardcount = 0
        spaceno = digs(nocards)

        for card in deck:
            try:
                print("    " + (spaceno - digs(cardcount)) * " " + str(cardcount) + ". " + card.term + ", " + card.defin + ", " + str(card.duedate.date()) + ", " + card.status + ", " + str(card.tags) + ", " + str(card.flags) + susstr(card))
            except:
                print("    " + (spaceno - digs(cardcount)) * " " + str(cardcount) + ". " + card.term + ", " + card.defin + ", " + str(card.duedate) + ", " + card.status + ", " + str(card.tags) + ", " + str(card.flags) + susstr(card))
            cardcount += 1

    while 1:
        print("\n    ~~~~~~~~~~~~~~~~~~~~")
        printcards(deck)
        print("    ~~~~~~~~~~~~~~~~~~~~")


        comm = input("""\n    enter:\n    - any number to edit its corresponding card\n    - 'add' to add a card\n    - 'sort' to sort the deck\n    - 'exit' to save and exit the deck\n    ______\n    >>> """)
        match comm:
            case "exit":
                writer = csv.writer(open(os.getcwd()+'/.mnakdata/sched.mnak', "w+"))
                for card in deck:
                    writer.writerow([card.term, card.defin.strip(), card.ls, card.ease, card.lastint, card.duedate, card.suspended, card.againcount, card.status, card.tags, card.flags])
                break
            case "add":
                writer = csv.writer(open(os.getcwd()+'/.mnakdata/sched.mnak', 'a'))
                writer2 = open(os.getcwd()+'/.mnakdata/nsched.mnak', 'a')
             
                term = input("    enter term: ")
                defin = input("    enter definition: ")

                writer.writerow([term,defin,0,variables[7][1],0,datetime.datetime.today(),False,0,"new",[],[]])
                writer2.write(str(term + defin + "\n"))
                deck.append(flashcard(term,defin,0,variables[7][1],0,datetime.datetime.today(),False,0,"new",[],[]))
            case "sort":
                sortby = input("    enter value by which you would like to sort by (term or duedate): ")
                ascdesc = input("    would you like to sort in descending order? (y/N) ")
                rev = False

                if ascdesc == "y":
                    rev = True
                match sortby:
                    case "term":
                        deck.sort(key = lambda x: x.term, reverse = rev)
                    case "duedate":
                        deck.sort(key = lambda x: x.duedate, reverse = rev)
            case _:
                try:
                    deck[int(comm)]
                except:
                    print("    invalid. try again.")
                else:
                    card = deck[int(comm)]
                    try:
                        print("    " + card.term + ", " + card.defin + ", " + str(card.duedate.date()) + ", " + card.status + ", " + str(card.tags) + ", " + str(card.flags) + susstr(card))
                    except:
                        print("    " + card.term + ", " + card.defin + ", " + str(card.duedate) + ", " + card.status + ", " + str(card.tags) + ", " + str(card.flags) + susstr(card))
                    while 1:
                        toedit = input("""\n    enter:\n    - any value you would like to change (term, def, suspension, tags or flags)\n    - any card action ('delete', 'bury' or 'forget')\n    - 'exit' to cancel\n    ______\n    >>> """)
                        match toedit:
                            case "term":
                                card.term = input("    enter new value: ")
                                break
                            case "def":
                                card.defin = input("    enter new value: ")
                                break
                            case "suspension":
                                match card.suspended:
                                    case "True":
                                        card.suspended = False
                                    case "False":
                                        card.suspended = True
                                    case _:
                                        card.suspended = True
                                print("\n    suspension toggled to", card.suspended)
                                break
                            case "tags":
                                while 1:
                                    print("    " + str(card.tags))
                                    addrm = input("    enter 'add/rm <tag>' to add or remove a tag. enter 'exit' to exit: ")
                                    match addrm:
                                        case "exit":
                                            break
                                        case _:
                                            if addrm[0:4] == "add ":
                                                card.tags.append(addrm[4:])
                                            elif addrm[0:3] == "rm ":
                                                try:
                                                    card.tags.remove(addrm[3:])
                                                except:
                                                    print("    not an existing tag. try again.")
                                            else:
                                                print("    invalid. try again.")
                            case "flags":
                                while 1:
                                    print("    " + str(card.flags))
                                    addrm = input("    enter 'add/rm <tag>' to add or remove a flag. enter 'exit' to exit: ").strip()
                                    match addrm:
                                        case "exit":
                                            break
                                        case _:
                                            if addrm[0:4] == "add ":
                                                card.flags.append(addrm[4:])
                                            elif addrm[0:3] == "rm ":
                                                try:
                                                    card.flags.remove(addrm[3:])
                                                except:
                                                    print("    not an existing flag. try again.")
                                            else:
                                                print("    invalid. try again.")

                            case 'bury':
                                card.duedate += datetime.timedelta(days=1)
                                break
                            case 'delete':
                                deck.remove(card)
                                break
                            case 'forget':
                                deck.remove(card)
                                writer = csv.writer(open(os.getcwd()+'/.mnakdata/sched.mnak', 'a'))
                                writer2 = open(os.getcwd()+'/.mnakdata/nsched.mnak', 'a')
                             
                                writer.writerow([card.term,card.defin,0,variables[7][1],0,datetime.datetime.today(),False,0,"new", [], []])
                                writer2.write(str(card.term + card.defin + "\n"))
                                deck.append(flashcard(card.term,card.defin,0,variables[7][1],0,datetime.datetime.today(),False,0,"new", [], []))
                                break
                            case 'exit':
                                break
                            case _:
                                print("    invalid. try again")

def update():
    print("\n    recloning minianki...")
    subprocess.run(["git", "-C", os.path.abspath(os.path.join(os.getcwd(), os.pardir)), "clone", "https://github.com/shuu-wasseo/minianki"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("    cleaning up the mess...")
    subprocess.run(["git", "restore", "."])
    subprocess.run(["git", "clean", "-f", "-d"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("    repulling minianki...")
    subprocess.run(["git", "pull", "https://github.com/shuu-wasseo/minianki"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("    done!")
    print("    minianki has been updated. please restart minianki to see changes take effect.")

def backup():
    # os.mkdir("~/.config/.minianki")
    subprocess.run(["rm", "-r", backuppath()+"/.mnakdata"])
    subprocess.run(["cp", "-r", os.getcwd()+"/.mnakdata", backuppath()])

def nobackup():
    reader = open(os.getcwd()+'/.mnakdata/nsched.mnak', 'r').readlines()
    rows = []
    for x in reader:
        rows.append(x)
    if len(rows) == 0:
        print("before we begin:")
        loadyn = input("you have no user data. would you like to load from a backup? (Y/n) ")
        if loadyn != "n":
            load()
    print("")

def load():
    subprocess.run(["rm", "-r", os.getcwd()+"/.mnakdata"])
    subprocess.run(["cp", "-r", backuppath()+"/.mnakdata", os.getcwd()])

def backuppath():
    open = prefs["backup location"][0]
    path = prefs["backup location"][1:]
    match open:
        case ".":
            return os.getcwd() + path
        case "~":
            return os.path.expanduser('~')+ path
        case _:
            return path

def stats(deck):
    # bar graph function
    def plotgraph(axes, data, title):
        plt.clf()
        plt.bar(axes, data)
        plt.title("# " + title)
        plt.plot_size(plt.tw(), plt.th() / 2)
        plt.canvas_color("black")
        plt.axes_color("black")
        plt.ticks_color("white")
        plt.show()

    # future due
    futdues = []
    futstats = []
    num = []
    for x in deck:
        futdues.append((x.duedate - datetime.datetime.today().date()).days)
    for x in futdues:
        try:
            futstats[x] += 1
        except IndexError:
            while len(futstats) < x + 1:
                futstats.append(0)
            futstats[x] += 1
    for x in range(len(futstats)):
        num.append(x)
    plotgraph(num, futstats, "future due")

    # calendar heatmap
    print("# calendar heatmap \ncoming soon!")

    # reviews per day
    l30d = [datetime.datetime.today()]
    for x in range(30):
        l30d.append((l30d[0] - datetime.timedelta(days=x+1)).date().isoformat())
    l30d.reverse()
    plotgraph(l30d, stat[0][1:], "reviews per day")
