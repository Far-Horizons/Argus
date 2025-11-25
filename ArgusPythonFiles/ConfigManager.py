# This class will manage configuration settings for the tool
from dataclasses import dataclass
from ArgManager import ArgManager

@dataclass
class ConfigManager:
    target: str = ""
    mode: str = ""
    silent: bool = False
    interval: int = 3600

    def set_config(self):
        self.args = ArgManager().parser.parse_args()
        self.target = self.args.target
        self.mode = "monitoring" if self.args.monitoring_mode else "single-run"
        self.interval = self.args.interval if self.args.monitoring_mode else 3600
        if self.args.silent:
            self.silent = True
        elif self.args.monitoring_mode:
            self.silent = True
        else:
            self.silent = False
        if (self.args.monitoring_mode and self.args.monitor_debug):
            self.silent = False