import subprocess
import time
import argparse

parser = argpars.ArgumentParser(description="Check for WLAN Strength.")
parser.add_argument(dest="interfce",nargs="?", default="wlan0", help="wlan_strength <interface> (default=wlan0)")
args = parser.parse_args()

print "Ctrl-C to quit."
while True:
  try:
     cmd = 'iwconfig %s' %s args.interface
     process = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
     for line in process.stdout:
        if 'Link Quality' in line:
           print line
  exception KeyboardInterrupt:
     break
     

