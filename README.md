# minianki

unofficial CLI version of anki. (still in development)

## requirements
- python 3 (3.10 and up)
- any working command line / terminal

## installation instructions
firstly, clone this repository.

```
$ git clone https://github.com/shuu-wasseo/minianki
```
secondly, add the minianki directory into your PATH. 

thirdly, make the mnak file executable with the following code (replace 'mnak' below with the path for the mnak file)
```
$ chmod +x mnak
```
now, you are able to use minianki! enter "mnak" in your terminal to begin!

## commands

list of commands:

importing:
- impt: import cards in import.txt to the main database.

manage/use deck:
- deck: see all your cards and edit, suspend or delete them.
- learn: an anki-esque learning session.

settings and help:
- guide: see guides.
- help: view all commands again.
- settings: customise deck options.

misc:
- exit: leave minianki.
- update: update minianki.

## directory
### main directory
- [README.md](https://github.com/shuu-wasseo/minianki/blob/main/READNE.md) - the file you are reading now :>
- [impt.txt](https://github.com/shuu-wasseo/minianki/blob/main/impt.txt) - file for importing new cards.
- [minianki.py](https://github.com/shuu-wasseo/minianki/blob/main/minianki.py) - package file, contains all functions for main.py
- [mnak](https://github.com/shuu-wasseo/minianki/blob/main/mnak) - main user interface.

### subdirectories
- [.userdata](https://github.com/shuu-wasseo/minianki/tree/main/.userdata) - exportable data.
  - [learnvars.csv](https://github.com/shuu-wasseo/minianki/blob/main/.userdata/learnvars.csv) - all customised deck options.
  - [nsched.mnak](https://github.com/shuu-wasseo/minianki/blob/main/.userdata/nsched.mnak) - all cards without scheduling.
  - [sched.mnak](https://github.com/shuu-wasseo/minianki/blob/main/.userdata/sched.mnak) - all cards with scheduling.

- [.guides](https://github.com/shuu-wasseo/minianki/tree/main/export) - guides.
  - [faq.txt](https://github.com/shuu-wasseo/minianki/blob/main/.guides/faq.txt)
  - [imexportguide.txt](https://github.com/shuu-wasseo/minianki/blob/main/.guides/imexportguide.txt) - exporting instructions.

## guides
the following can also be found in [`./guides/`](https://github.com/shuu-wasseo/minianki/tree/main/export).

### import/export 
*(also found in [.guides/imexportguide.txt](https://github.com/shuu-wasseo/minianki/blob/main/.guides/imexportguide.txt))*

**importing new cards:**

either:
- paste text into import.txt in a terms-definitions format
- or replace import.txt with a .txt file in that format.

minianki will:
- import your files into the database with the "import" command and prompt you for a delimiter (4-space tab by default)
- refresh the deck with the "init" command. 
do remember to do both "import" and "init" everytime new cards are added into import.txt.

**importing/exporting user data:**

simply paste another .userdata subdirectory from your old minianki setup into the main minianki directory of your new minianki setup. 
the .userdata subdirectory contains data such as cards (with or without scheduling) and learning variables (preferences).

### faq
*(also found in [.guides/faq.txt](https://github.com/shuu-wasseo/minianki/blob/main/.guides/faq.txt))*

**how does the algorithm work in minianki?**

the minianki algorithm is similar to anki's algorithm without certain features. however, we aim to implement most if not all features of anki in minianki (other than features that the terminal does not support) by v1. see the [wiki](https://github.com/shuu-wasseo/minianki/wiki) for more information.

**can i have subdecks in minianki?**

minianki currently does not support subdecks, but we are currently working to implement these in upcoming versions.

**can i have media in my minianki flashcards?**

while this is a prominent feature of anki, minianki does not currently support media and we are not planning to implement media support anytime soon.
