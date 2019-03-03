path = '/Users/muditverma/Downloads'


filename = 'E - August.html'

path = path+'/'+filename


import pandas as pd

# workbook_df=pd.ExcelFile(path)
# key_sheet = workbook_df.parse("All India")

df  = pd.read_html(path)

for xdf in df:
	# print xdf.head()
	print xdf[xdf.keys()[1][1]]


	# print xdf['Assam']

# df = pd.read_excel(path)

# with open(path) as f:
# 	x = f.read()



# df.head()

# correct 8th

def getFieldss(state):
	with open('fields.txt') as f:
		

getFields('Uttar Pradesh')












































def getFields(state):
	pass









