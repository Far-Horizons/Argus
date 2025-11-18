# Single-run object, it is invoked by the controlsuite every time a subdomain enumeration is needed, then dies
import subprocess
from ArgusHelperMethods import print_non_silent
import os

class SubdomainCollector:
    def __init__(self, configuration, target):
        self.config = configuration
        self.domain_name = target.replace('.', '_')
        self.target = target

    def run(self):
        self.Subfinder_collect()
        self.Findomain_collect()

    def Subfinder_collect(self):
        print_non_silent(self, f"running subfinder for {self.target}...")
        subprocess.run(
            ["subfinder",
             "-d", self.target,
             "-o", os.path.expanduser(f"~/Argus/{self.domain_name}/domains_subfinder-{self.domain_name}.txt"),
             "-silent"],
            check=True,
            stdout=subprocess.DEVNULL
        )
        print_non_silent(self, "\nFinished subdomain collection with subfinder.\n")
    
    def Findomain_collect(self):
        print_non_silent(self, f"running findomain for {self.target}...")
        subprocess.run(
            ["findomain",
             "-t", self.target,
             "-u", os.path.expanduser(f"~/Argus/{self.domain_name}/domains_findomain-{self.domain_name}.txt"),
             "-q"],
            check=True,
            stdout=subprocess.DEVNULL
        )
        print_non_silent(self, "\nFinished subdomain collection with findomain.\n")


