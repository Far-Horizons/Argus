# This class will control the argument parsing for the Argus framework
import argparse

class ArgManager:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Argus - A recon tool by Horizon")
        self._configure_arguments()

    # Define the arguments here
    def _configure_arguments(self):
        self.parser.add_argument( #set the target domain
            "-t", "--target",
            help="Sets the target. Single domain for single-run mode, or target file for monitoring mode."
        )

        modeGroup = self.parser.add_mutually_exclusive_group(required=True) # group that sets mode (single-run or monitoring)

        modeGroup.add_argument(
            "-s", "--single-run",
            help="Run a single subdomain enumeration and exit. This is the default mode if no other mode is specified."
        )

        modeGroup.add_argument(
            "--monitoring-mode",
            default=False,
            action='store_true',
            help="enable monitoring mode, for periodic scanning and comparisons. Mainly intended for use in automated VPS setups."
        )

        self.parser.add_argument( #set silent mode
            "--silent",
            default=False,
            action='store_true',
            help="Run in silent mode, which gives no output to the console. Only affects single-run mode, as monitoring mode is always silent."
        )

        self.parser.add_argument(
            "-i", "--interval",
            type = int,
            default = 3600,
            help="In monitoring mode, sets the interval (in seconds) between scan cycles. Default is 3600 seconds (1 hour). Other useful values are: 900 (15 minutes), 1800 (30 minutes), 7200 (2 hours) and 14400 (4 hours)."
        )

        self.parser.add_argument(
            "--monitor-debug",
            default=False,
            action='store_true',
            help="Enable debug mode for monitoring, which forces it to not be silent and print debug information to the console."
        )

        self.parser.add_argument(
            "-b", "--bruteforce",
            default=False,
            action='store_true',
            help="Enable bruteforcing mode, which makes Argus attempt to bruteforce any new subdomains using GoBuster on every cycle. This uses the SubdomainBruteforceWordlists.txt in your Argus folder"
        )

        self.parser.add_argument(
            "-tr", "--threads-responsive",
            type = int,
            default = 1,
            help="Set a multiplier for the threads used for checking if subdomains are responsive. Default is a multiplier of 1. A higher multiplier will result in higher speed, but might lead to rate-limiting"
        )

        self.parser.add_argument(
            "-ta", "--threads-accesible",
            type = int,
            default = 1,
            help="Set a multiplier for the threads used for checking if subdomains are accessible. Default is a multiplier of 1. A higher multiplier will result in higher speed, but might lead to rate-limiting"
        )

        self.parser.add_argument(
            "--screenshots",
            default=False,
            action='store_true',
            help='Enable screenshot capturing and sending (to webhook) of new responsive subdomains found during monitoring.'
        )

        self.parser.add_argument(
            "--screenshotwebhook",
            type= str,
            help="Set the webhook to which the screenshots will be sent (needed as screenshots do not rely upon PDs notify)"
        )