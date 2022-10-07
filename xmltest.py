import tkinter
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
from tabulate import tabulate
import json
import xml.etree.ElementTree as et

Tk().withdraw()
report = askopenfilename()
#ata = json.load(open(report))
#df = pd.DataFrame(data["id"])
#df = pd.read_json(report)
#print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
#df = df.to_csv('test.csv', index=False)

xtree = et.parse(report)
xroot = xtree.getroot()

df_cols = ['product', 'vendor', 'serial']
rows = []

for node in xroot:
    product = node.find('core').text
    #vendor = node.find('vendor').text
    #serial = node.find('serial').text

    rows.append({'core':product})

out_df = pd.DataFrame(rows, columns=df_cols)
print(out_df)