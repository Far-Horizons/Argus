# Reads data from previous scan result and makes it available to ResultComparer
# single-run object, created anew for each target scan
import os

class HistoricalDataManager:
    def __init__(self, configuration, target):
        self.config = configuration
        self.target = target
        self.domain_name = target.replace('.', '_')
        self.historical_data_directory = os.path.expanduser(f"~/Argus/{self.domain_name}/")
        os.makedirs(self.historical_data_directory, exist_ok=True)
        self.historical_data_all_subdomains = self._load_historical_data("domains_all")
        self.historical_data_alive_subdomains = self._load_historical_data("alive")
        self.historical_data_responsive_subdomains = self._load_historical_data("responsive")
        self.historical_data_accessible_subdomains = self._load_historical_data("accessible")
        

    def _load_historical_data(self, type):
        file_path = os.path.expanduser(f"{self.historical_data_directory}{type}-{self.domain_name}.txt")
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def clear_old_data_file(self):
        for type in ["domains_all", "alive", "responsive", "accessible"]:
            file_path = os.path.expanduser(f"{self.historical_data_directory}{type}-{self.domain_name}.txt")
            if os.path.exists(file_path):
                os.remove(file_path)
