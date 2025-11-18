#!/usr/bin/env python3
import os
import sys

import StartManager

if __name__ == "__main__":
    correct_directory = os.path.expanduser("~/Argus")
    current_directory = os.getcwd()

    if current_directory == correct_directory:
        starter = StartManager.StartManager()
        starter.start()
    else: 
        print(f"Please run Argus from the {correct_directory} directory.")
        sys.exit(1)