# The heart of monitoring mode, from which the monitoring is controlled and orchestrated
# This will keep running until the process dies by intervention or error
import time
import SubdomainCollector
import SubdomainBruteforcer
import SubdomainProcessor
import TargetManager
import HistoricalDataManager
import ResultComparer
import NotificationManager
from ArgusHelperMethods import print_non_silent

class MonitoringManager:
    def __init__(self, configuration):
        self.config = configuration
        self.target = ""
        self.target_manager = TargetManager.TargetManager(configuration) # creates the target manager object, which will persist throughout the monitoring session

    # Starts the monitoring loop
    def start_monitoring(self):
        while True:
            print_non_silent(self, f"[[MONITOR DEBUG]] Starting monitoring cycle for targets in {self.config.target}...")
            self.monitoring_cycle()
            print_non_silent(self, f"[[MONITOR DEBUG]] Monitoring cycle complete. Sleeping for {self.config.interval} seconds...")
            time.sleep(self.config.interval)

    # Runs a single monitoring cycle
    def monitoring_cycle(self):
        print_non_silent(self, "[[MONITOR DEBUG]] Starting a new monitoring cycle...")
        while True:
            self.run_target_scan()
            if self.target_manager.cycle_completion_check():
                print_non_silent(self, "[[MONITOR DEBUG]] Break condition met (completed a full cycle)")
                break
        print_non_silent(self, "[[MONITOR DEBUG]] End of the monitoring cycle")

    # Runs a single target's scans
    def run_target_scan(self):
        target = self.target_manager.get_target()

        # load and clear historical data
        print_non_silent(self, f"[[MONITOR DEBUG]] Loading historigy for target: {target}, and clearing previous findings...")
        historical_data_manager = HistoricalDataManager.HistoricalDataManager(self.config, target)
        historical_data_manager.clear_old_data_file()
        print_non_silent(self, f"[[MONITOR DEBUG]] Historical data loaded and files cleared for target: {target}")

        # run the scans
        print_non_silent(self, f"[[MONITOR DEBUG]] Starting scans for target: {target}")
        collector = SubdomainCollector.SubdomainCollector(self.config, target)
        collector.run()
        bruteforcer = SubdomainBruteforcer.SubdomainBruteforcer(self.config, target)
        bruteforcer.run()
        processor = SubdomainProcessor.SubdomainProcessor(self.config, target)
        processor.run()
        print_non_silent(self, f"[[MONITOR DEBUG]] Finished scans for target: {target}")
        
        # compare the results
        print_non_silent(self, f"[[MONITOR DEBUG]] Comparing results for target: {target}")
        comparer = ResultComparer.ResultComparer(self.config, target, historical_data_manager)
        comparer.run()
        print_non_silent(self, f"[[MONITOR DEBUG]] Finished comparing results for target: {target}")

        # If new findings were detected, notify the user
        if comparer.has_new_findings():
            print_non_silent(self, f"[[MONITOR DEBUG]] New findings detected for target: {target}, notifying user...")
            notification_manager = NotificationManager.NotificationManager(self.config, target)
            notification_manager.notify_new_findings()
            print_non_silent(self, f"[[MONITOR DEBUG]] User notified for target: {target}")
        else:
            print_non_silent(self, f"[[MONITOR DEBUG]] No new findings for target: {target}, skipping notification.")
        
        self.target_manager.next_target()