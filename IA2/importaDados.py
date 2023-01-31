

import sqlite3
import pandas as pd

#data_paths = [os.path.join(pth, f)
#for pth, dirs, files in os.walk('../input/soccer/') for f in files]

#(after executing the above two code statements we get path directory - '../input/soccer/database.sqlite')

#After we got our directory path we have to import the data for that we can use the below code.


cnx = sqlite3.connect('database.sqlite')
df = pd.read_sql_query("SELECT * FROM Player", cnx)