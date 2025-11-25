# Handles logging, writes to a txt file. Single-run object, it is invoked whenever logging is needed, then dies
# Not properly implemented yet.
import os

class Logger:
    def __init__(self, configuration, target):
        self.config = configuration
        self.program_log_file = os.path.expanduser("~/Argus/Argus_Main_Log.txt") # Global log for the program - Notes aboute start/stop times, errors, etc.
        self.target_log_file = "" # Target-specific log file - Notes about the target's scan times, errors, etc.
        self.target = target

    def set_target_log_file(self):
        domain_name = self.target.replace('.', '_')
        self.target_log_file = os.path.expanduser(f"~/Argus/{domain_name}/Argus_{domain_name}_Log.txt")