# This class bruteforces subdomains for a given target. Single-run object, it is invoked whenever subdomain bruteforcing is needed, then dies
import os
import subprocess
from ArgusHelperMethods import print_non_silent

class SubdomainBruteforcer:
    def __init__(self, configuration, target):
        self.config = configuration
        self.domain_name = target.replace('.', '_')
        self.target = target
        self.wordlist_path = os.path.expanduser("~/Argus/SubdomainBruteforceWordlist.txt")
        self.output_file = os.path.expanduser(f"~/Argus/{self.domain_name}/domains_gobuster-{self.domain_name}.txt")
    
    def run(self):
        self.gobuster_bruteforce()
    

    def gobuster_bruteforce(self):
        print_non_silent(self, f"running gobuster for {self.target}...")
        subprocess.run(
            ["gobuster", "dns",
             "--domain", self.target,
             "--wordlist", self.wordlist_path,
             "-o", self.output_file],
             check=True,
            stdout=subprocess.DEVNULL
        )
        print_non_silent(self, "\nFinished subdomain bruteforcing with gobuster.\n")
    
