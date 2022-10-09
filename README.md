![](https://progress-bar.dev/90/?title=completed)

# minianki

**working idea:** emulate an anki session in the terminal. users should be able to import and export modified data files containing progress, etc..

## directory
### main directory
- [README.md](https://github.com/shuu-wasseo/minianki/blob/main/READNE.md) - the file you are reading now :>
- [import.txt](https://github.com/shuu-wasseo/minianki/blob/main/import.txt) - file for importing new cards.
- [main.py](https://github.com/shuu-wasseo/minianki/blob/main/main.py) - main user interface.
- [minianki.py](https://github.com/shuu-wasseo/minianki/blob/main/minianki.py) - package file, contains all functions for main.py

### subdirectories
- [.userdata](https://github.com/shuu-wasseo/minianki/tree/main/export) - exportable data.
  - [csv.mnak](https://github.com/shuu-wasseo/minianki/blob/main/export/csv.mnak) - all cards with scheduling.
  - [learnvars.csv](https://github.com/shuu-wasseo/minianki/blob/main/export/learnvars.csv) - all customised learning variables.
  - [txt.mnak](https://github.com/shuu-wasseo/minianki/blob/main/export/txt.mnak) - all cards without scheduling.

- [.guides](https://github.com/shuu-wasseo/minianki/tree/main/export) - guides.
  - [exportguide.txt](https://github.com/shuu-wasseo/minianki/blob/main/export/export.txt) - exporting instructions.
