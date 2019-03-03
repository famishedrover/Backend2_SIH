import random
import requests

with open('labs.txt') as f :
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

	if md[-1] is 'True' :
		md[-1] = True
	else :
		md[-1] = False

	data = {'pincode':md[3], 
	        'city':'Varanasi', 
	        'state':'Uttar Pradesh', 
	        'longitude':md[2],
	        'latitude':md[1]}
	r = requests.post(url = 'http://10.32.8.207:8000/db/region/', data = data)

	lab = {'username': str(random.random()), 
	        'password': 'pass', 
	        'pincode':md[3], 
	        'first_name':md[0],
	        'free':md[-1],
	        'type_user':'L'
	        }
	r = requests.post(url = 'http://10.32.8.207:8000/db/lab/', data = lab)
	print r




# data = {'pincode':API_KEY, 
#         'city':'paste', 
#         'state':source_code, 
#         'longitude':,
#         'latitude':}
# r = requests.post(url = API_ENDPOINT, data = data)

# disp = {'username':API_KEY, 
#         'password':'paste', 
#         'malaria_free':'D', 
#         'tb_free':,
#         'dengue_free':,
#         'pincode':
#         }
# r = requests.post(url = API_ENDPOINT, data = data)

# data = {'pincode':API_KEY, 
#         'city':'paste', 
#         'state':source_code, 
#         'longitude':,
#         'latitude':}
# r = requests.post(url = API_ENDPOINT, data = data)

# hosp = {'username':API_KEY, 
#         'password':'paste', 
#         'malaria_free':'H', 
#         'tb_free':,
#         'dengue_free':,
#         'pincode':
#         }

# r = requests.post(url = API_ENDPOINT, data = data)