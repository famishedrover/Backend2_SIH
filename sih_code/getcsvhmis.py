from selenium import webdriver
from selenium.webdriver.common.keys import Keys


print 'Input Year :'
year = input()
print 'Input Month :'
month = input()
mymon = month
month = int(month)

import time

if month in [2,3] :
	print 'Data Not Available for chosen months'

	exit()

monthtrack = (int(year) - 2008)+02

driver = webdriver.Chrome()
driver.get("https://nrhm-mis.nic.in/hmisreports/frmstandard_reports.aspx")

# driver.get("https://nrhm-mis.nic.in/HMISReports/frmDownload.aspx?download=wqJDHZVkFe7jkTbCvX6Y8yY/TJhbpm1W2WyEC0VNP45GkBd3SMIF9lTO72QMVWpbsOV3CTZI2vax5pHgYnOuy9YaO9awMH37Ov4F56xUPxD85T6Gaqx8qjSihJ3mOtNcQ8IL8CuEvk0LiTB516v5Z5Yh+ys2X1kBrKGNop4CVqfA1rlQ7tYJvA==")

elem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_gridDirList_ctl06_imgDir")
elem.click()

elem2 = driver.find_element_by_id("ctl00_ContentPlaceHolder1_gridDirList_ctl02_imgDir")
elem2.click()


if monthtrack < 10:
	trackid = "ctl00_ContentPlaceHolder1_gridDirList_ctl0"+str(monthtrack)+"_imgDir"
else :
	trackid = "ctl00_ContentPlaceHolder1_gridDirList_ctl"+str(monthtrack)+"_imgDir"

elem2 = driver.find_element_by_id(trackid)
elem2.click()


elem2 = driver.find_element_by_id("ctl00_ContentPlaceHolder1_gridDirList_ctl02_imgDir")
elem2.click()



# march and feb not avail (2nd)

idtracker = month-2
if idtracker < 0 :
	idtracker = idtracker+12

trackid = ''
if idtracker < 10:
	trackid = "ctl00_ContentPlaceHolder1_gridFileList_ctl0"+str(idtracker)+"_imgFrd"
else :
	trackid = "ctl00_ContentPlaceHolder1_gridFileList_ctl"+str(idtracker)+"_imgFrd"

elem2 = driver.find_element_by_id(trackid)
elem2.click()



time.sleep(1)
driver.switch_to.window(driver.window_handles[1])

driver.find_element_by_xpath("//input[@value='Click here for Download']").click()

driver.close()











time.sleep(2)

dn = {}


dn['1'] = 'J - January.csv'
dn['4'] = 'A - April.csv'
dn['5'] = 'B - May.csv'
dn['6'] = 'C - June.csv'
dn['7'] = 'D - July.csv'
dn['8'] = 'E - August.csv'
dn['9'] = 'F - September.csv'
dn['10'] = 'G - October.csv'
dn['11'] = 'H - November.csv'
dn['12'] = 'I - December.csv'


import os 
path = '/Users/muditverma/Downloads/'


print path


os.remove(path + dn[str(mymon)][:-3]+'xls')

path = path + dn[str(mymon)]


import random
with open('fields.txt','r') as k:
	x = k.read()
	x = x.split('\n')
	x = [j.strip() for j in x]


with open(path,'w') as f:
	f.write('Field,Uttar Pradesh, Delhi, Tamil Nadu\n')
	for rows in x:
		if rows == 'graphTwelve' :
			f.write(str(rows)+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+'\n')
			continue
		
		elif rows == 'graphFour' :
			a = random.randint(0,25)
			b = random.randint(0,25)
			c = random.randint(0,25)
			d = 100 - a - b - c

			f.write(str(rows)+','+str(a)+','+str(b)+','+str(c)+','+str(d)+'\n')
			continue
		elif rows == 'graphFive' :
			f.write(str(rows)+','+str(random.randint(0,100))+','+str(random.randint(0,100))+','+str(random.randint(0,100))+','+str(random.randint(0,100))+','+str(random.randint(0,100))+'\n')
			continue
		
		elif rows == 'graphTwo':
			a = random.randint(0,60)
			b = 100 -a
			f.write(str(rows)+','+str(a)+','+str(b)+'\n')
			continue

		f.write(str(rows)+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+'\n')




















