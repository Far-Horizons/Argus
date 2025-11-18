# Reads targets from the target file, and manages cycling the active target
# A cycle is completed when all loaded targets have been used once
# After completing a cycle, the target list is refreshed from the target file
# persisten object, lives throughout the program execution
import os

class TargetManager:
    def __init__(self, configuration):
        self.config = configuration
        self.targets = self.__load_targets()
        self.current_index = 0

    # Loads targets from the target file
    def __load_targets(self):
        with open(os.path.expanduser(f"~/Argus/{self.config.target}"), 'r') as f:
            return [line.strip() for line in f if line.strip()]
        
    # Returns the current target
    def get_target(self):
        return self.targets[self.current_index] if self.targets else None
    
    # advances to the next target, cycling back to the start if needed
    def next_target(self):
        if not self.targets:
            return
        self.current_index += 1
        if self.current_index >= len(self.targets):
            self.reset()
    
    # check if there are any targets loaded
    def has_targets(self):
        return len(self.targets) > 0
    
    # counts the loaded targets
    def count_targets(self):
        return len(self.targets)
    
    # Resets the target list and index
    def reset(self):
        self.current_index = 0
        self.targets = self.__load_targets()
    
    # Checks if a full cycle has been completed (or rather, if we are back at the start of a cycle)
    def cycle_completion_check(self):
        return self.current_index == 0