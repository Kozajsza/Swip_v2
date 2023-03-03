import tkinter
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import numpy as np
import sqlalchemy
import time
import datetime
import random
import xml.etree.ElementTree as ET


Tk().withdraw()
BlanccoReport = askopenfilename()

tree = ET.parse(BlanccoReport)
root = tree.getroot()



for child in root:
    print (child.tag, child.attrib)


