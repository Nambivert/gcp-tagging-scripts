import subprocess
import pandas as pd
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

def get_projects():
  cmd = run(['gcloud projects list --format=\"value(PROJECT_ID)\"'], stdout=PIPE, shell=True)
  gcp_projects = cmd.stdout.decode('utf-8')
  filename = "project_list.txt"
  file = open(filename, "w")
  file.write(gcp_projects)
  file.close()
  #print(gcp_projects)

def create_excel(project_id, bucket):
    csv_files = ['tags-compute_instances.csv', 'tags-compute_disks.csv', 'tags-compute_snapshots.csv', 'tags-compute_images.csv', 'tags-bigtable_instances.csv', 'tags-pubsub_subscriptions.csv', 'tags-pubsub_topics.csv', 'tags-forwarding_rules.csv', 'tags-vpn_tunnels.csv', 'tags-external_ip.csv']
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    filename = "GCP_Tagging"+"_"+project_id+"_"+date
    writer = pd.ExcelWriter(filename+'.xlsx', engine='openpyxl')
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        sheet_name = os.path.splitext(csv_file)[0]
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.close()
    run(['gsutil cp '+filename+' '+bucket+'/'+project_id+'/'], shell=True)
    
def compute_instances_tags(api_name, project_id, bucket):
    if api_found(api_name):
        cmd = run(['gcloud compute instances list --quiet --verbosity=none --project='+project_id+ ' ' + '--format=\"csv(name, labels.owner, labels.sponsor,labels.workload, labels.resource, labels.environment)\"'], stdout=PIPE, shell=True)
        instances = cmd.stdout.decode('utf-8')
        filename = "tags-compute_instances.csv"
        file = open(filename, "w")
        file.write(instances)
        file.close()
        run(['gsutil cp '+filename+' '+bucket+'/'+project_id+'/'], shell=True)
    else:
        print("Cannot list instances!, Compute API is not enabled") 

def compute_disks_tags(api_name, project_id, bucket):
    if api_found(api_name):
        cmd = run(['gcloud compute disks list --project='+project_id+ ' ' + '--format=\"csv(name, labels.owner, labels.sponsor,labels.workload, labels.resource, labels.environment)\"'], stdout=PIPE, shell=True)
        disks = cmd.stdout.decode('utf-8')
        filename = "tags-compute_disks.csv"
        file = open(filename, "w")
        file.write(disks)
        file.close()
        run(['gsutil cp '+filename+' '+bucket+'/'+project_id+'/'], shell=True)
    else:
        print("Cannot list disks!, Compute API is not enabled")

def compute_snapshots_tags(api_name, project_id, bucket):
    if api_found(api_name):
        cmd = run(['gcloud compute snapshots list --project='+project_id+ ' ' + '--format=\"csv(name, labels.owner, labels.sponsor,labels.workload, labels.resource, labels.environment)\"'], stdout=PIPE, shell=True)
        snapshots = cmd.stdout.decode('utf-8')
        filename = "tags-compute_snapshots.csv"
        file = open(filename, "w")
        file.write(snapshots)
        file.close()
        run(['gsutil cp '+filename+' '+bucket+'/'+project_id+'/'], shell=True)
    else:
        print("Cannot list snapshots!, Compute API is not enabled") 

def compute_images_tags(api_name, project_id, bucket):
    if api_found(api_name):
        cmd = run(['gcloud compute images list --project='+project_id+ ' ' + '--format=\"csv(name, labels.owner, labels.sponsor,labels.workload, labels.resource, labels.environment)\"'], stdout=PIPE, shell=True)
        images = cmd.stdout.decode('utf-8')
        filename = "tags-compute_images.csv"
        file = open(filename, "w")
        file.write(images)
        file.close()
        run(['gsutil cp '+filename+' '+bucket+'/'+project_id+'/'], shell=True)
    else:
        print("Cannot list images!, Compute API is not enabled") 

def bigtable_instances_tags(api_name, project_id, bucket):
        cmd = run(['gcloud bigtable instances list --project='+project_id+ ' ' + '--format=\"csv(name, labels.owner, labels.sponsor,labels.workload, labels.resource, labels.environment)\"'], stdout=PIPE, shell=True)
        bt_instances = cmd.stdout.decode('utf-8')
        filename = "tags-bigtable_instances.csv"
        file = open(filename, "w")
        file.write(bt_instances)
        file.close()
        run(['gsutil cp '+filename+' '+bucket+'/'+project_id+'/'], shell=True)

