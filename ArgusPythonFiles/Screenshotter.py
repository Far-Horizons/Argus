# Takes screenshots of web pages using gowitness
import os
import subprocess
import requests
from ArgusHelperMethods import print_non_silent
from time import sleep
import shutil

class Screenshotter:
    def __init__(self, targetlist, webhookURL, config):
        self.targetlist: list = targetlist    #target is provided as a list of URLs or IPs
        self.webhookURL: str =  webhookURL
        self.valid_ext = ".jpeg"
        self.config = config
        self.screenshotpath = os.path.expanduser("~/Argus/gowitness_screenshots")
    
    def run(self):
        targetcounter = 0
        for target in self.targetlist:
            self.take_screenshot(target)
            targetcounter += 1
        print_non_silent(self, f"\ntook screenshots of {targetcounter} targets, attempting to send now\n")

        self.send_screenshots()
        print_non_silent(self, f"sent screenshots to the webhook")

        self.clear_screenshots()



    def take_screenshot(self, target):
        if target != None:
            try:
                subprocess.run(
                    ["gowitness", "scan", "single",
                    "-u", f"http://{target}",
                    "--screenshot-fullpage",
                    "--screenshot-path", f"{self.screenshotpath}"],
                    check=True,
                    stdout=subprocess.DEVNULL)
                print_non_silent(self, f"\ntook a screenshot of http://{target}")
            except subprocess.CalledProcessError as e:
                print_non_silent(self, f"Failed to screenshot http://{target}: {e}")
            try:
                subprocess.run(
                    ["gowitness", "scan", "single",
                    "-u", f"https://{target}",
                    "--screenshot-fullpage",
                    "--screenshot-path", f"{self.screenshotpath}"],
                    check=True,
                    stdout=subprocess.DEVNULL)
                print_non_silent(self, f"\ntook a screenshot of https://{target}")
            except subprocess.CalledProcessError as e:
                print_non_silent(self, f"Failed to screenshot https://{target}: {e}")
        
    
    def send_screenshots(self):
        if os.path.exists(self.screenshotpath):
            for filename in os.listdir(self.screenshotpath):
                if not filename.lower().endswith(self.valid_ext):
                    continue

                path = os.path.join(self.screenshotpath, filename)

                with open(path, "rb") as f:
                    response = requests.post(
                        self.webhookURL,
                        data={"content": f"Uploading: {filename}"},
                        files={"file": (filename, f)}
                    )
                
                if response.status_code == 204:
                    print_non_silent(self, f"Successfully uploaded: {filename}")
                else:
                    print_non_silent(self, f"Failed upload: {filename} | {response.status_code} | {response.text}")
                
                sleep(1) # avoid rate limiting
        else: print_non_silent(self, f"\n!!!\nNo screenshots found, skipping to next step\n!!!\n")

    def clear_screenshots(self):
        if os.path.exists(self.screenshotpath):
            shutil.rmtree(self.screenshotpath)