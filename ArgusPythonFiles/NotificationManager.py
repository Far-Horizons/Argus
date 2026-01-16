# Handles notifying me of new subdomains/changes in alive/responsive status, or if the process dies due to error
# Single run process spun up when needed, then dies
import os
import subprocess
import Screenshotter

class NotificationManager:
    def __init__(self, configuration, target):
        self.config = configuration
        self.target = target
        self.domain_name = self.target.replace('.', '_')


    def notify_new_findings(self):
        report_path = os.path.expanduser(f"~/Argus/{self.domain_name}/new_subdomains_report-{self.domain_name}.txt")
        if os.path.exists(report_path):
            subprocess.run(
                ["notify",
                 "-data", report_path,
                 "-bulk"],
                 check=True
            )
    
    def run_screenshot_cycle(self, targetlist, webhookURL):
        ss = Screenshotter.Screenshotter(targetlist, webhookURL, self.config)
        ss.run()