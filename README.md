**minianki has been archived. no further progress will be made on this project.**

# minianki

an unofficial CLI version of anki.

## table of contents
1. [requirements](#requirements)
2. [installation](#installation)
3. [updation/upgradation](#updation-and-upgradation)
4. [commands](#commands)

## requirements
- python 3 (3.10 and up)
- any working command line / terminal

## installation
firstly, clone this repository.

```
$ git clone https://github.com/shuu-wasseo/minianki
```

secondly, add the minianki directory into your PATH. 

thirdly, make the mnak file executable with the following code.

```
$ cd minianki
$ chmod +x mnak
```

lastly, enter the following in your browser to install all relevant and necessary packages.

```
$ make install
```

now, you are able to use minianki! enter "mnak" in your terminal to begin!

## updation and upgradation
simply enter "update" into your mini-console and minianki will instantly update/upgrade itself for you.

## commands 
list of commands:

importing:
- impt: import cards in import.txt to the main database.

manage/use deck:
- deck: see all your cards and edit, suspend or delete them.
- learn: an anki-esque learning session.
- stats: see your stats for the deck.

settings and help:
- guide: see guides.
- help: view all commands again.
- prefs: configure general preferences.
- sett: configure deck options.

misc:
- clog: see changelog.
- exit: leave minianki.
- load: load backup.
- update: update and restart minianki.
