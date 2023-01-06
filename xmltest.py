import tkinter
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import sqlalchemy
import time
import datetime
import random

Tk().withdraw()
report = askopenfilename()
date = datetime.datetime.now()
engine = sqlalchemy.create_engine('sqlite:///db.sqlite3')

#GENERAL INFO EXTRACTION:
try:
    geninfo = pd.read_html(report, match='mint') #searching for top table info in the html
    geninfoarr = np.array(geninfo) #turning it into a numpy array
    geninfoarr2 = np.reshape(geninfoarr, (-1,3)) #reshaping the array from 1d list to 2d frame
    geninfodf = pd.DataFrame(geninfoarr2) #opening new data frame
    geninfodf = geninfodf.transpose() #flip collumns with rows
    new_header = geninfodf.iloc[0] #grab the first row for the header
    geninfodf = geninfodf[1:] #take the data less the header row
    geninfodf.columns = new_header #set the header row as the df header
    #reshaping the dataframe:
    geninfodf['Type'] = geninfodf['description:']
    geninfodf['Make'] = geninfodf['vendor:']
    geninfodf['Model'] = geninfodf['product:']
    geninfodf['Serial Number'] = geninfodf['serial:']
    geninfodf = geninfodf.dropna()
    geninfodf = geninfodf [['Type', 'Make' , 'Model', 'Serial Number']]
except:
    geninfodf = pd.DataFrame(index=['Type', 'Make' , 'Model', 'Serial Number'])
    geninfodf = geninfodf.transpose()

#CPU INFO EXTRACTION:

try:
    cpuinfo = pd.read_html(report, match='cpu') #searching for cpu table info in the html
    cpuinfoarr = np.array(cpuinfo)
    cpuinfoarr2 = np.reshape(cpuinfo, (-1,3))
    cpuinfodf = pd.DataFrame(cpuinfoarr2)
    cpuinfodf = cpuinfodf.transpose() #flip collumns with rows
    cpu_header = cpuinfodf.iloc[0] #grab the first row for the header
    cpuinfodf = cpuinfodf[1:] #take the data less the header row
    cpuinfodf.columns = cpu_header #set the header row as the df header
    #reshaping the dataframe:
    cpuinfodf['CPU'] = cpuinfodf['product:']
    cpuinfodf = cpuinfodf.dropna()
    cpuinfodf = cpuinfodf[['CPU']]

except:
    cpuinfodf = pd.DataFrame(index=['CPU'])
    cpuinfodf = cpuinfodf.transpose()

#MEMORY INFO EXTRACTION:

try:
    meminfo = pd.read_html(report, match='System Memory') #searching for cpu table info in the html
    meminfoarr = np.array(meminfo)
    meminfoarr2 = np.reshape(meminfo, (4,2))
    meminfodf = pd.DataFrame(meminfoarr2)
    meminfodf = meminfodf.transpose()
    meminfo_header = meminfodf.iloc[0]
    meminfodf = meminfodf[1:]
    meminfodf.columns = meminfo_header
    meminfodf['RAM'] = meminfodf['size:']
    meminfodf = meminfodf.dropna()
    meminfodf = meminfodf[['RAM']]
except:
    meminfodf = pd.DataFrame(index=['RAM'])
    meminfodf = meminfodf.transpose()


#NVME STORAGE INFO EXTRACTION:

try:
    nvmeinfo = pd.read_html(report, match='NVMe device')
    nvmeinfoarr = np.array(nvmeinfo)
    nvmeinfoarr2= np.reshape(nvmeinfoarr, (-1,3))
    nvmeinfodf = pd.DataFrame(nvmeinfoarr2)
    nvmeinfodf = nvmeinfodf.transpose()
    nvmeinfo_header = nvmeinfodf.iloc[0] #grab the first row for the header
    nvmeinfodf = nvmeinfodf[1:] #take the data less the header row
    nvmeinfodf.columns = nvmeinfo_header #set the header row as the df header
    nvmeinfodf['nvme_Storage'] = nvmeinfodf['vendor:'] + ' ' + nvmeinfodf['product:']
    nvmeinfodf['nvme_Storage_Serial_Number'] = nvmeinfodf['serial:']
    nvmeinfodf = nvmeinfodf[['nvme_Storage', 'nvme_Storage_Serial_Number']]

except:
    nvmeinfodf = pd.DataFrame(index=['nvme_Storage', 'nvme_Storage_Serial_Number'])
    nvmeinfodf = nvmeinfodf.transpose()


    
