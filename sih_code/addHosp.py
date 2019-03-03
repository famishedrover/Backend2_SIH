import random
import requests

with open('hosp.txt') as f :
	x = f.read()



x = x.split('\n')
z = []


for t in x :
	t = t.split(',')
	t = [j.strip() for j in t]
	t[0] = t[0].replace('.','')
	z.append(t)




for md in z :
	if len(md) < 2 :
		continue
	print md

	data = {'pincode':md[3], 
	        'city':'Varanasi', 
	        'state':'Uttar Pradesh', 
	        'longitude':md[2],
	        'latitude':md[1]}
	r = requests.post(url = 'http://10.32.8.207:8000/db/region/', data = data)

	hosp = {'username':str(random.random()), 
	        'password':'pass', 
	        'first_name':md[0],
	        'malaria_free':random.randint(0,10), 
	        'tb_free':random.randint(0,10),
	        'dengue_free':random.randint(0,10),
	        'pincode':md[3],
	        'type_user':'H'
	        }

	r = requests.post(url = 'http://10.32.8.207:8000/db/hospital/', data = hosp)
	print r

