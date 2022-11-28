# labeling

First of all, you need to convert your existing file for labeling into .csv file -> here https://convertio.co/ru/xlsx-csv/

Linux
- figure it out ;)

MacOS

- install brew (run command in terminal)
- /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)
---
- brew install pyenv
- pyenv install 3.9.2
- python3 -m pip install --upgrade pip
- pip3 install webdriver-manager
- pip3 install pandas
- pip3 install selenium
- pip3 instal webdriver-manager

After all run "python google_lableling_chrome.py" in terminal

Default tabs per window - 5

After it opend, you can back to terminal and wtire 'n' to open new batch of tabs in new window
