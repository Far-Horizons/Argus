# This class handles the initial setup, and after setting things like the config hands the "power" to the MonitoringManager, or the SingleRunManager
import MonitoringManager
import SingleRunManager
import ConfigManager

class StartManager:
    def __init__(self):
        self.config = ConfigManager.ConfigManager()
        self.config.set_config()

    def start(self):
        if self.config.mode == "monitoring":
            monitoring_manager = MonitoringManager.MonitoringManager(self.config)
            monitoring_manager.start_monitoring()
        else:
            single_run_manager = SingleRunManager.SingleRunManager(self.config)
            single_run_manager.start_single_run()