def pubsub_subscriptions_tags(api_name, project_id, bucket):
        cmd = run(['gcloud pubsub subscriptions list --project='+project_id+ ' ' + '--format=\"csv(name, labels.owner, labels.sponsor,labels.workload, labels.resource, labels.environment)\"'], stdout=PIPE, shell=True)
        pub_subscriptions = cmd.stdout.decode('utf-8')
        filename = "tags-pubsub_subscriptions.csv"
        file = open(filename, "w")
        file.write(pub_subscriptions)
        file.close()
        run(['gsutil cp '+filename+' '+bucket+'/'+project_id+'/'], shell=True)

def pubsub_topics_tags(api_name, project_id, bucket):
        cmd = run(['gcloud pubsub topics list --project='+project_id+ ' ' + '--format=\"csv(name, labels.owner, labels.sponsor,labels.workload, labels.resource, labels.environment)\"'], stdout=PIPE, shell=True)
        pub_topics = cmd.stdout.decode('utf-8')
        filename = "tags-pubsub_topics.csv"
        file = open(filename, "w")
        file.write(pub_topics)
        file.close()
        run(['gsutil cp '+filename+' '+bucket+'/'+project_id+'/'], shell=True)

def compute_forwarding_rules_tags(api_name, project_id, bucket):
    if api_found(api_name):
        cmd = run(['gcloud compute forwarding-rules list --project='+project_id+ ' ' + '--format=\"csv(name, labels.owner, labels.sponsor,labels.workload, labels.resource, labels.environment)\"'], stdout=PIPE, shell=True)
        forwarding_rules = cmd.stdout.decode('utf-8')
        filename = "tags-forwarding_rules.csv"
        file = open(filename, "w")
        file.write(forwarding_rules)
        file.close()
        run(['gsutil cp '+filename+' '+bucket+'/'+project_id+'/'], shell=True)
    else:
        print("Cannot list forwarding rules!, Compute API is not enabled")

def compute_vpn_tunnels_tags(api_name, project_id, bucket):
    if api_found(api_name):
        cmd = run(['gcloud compute vpn-tunnels list --project='+project_id+ ' ' + '--format=\"csv(name, labels.owner, labels.sponsor,labels.workload, labels.resource, labels.environment)\"'], stdout=PIPE, shell=True)
        vpn_tunnels = cmd.stdout.decode('utf-8')
        filename = "tags-vpn_tunnels.csv"
        file = open(filename, "w")
        file.write(vpn_tunnels)
        file.close()
        run(['gsutil cp '+filename+' '+bucket+'/'+project_id+'/'], shell=True)
    else:
        print("Cannot list vpn tunnels!, Compute API is not enabled")

def compute_external_ip_tags(api_name, project_id, bucket):
    if api_found(api_name):
        cmd = run(['gcloud compute forwarding-rules list --global --project='+project_id+ ' ' + '--format=\"csv(name, labels.owner, labels.sponsor,labels.workload, labels.resource, labels.environment)\"'], stdout=PIPE, shell=True)
        external_ip = cmd.stdout.decode('utf-8')
        filename = "tags-external_ip.csv"
        file = open(filename, "w")
        file.write(external_ip)
        file.close()
        run(['gsutil cp '+filename+' '+bucket+'/'+project_id+'/'], shell=True)
    else:
        print("Cannot list vpn tunnels!, Compute API is not enabled")
                
@app.route("/")
def home():
  return "It Works!"

@app.route("/tagging", methods=["POST"])
def gcp_tagging():
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405
    #Trigger all functions
    #get_projects()
    #with open("project_list.txt", "r") as project_list:
    # for project_id in project_list:
    compute_instances_tags(api_name, project_id, bucket)
    compute_disks_tags(api_name, project_id, bucket)
    compute_snapshots_tags(api_name, project_id, bucket)
    compute_images_tags(api_name, project_id, bucket)
    bigtable_instances_tags(api_name, project_id, bucket)
    pubsub_subscriptions_tags(api_name, project_id, bucket)
    pubsub_topics_tags(api_name, project_id, bucket)
    compute_forwarding_rules_tags(api_name, project_id, bucket)
    compute_vpn_tunnels_tags(api_name, project_id, bucket)
    compute_external_ip_tags(api_name, project_id, bucket)
    create_excel(project_id, bucket)
    # Return an HTTP response
    return "Tagging CSVs added successfully"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))