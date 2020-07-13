# DvachParser

A program to continuously download all files from dvach thread.

## Installation and starting

1. Install python>3.5.
2. Download and install [phf](https://github.com/framaz/phf).
3. Download the latest release.
4. Run main.py with python.

## Usage

There are two types of command now:

1. Subscribe to a thread and start downloading: 

```d 2ch.hk/?/res/???.html dir_to_save```

You can ommit dir_to_save, then the thread pics will be saved to ```./downloads```
(not your user's downloads but downloads in the same folder where the main.py is)

2. List all followed threads: ```l```

