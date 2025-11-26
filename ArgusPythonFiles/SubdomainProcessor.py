# Handles the processing of the collected subdomains. It merges files, checks alive status, etc. Single-run object, it is invoked whenever it is needed, then dies
import subprocess
from ArgusHelperMethods import print_non_silent, merge_lists
import os

class SubdomainProcessor:
    def __init__(self, configuration, target):
        self.config = configuration
        self.domain_name = target.replace('.', '_')
        self.target = target
        self.subfinder_filepath = os.path.expanduser(f"~/Argus/{self.domain_name}/domains_subfinder-{self.domain_name}.txt")
        self.findomain_filepath = os.path.expanduser(f"~/Argus/{self.domain_name}/domains_findomain-{self.domain_name}.txt")
        self.gobuster_filepath = os.path.expanduser(f"~/Argus/{self.domain_name}/domains_gobuster-{self.domain_name}.txt")
        self.domains_all_collected_filepath = os.path.expanduser(f"~/Argus/{self.domain_name}/domains_all_collected-{self.domain_name}.txt")
        self.master_subdomain_list_filepath = os.path.expanduser(f"~/Argus/{self.domain_name}/master_subdomain_list-{self.domain_name}.txt")
        self.alive_filepath = os.path.expanduser(f"~/Argus/{self.domain_name}/alive-{self.domain_name}.txt")
        self.responsive_filepath = os.path.expanduser(f"~/Argus/{self.domain_name}/responsive-{self.domain_name}.txt")
        self.accessible_filepath = os.path.expanduser(f"~/Argus/{self.domain_name}/accessible-{self.domain_name}.txt")

    def run(self):
        self.merge_collected_subdomain_files()
        self.add_new_subdomains_to_master_file()
        self.check_alive()
        self.check_responsive()
        self.check_accessible()
    
    def merge_collected_subdomain_files(self):
        print_non_silent(self, "Merging the subdomain files...")
        merge_lists(self, self.subfinder_filepath,
                    self.findomain_filepath,
                    self.domains_all_collected_filepath
                    )
        if self.config.bruteforce:
            merge_lists(self, self.domains_all_collected_filepath,
                        self.gobuster_filepath,
                        self.domains_all_collected_filepath
                        )
        os.remove(self.subfinder_filepath)
        os.remove(self.findomain_filepath)
        if self.config.bruteforce:
            os.remove(self.gobuster_filepath)
        print_non_silent(self, "Finished merging the subdomain files")

    # merge the collected subdomain files into the file containing all the subdomains of this target that have ever been found. then remove the temporary file containing the collected subdomains
    def add_new_subdomains_to_master_file(self):
        print_non_silent(self, "Adding new subdomains to the master subdomain file...\n")
        if not os.path.exists(self.master_subdomain_list_filepath):
            open(self.master_subdomain_list_filepath, "w").close()
        merge_lists(self, self.domains_all_collected_filepath,
                             self.master_subdomain_list_filepath,
                             self.master_subdomain_list_filepath
                             )
        if os.path.exists(self.domains_all_collected_filepath):
            os.remove(self.domains_all_collected_filepath)
        print_non_silent(self, "Finished adding new subdomains to the master subdomain file.\n")

    # This method checks if the subdomains are alive
    def check_alive(self):
        print_non_silent(self, "checking which subdomains are alive...")
        subprocess.run(
            ["dnsx",
            "-l", self.master_subdomain_list_filepath, 
            "-o", self.alive_filepath,
            "-silent",
            "-retry", "5"],
            check=True,
            stdout=subprocess.DEVNULL
        )
        print_non_silent(self, "\nFinished checking alive subdomains.\n")
    
    # This method checks if the subdomains are responsive
    def check_responsive(self):
        print_non_silent(self, "checking which subdomains are responsive...")
        with open(self.responsive_filepath, "w") as responsive_file:
            subprocess.run(
                ["ffuf", "-u", "https://FUZZ",
                "-w", self.alive_filepath,
                "-s"],
                check=True,
                stdout=responsive_file,
                stderr=subprocess.STDOUT
            )
        print_non_silent(self, "\nFinished checking responsive subdomains.\n")

    # This method checks which subdomains are accessible
    def check_accessible(self):
        print_non_silent(self, "checking which subdomains are accessible...")
        with open(self.accessible_filepath, "w") as accessible_file:
            subprocess.run(
                ["ffuf", "-u", "https://FUZZ",
                "-w", self.responsive_filepath,
                "-s", "-fc", "404,403,401"],
                check=True,
                stdout=accessible_file,
                stderr=subprocess.STDOUT
            )
        print_non_silent(self, "\nFinished checking accessible subdomains.\n")