#NVME STORAGE CAPACITY EXTRACTION:

try:
    nvmecap = pd.read_html(report,match='/dev/nvme0n1')
    nvmecaparr = np.array(nvmecap, dtype=object)
    try:
        nvmecaparr2 = np.reshape(nvmecaparr, (3,10))
        nvmecapdf = pd.DataFrame(nvmecaparr2)
        nvmecap_header = nvmecapdf.iloc[0] #grab the first row for the header
        nvmecapdf = nvmecapdf[1:] #take the data less the header row
        nvmecapdf.columns = nvmecap_header #set the header row as the df header
        nvmecapdf['nvme_Storage_Capacity'] = nvmecapdf['physical id:']
        nvmecapdf = nvmecapdf.drop([2])
        nvmecapdf[['nvme_Storage_Capacity', 'x']] = nvmecapdf['nvme_Storage_Capacity'].str.split(' ', n=1, expand=True)
        nvmecapdf['nvme_Storage_Capacity'] = nvmecapdf['nvme_Storage_Capacity'].str.replace('(', '', regex=False)
        nvmecapdf['nvme_Storage_Capacity'] = nvmecapdf['nvme_Storage_Capacity'].str.replace(')', '', regex=False)
        nvmecapdf['nvme_Storage_Capacity'] = nvmecapdf['nvme_Storage_Capacity'].str.replace('GiB', '', regex=False)
        nvmecapdf['nvme_Storage_Capacity'] = nvmecapdf['nvme_Storage_Capacity'].astype(float)
        nvmecapdf = nvmecapdf[['nvme_Storage_Capacity']]
        nvmecapdf.to_csv('nvme.csv')
        print(nvmecapdf)

    except:
        nvmecaparr2 = np.reshape(nvmecaparr,(1,1,5))
        nvmecaparr3 = nvmecaparr2[0, 0, 0]
        nvmecapdf = pd.DataFrame(nvmecaparr3)
        nvmecapdf = nvmecapdf.transpose()
        nvmecap_header = nvmecapdf.iloc[0] #grab the first row for the header
        nvmecapdf = nvmecapdf[1:] #take the data less the header row
        nvmecapdf.columns = nvmecap_header #set the header row as the df header
        nvmecapdf['nvme_Storage_Capacity'] = nvmecapdf['size:']
        nvmecapdf = nvmecapdf.dropna(0)
        nvmecapdf[['nvme_Storage_Capacity', 'x']] = nvmecapdf['nvme_Storage_Capacity'].str.split(' ', n=1, expand=True)
        nvmecapdf['nvme_Storage_Capacity'] = nvmecapdf['nvme_Storage_Capacity'].str.replace('GiB', '', regex=False)
        nvmecapdf['nvme_Storage_Capacity'] = nvmecapdf['nvme_Storage_Capacity'].astype(float)
        nvmecapdf = nvmecapdf[['nvme_Storage_Capacity']]
        nvmecapdf.to_csv('nvme.csv')
        print(nvmecapdf)


except:
    #print('nvme device not found, creating an empty array')
    nvmecapdf = pd.DataFrame(index=['nvme_Storage_Capacity'])
    nvmecapdf = nvmecapdf.transpose()



#SATA STORAGE INFO EXTRACTION:

try:
    satainfo = pd.read_html(report, match='ATA Disk')
    satainfoarr = np.array(satainfo)
    satainfoarr2 = np.reshape(satainfoarr,(15,3))
    satainfodf = pd.DataFrame(satainfoarr2)
    satainfodf = satainfodf.transpose()
    satainfo_header = satainfodf.iloc[0] #grab the first row for the header
    satainfodf = satainfodf[1:] #take the data less the header row
    satainfodf.columns = satainfo_header #set the header row as the df header
    satainfodf ['sata_Storage'] = satainfodf['vendor:'] + ' ' + satainfodf['product:']
    satainfodf['sata_Storage_Serial_Number'] = satainfodf['serial:']
    satainfodf['sata_Storage_Capacity'] = satainfodf['size:']
    satainfodf = satainfodf.dropna()
    satainfodf[['sata_Storage_Capacity', 'x']] = satainfodf['sata_Storage_Capacity'].str.split(' ', n=1, expand=True)
    satainfodf['sata_Storage_Capacity'] = satainfodf['sata_Storage_Capacity'].str.replace('(', '', regex=False)
    satainfodf['sata_Storage_Capacity'] = satainfodf['sata_Storage_Capacity'].str.replace(')', '', regex=False)
    satainfodf['sata_Storage_Capacity'] = satainfodf['sata_Storage_Capacity'].str.replace('GiB', '', regex=False)
    satainfodf['sata_Storage_Capacity'] = satainfodf['sata_Storage_Capacity'].astype(int)
    satainfodf = satainfodf[['sata_Storage', 'sata_Storage_Serial_Number', 'sata_Storage_Capacity']]


