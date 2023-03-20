import pandas as pd
import lxml.etree as ET  # change to "import lxml.etree as ET"
import tkinter
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import datetime
from datetime import datetime
import random
import sqlalchemy
import os
import shutil

# Define the source and destination directories
source_dir = '\\\\FM_WEEE_NAS\\BlanccoReports\\unassigned'
destination_dir = '\\\\FM_WEEE_NAS\\BlanccoReports\\archive'

#Tk().withdraw()
#file = askopenfilename()
date = datetime.now()
# Format the date and time as a string
date_time_str = date.strftime("%m%d%M")
engine = sqlalchemy.create_engine('sqlite:///db.sqlite3')


today = datetime.today().strftime('%Y-%m-%d')

# Create the destination directory if it doesn't already exist
destination_path = os.path.join(destination_dir, today)
if not os.path.exists(destination_path):
    os.makedirs(destination_path)

files = os.listdir(source_dir)
print(files)

for file in files:
    source_path = os.path.join(source_dir, file)
    try:
        tree = ET.parse(source_path)
        root = tree.getroot()

        # Get the erasure entries
        erasure_entries = root.findall('.//blancco_erasure_report/entries[@name="erasures"]/entries[@name="erasure"]')
        drive_entries = root.findall('.//blancco_erasure_report/entries[@name="erasures"]/entries[@name="erasure"]/entries[@name="target"]')
        system_entries = root.findall('.//blancco_hardware_report/entries[@name="system"]')
        cpu_entries = root.findall('.//blancco_hardware_report/entries[@name="processors"]/entries[@name="processor"]')
        ram_entries = root.findall('.//blancco_hardware_report/entries[@name="memory"]')
        gpu_entries = root.findall('.//blancco_hardware_report/entries[@name="video_cards"]/entries[@name="video_card"]')
        user_entries = root.findall('.//user_data/entries[@name="fields"]')
        # Create a dictionary to store the column names and content
        data = {}

        for erasure_entry in erasure_entries:
            for child in erasure_entry:
                name = child.get('name')
                content = child.text
                if name in data:
                    data[name].append(content)
                else:
                    data[name] = [content]


        # Get the column names from the first erasure entry
        drive_entry = drive_entries[0]
        column_names = [child.get('name') for child in drive_entry]

        # Add the column names to the dictionary
        for name in column_names:
            data[name] = []

        for system_entry in system_entries:
            for child in system_entry:
                name = str(child.get('name') + "_system")
                content = child.text 
                if name in data:
                    data[name].append(content)
                else:
                    data[name] = [content]

        # Extract the content from each drive entry
        for drive_entry in drive_entries:
            for child in drive_entry:
                name = str(child.get('name') + "_drive")
                content = child.text
                if name in data:
                    data[name].append(content)
                else:
                    data[name] = [content]


        for cpu_entry in cpu_entries:
            for child in cpu_entry:
                name = str(child.get('name') + "_cpu")
                content = child.text
                if name in data:
                    data[name].append(content)
                else:
                    data[name] = [content]

        for ram_entry in ram_entries:
            for child in ram_entry:
                name = str(child.get('name') + "_ram")
                content = child.text
                if name in data:
                    data[name].append(content)
                else:
                    data[name] = [content]

        for gpu_entry in gpu_entries:
            for child in gpu_entry:
                name = str(child.get('name') + "_gpu")
                content = child.text
                if name in data:
                    data[name].append(content)
                else:
                    data[name] = [content]

        for user_entry in user_entries:
            for child in user_entry:
                name = str(child.get('name') + "_user")
                content = child.text
                if name in data:
                    data[name].append(content)
                else:
                    data[name] = [content]

        # Fill missing data points with None
        max_len = max(len(lst) for lst in data.values())
        for name in data.keys():
            lst = data[name]
            if len(lst) < max_len:
                lst += [None] * (max_len - len(lst))

        # Generate four random numbers
        random_numbers = [random.randint(0, 9) for _ in range(2)]

        # Combine the date and time string with the random numbers
        dateoutput = date_time_str + "".join(str(x) for x in random_numbers)
        # Create the Pandas DataFrame
        df = pd.DataFrame(data)

        df['Order_Number_id'] = pd.Series(dtype='int')

        if df['QR Code_user'].isnull().all():
            df['Asset_QR'] = "FM" + dateoutput
        else:
            df['Asset_QR'] = df['QR Code_user']

        df['Type'] = df['chassis_type_system']
        df['Make'] = df['manufacturer_system']
        df['Make'] = df['Make'].str.replace('Inc.', '', regex=False)
        df['Make'] = df['Make'].str.replace('Hewlett-Packard', 'HP', regex=False)
        df['Model'] = df['model_system']
        df['Model'] = df['Model'].str.replace('HP', '', regex=False)
        df['Serial_Number'] = df['serial_system']

        df['CPU'] = df['model_cpu']
        df['CPU'] = df['CPU'].str.replace('(R)', '', regex=False)
        df['CPU'] = df['CPU'].str.replace('(TM)', '', regex=False)
        df['CPU'] = df['CPU'].str.replace('CPU', '', regex=False)


        df['RAM'] = df['total_memory_ram'].astype(float)
        df['RAM'] = df['RAM'].div(1073741824)

        df['Storage'] = df['vendor_drive'] + ' ' + df['model_drive']
        df['Storage_Serial_Number'] = df['serial_drive']
        df['Storage_Capacity'] = df['capacity_drive'].astype(float)
        df['Storage_Capacity'] = df['Storage_Capacity'].div(1073741824).round(1)

        df['GPU'] = df['vendor_gpu'] + ' ' + df['model_gpu']



        df['Motherboard_Test'] = 'Pass'
        df['CPU_Test'] = 'Pass'
        df['RAM_Test'] = 'Pass'

        df['Wipe_Method'] = df['erasure_standard_name']
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['Wipe_Start_Time'] = df['start_time'].dt.strftime('%A, %d %B %Y at %H:%M:%S')
        df['end_time'] = pd.to_datetime(df['end_time'])
        df['Wipe_End_Time'] = df['end_time'].dt.strftime('%A, %d %B %Y at %H:%M:%S')
        df['Wipe_Result'] = df['state']
        df['Weight'] = '0'
        df['Ecommerce_Title']= df['Make'] + ' ' + df['Model'] + ' ' + df['CPU'] + ' ' + df['RAM'].astype(str) + 'GB RAM' + df['Storage_Capacity'].astype(str)
        df['Ecommerce_Category']=''
        df['Ecommerce_Condition']='3000'
        df['Ecommerce_Condition_Description']=''
        with open('ebaydesc.txt.', 'r') as f:
            desc = f.read()
        df['Ecommerce_Item_Description'] = desc
        df['Ecommerce_Price']='0'
        df['Ecommerce_SuitableFor']='Casual Computing'
        df['Ecommerce_FormFactor']= df['chassis_type_system']
        df['Ecommerce_Features']=''
        df['Ecommerce_Connectivity']=''
        df['Created'] = date
        df['Updated'] = date



        df = df[
                    [
                        'Order_Number_id', 'Asset_QR', 'Type', 'Make', 'Model', 'Serial_Number', 'CPU', 'RAM', 'Storage', 'Storage_Serial_Number', 'Storage_Capacity',
                        'GPU', 'Motherboard_Test', 'CPU_Test', 'RAM_Test', 'Wipe_Method', 'Wipe_Start_Time', 'Wipe_End_Time', 'Wipe_Result',
                        'Weight', 'Ecommerce_Title', 'Ecommerce_Category', 'Ecommerce_Condition', 'Ecommerce_Condition_Description', 'Ecommerce_Item_Description', 'Ecommerce_Price',
                        'Ecommerce_SuitableFor', 'Ecommerce_FormFactor','Ecommerce_Features', 'Ecommerce_Connectivity' ,'Created', 'Updated'
                    ]
                ]
        df = df.drop_duplicates(subset='Serial_Number', keep="first") #for some reason pandas sometimes duplicates some of the records, this drops duplicate records
        df = df.iloc[[0]] #leaves only the first row
        # Print the resulting DataFrame
        df.to_sql('SWIPapp_asset',engine, if_exists='append', index=False)


        new_filename = today + '_' + ''.join(str(num) for num in random_numbers) + os.path.splitext(file)[1]
        destination_path = os.path.join(destination_dir, today, new_filename)
        shutil.move(source_path, destination_path)
        print(df)

    except Exception as e:
        print(f"Error reading file {file}: {e}")
#df.to_csv('report.csv')