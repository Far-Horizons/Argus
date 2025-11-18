# Runs a single enumeration and set of checks, then dies
import SubdomainCollector
import SubdomainProcessor

class SingleRunManager:
    def __init__(self, configuration):
        self.config = configuration
        self.target = configuration.target

    def start_single_run(self):
        collector = SubdomainCollector.SubdomainCollector(self.config, self.target)
        collector.run()
        processor = SubdomainProcessor.SubdomainProcessor(self.config, self.target)
        processor.run()