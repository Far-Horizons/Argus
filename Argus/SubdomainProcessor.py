# Handles the processing of the collected subdomains. It merges files, checks alive status, etc. Single-run object, it is invoked whenever it is needed, then dies
import subprocess
from ArgusHelperMethods import print_non_silent, merge_lists
import os

class SubdomainProcessor:
    def __init__(self, configuration, target):
        self.config = configuration
        self.domain_name = target.replace('.', '_')
        self.target = target

    def run(self):
        self.merge_subdomain_files()
        self.check_alive()
        self.check_accessible()
        self.check_responsive()
    
    def merge_subdomain_files(self):
        print_non_silent(self, "Merging the subdomain files...")
        merge_lists(self, os.path.expanduser(f"~/Argus/{self.domain_name}/domains_subfinder-{self.domain_name}.txt"),
                             os.path.expanduser(f"~/Argus/{self.domain_name}/domains_findomain-{self.domain_name}.txt"),
                             os.path.expanduser(f"~/Argus/{self.domain_name}/domains_all-{self.domain_name}.txt")
                             )
        subprocess.run(
                    ["rm", os.path.expanduser(f"~/Argus/{self.domain_name}/domains_subfinder-{self.domain_name}.txt"),
                    os.path.expanduser(f"~/Argus/{self.domain_name}/domains_findomain-{self.domain_name}.txt")],
                    check=True
                )
        print_non_silent(self, "Finished merging the subdomain files")

    # This method checks if the subdomains are alive
    def check_alive(self):
        print_non_silent(self, "checking which subdomains are alive...")
        subprocess.run(
            ["dnsx",
            "-l", os.path.expanduser(f"~/Argus/{self.domain_name}/domains_all-{self.domain_name}.txt"), "-o",
            os.path.expanduser(f"~/Argus/{self.domain_name}/alive-{self.domain_name}.txt"),
            "-silent"],
            check=True,
            stdout=subprocess.DEVNULL
        )
        print_non_silent(self, "\nFinished checking alive subdomains.\n")
    
    # This method checks if the subdomains are responsive
    def check_responsive(self):
        print_non_silent(self, "checking which subdomains are responsive...")
        with open(os.path.expanduser(f"~/Argus/{self.domain_name}/responsive-{self.domain_name}.txt"), "w") as responsive_file:
            subprocess.run(
                ["ffuf", "-u", "https://FUZZ",
                "-w", os.path.expanduser(f"~/Argus/{self.domain_name}/alive-{self.domain_name}.txt"),
                "-s"],
                check=True,
                stdout=responsive_file,
                stderr=subprocess.STDOUT
            )
        print_non_silent(self, "\nFinished checking responsive subdomains.\n")

    # This method checks which subdomains are accessible
    def check_accessible(self):
        print_non_silent(self, "checking which subdomains are accessible...")
        with open(os.path.expanduser(f"~/Argus/{self.domain_name}/accessible-{self.domain_name}.txt"), "w") as accessible_file:
            subprocess.run(
                ["ffuf", "-u", "https://FUZZ",
                "-w", os.path.expanduser(f"~/Argus/{self.domain_name}/alive-{self.domain_name}.txt"),
                "-s", "-fc", "404,403,401"],
                check=True,
                stdout=accessible_file,
                stderr=subprocess.STDOUT
            )
        print_non_silent(self, "\nFinished checking accessible subdomains.\n")