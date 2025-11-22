# Contains the helper methods used in various parts of Argus

# helper method to print only if not in silent mode
def print_non_silent(self, stringtoprint):
    if not self.config.silent:
        print(stringtoprint)
'''
# This method sets up the domain name
def setup_domain_name(self):
    domain_name = ""
    domainparts = self.config.target.split('.')
    for part in domainparts:
        if part == domainparts[-1]:
            domain_name += part.lower()
        else:
            domain_name += part.lower() + "_"
    return domain_name
'''
# Helper method that merges lists, removes duplicates and normalizes domains
def merge_lists(self, filename1, filename2, output_filename):
    unique_domains = set()

    # Read domains from the first file
    with open(filename1, 'r') as file1:
        for line in file1:
            normalized_domain = normalize_domain(self, line)
            if normalized_domain:
                unique_domains.add(normalized_domain)

    # Read domains from the second file
    with open(filename2, 'r') as file2:
        for line in file2:
            normalized_domain = normalize_domain(self, line)
            if normalized_domain:
                unique_domains.add(normalized_domain)

    # Write the unique domains to the output file
    with open(output_filename, 'w') as output_file:
        for domain in sorted(unique_domains):
            output_file.write(domain + '\n')

# helper method that normalizes the subdomain format
def normalize_domain(self, domain):
    if not domain:
        return None
    d = domain.strip()
    d = d.split("://", 1)[-1] # remove http(s)://
    d = d.split("/", 1)[0] # remove trailing / or entire paths
    if d.startswith("*."): # remove wildcard prefix
        d = d[2:]
    if d.endswith("."): # remove trailing dot
        d = d[:-1]
    if d.startswith("."): # remove leading dot
        d = d[1:]
    d = d.lower()

    # sanity checks:
    if not d:       # empty domain
        return None
    if " " in d:    # domain with spaces
        return None
    if d.count(".") < 1:  # domain without extension
        return None
    if d.count("..") > 0: # domain with double dots
        return None
        
    return d