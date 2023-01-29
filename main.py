import subprocess
import os
import json
from flask import Flask
from flask import request
from flask import jsonify
import functions_framework
import csv
from sys import stdout
import argparse
from subprocess import run, PIPE
import datetime
import sys

app = Flask(__name__)
api_name = os.environ['API_NAME'] #"compute"
bucket = os.environ['BUCKET']#"gs://gcp-tags"
project_id = os.environ['PROJECT'] #"mineral-anchor-361313"

def api_found(api_string):
    api_present = os.system("gcloud services list --enabled --project {} > api_present.txt".format(project_id))
    #print(api_present)

    with open("api_present.txt", "r") as api_file:
        contents = api_file.read()
        if api_string in contents:
            return 1

def compute_disks_enabled(api_name, project_id, bucket):
    if api_found(api_name):
        cmd = run(['gcloud compute disks list --project='+project_id+ ' ' + '--format=\"csv(name, labels.owner, labels.sponsor,labels.workload, labels.resource, labels.environment)\"'], stdout=PIPE, shell=True)
        disks = cmd.stdout.decode('utf-8')
        filename = "compute_disk.csv"
        file = open(filename, "w")
        file.write(disks)
        file.close()
        run(['gsutil cp '+filename+' '+bucket], shell=True)
    else:
        print("Compute API is not enabled") 
        


@app.route("/")
def home():
  return "It Works!"

@app.route("/tagging", methods=["POST"])
def gcp_tagging():
  if request.method != 'POST':
        return 'Only POST requests are accepted', 405
    
  compute_disks_enabled(api_name, project_id, bucket)
  # Return an HTTP response
  return "Tagging CSVs added successfully"
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))