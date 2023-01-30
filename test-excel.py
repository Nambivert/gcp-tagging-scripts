import pandas as pd
import os
import datetime

# list of CSV file names
project_id = "gcp-id"
csv_files = ['compute_disk.csv', 'compute_disk-2.csv', 'compute_disk-3.csv']
date = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
filename = "GCP_Tagging"+"_"+project_id+"_"+date
# create an Excel writer object
writer = pd.ExcelWriter(filename+'.xlsx', engine='openpyxl')

# read each CSV file and write to a separate sheet in the Excel file
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    sheet_name = os.path.splitext(csv_file)[0]
    df.to_excel(writer, sheet_name=sheet_name, index=False)

# save the Excel file
writer.close()