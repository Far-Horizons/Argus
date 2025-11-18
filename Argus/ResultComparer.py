# Compares the result from previous scan with new scan, and takes note of any differences
import os

class ResultComparer:
    def __init__(self, configuration, target, historical_data):
        self.config = configuration
        self.target = target
        self.domain_name = self.target.replace('.', '_')
        self.historical_data = historical_data
        self.current_data_directory = os.path.expanduser(f"~/Argus/{self.domain_name}/")
        self.current_data_all_subdomains = self._load_new_data("domains_all")
        self.current_data_alive_subdomains = self._load_new_data("alive")
        self.current_data_responsive_subdomains = self._load_new_data("responsive")
        self.current_data_accessible_subdomains = self._load_new_data("accessible")

    def run(self):
        self.compare_lists()
        self.create_reports()

    def _load_new_data(self, type):
        file_path = os.path.expanduser(f"{self.current_data_directory}{type}-{self.domain_name}.txt")
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    
    # compares the lists and identifies new subdomains of each category
    def compare_lists(self):
        self.new_subdomains = list(set(self.current_data_all_subdomains) - set(self.historical_data.historical_data_all_subdomains))
        self.new_alive_subdomains = list(set(self.current_data_alive_subdomains) - set(self.historical_data.historical_data_alive_subdomains))
        # self.new_responsive_subdomains = list(set(self.current_data_responsive_subdomains) - set(self.historical_data.historical_data_responsive_subdomains))
        # self.new_accessible_subdomains = list(set(self.current_data_accessible_subdomains) - set(self.historical_data.historical_data_accessible_subdomains))
    
    def create_reports(self):
        with open(os.path.expanduser(f"~/Argus/{self.domain_name}/new_subdomains_report-{self.domain_name}.txt"), 'w') as report_file:

            if len(self.new_subdomains) > 0:
                report_file.write("New Subdomains:\n")
            for subdomain in self.new_subdomains:
                report_file.write(f"{subdomain}\n")

            if len(self.new_alive_subdomains) > 0:
                report_file.write("\nNew Alive Subdomains:\n")
            for subdomain in self.new_alive_subdomains:
                report_file.write(f"{subdomain}\n")

            # if len(self.new_responsive_subdomains) > 0:
            #     report_file.write("\nNew Responsive Subdomains:\n")
            # for subdomain in self.new_responsive_subdomains:
            #     report_file.write(f"{subdomain}\n")

            # if len(self.new_accessible_subdomains) > 0:
            #     report_file.write("\nNew Accessible Subdomains:\n")
            # for subdomain in self.new_accessible_subdomains:
            #     report_file.write(f"{subdomain}\n")
    
    def has_new_findings(self):
        return (len(self.new_subdomains) > 0 or
                len(self.new_alive_subdomains) > 0 # or
                # len(self.new_responsive_subdomains) > 0 or
                # len(self.new_accessible_subdomains) > 0
                )
    
    def clear_old_reports(self):
        report_path = os.path.expanduser(f"~/Argus/{self.domain_name}/new_subdomains_report-{self.domain_name}.txt")
        if os.path.exists(report_path):
            os.remove(report_path)