except(ValueError):
    #print('sata device not found, creating an empty array')
    satainfodf = pd.DataFrame(index=['sata_Storage', 'sata_Storage_Serial_Number', 'sata_Storage_Capacity'])
    satainfodf = satainfodf.transpose()


#GPU INFO EXTRACTION:
try:
    gpuinfo = pd.read_html(report, match='display')
    gpuinfoarr = np.array(gpuinfo)
    gpuinfoarr2 = np.reshape(gpuinfoarr,(21,3))
    gpuinfodf = pd.DataFrame(gpuinfoarr2)
    gpuinfodf = gpuinfodf.transpose()
    gpuinfo_header = gpuinfodf.iloc[0] #grab the first row for the header
    gpuinfodf = gpuinfodf[1:] #take the data less the header row
    gpuinfodf.columns = gpuinfo_header #set the header row as the df header
    gpuinfodf['GPU'] = gpuinfodf['vendor:'] + ' ' + gpuinfodf['product:']
    gpuinfodf = gpuinfodf[['GPU']]

except:
    gpuinfodf = pd.DataFrame(index=['GPU'])
    gpuinfodf = gpuinfodf.transpose()

# Get the current date and time
now = datetime.datetime.now()

# Format the date and time as a string
date_time_str = now.strftime("%m%d%M")

# Generate four random numbers
random_numbers = [random.randint(0, 9) for _ in range(2)]

# Combine the date and time string with the random numbers
dateoutput = date_time_str + "".join(str(x) for x in random_numbers)


df = pd.concat([geninfodf, cpuinfodf, meminfodf, nvmeinfodf, nvmecapdf, satainfodf, gpuinfodf], axis=1)
df.to_csv('testbefore.csv', index=False)
engine = sqlalchemy.create_engine('sqlite:///db.sqlite3')

df['Order_Number_id'] = pd.Series(dtype='int')
df['Asset_QR'] = 'FM' + dateoutput
#Type is ok
#Make is ok
#Model is ok
df['Serial_Number'] = df['Serial Number']
#cpu is ok
df['RAM'] = df['RAM'].str.replace('GiB', '', regex=False)
df['RAM'] = df['RAM'].fillna(0)
df['RAM'] = df['RAM'].astype(int)

df['Storage'] = df['nvme_Storage'].fillna(df['sata_Storage'])
df['Storage_Serial_Number'] = df['nvme_Storage_Serial_Number'].fillna(df['sata_Storage_Serial_Number'])
df['Storage_Capacity'] = df['nvme_Storage_Capacity'].fillna(df['sata_Storage_Capacity'])

row_1 = df.iloc[0]['Storage_Capacity']

if pd.notnull(row_1):
    pass
else:
    df['Storage_Capacity'] = df['Storage_Capacity'].shift(-2)

#gpu is ok

df['Motherboard_Test'] = 'Pass'
df['CPU_Test'] = 'Pass'
df['RAM_Test'] = 'Pass'

df['Wipe_Method'] = 'None'
df['Wipe_Start_Time'] = 'None'
df['Wipe_End_Time'] = 'None'
df['Wipe_Result'] = 'None'
df['Weight'] = '0'
df['Ecommerce_Title']= df['Make'] + ' ' + df['Model'] + ' ' + df['CPU'] + ' ' + df['RAM'].astype(str) + 'GB RAM' + ' ' + df['Storage_Capacity'].astype(str)
df['Ecommerce_Category']=''
df['Ecommerce_Condition']=''
df['Ecommerce_Condition_Description']=''
df['Ecommerce_Item_Description']=''
df['Ecommerce_Price']='0'
df['Ecommerce_SuitableFor']='Casual Computing'
df['Ecommerce_FormFactor']=''
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

df = df.drop(df.index[1:])

df.to_csv('finaltest.csv', index=False)
df.to_sql('SWIPapp_asset',engine, if_exists='append', index=False)