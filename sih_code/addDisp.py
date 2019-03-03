import random
import requests

# with open('disp.txt') as f :
# 	x = f.read()

with open('disp_new.txt') as f :
	x = f.read()



x = x.split('\n')
z = []

# print x

for t in x :
	t = t.split(',')
	t = [j.strip() for j in t]
	t[0] = t[0].replace('.','')
	z.append(t)



# i=0
for md in z :
	
	if len(md) < 2 :
		continue


	# if i in [0,2,3,4] :
	# 	i+=1
	# 	continue

	# i+=1 

	print md

	data = {'pincode':md[3], 
	        'city':'Varanasi', 
	        'state':'Uttar Pradesh', 
	        'longitude':md[2],
	        'latitude':md[1]}
	r = requests.post(url = 'http://ddb281c5.ngrok.io/db/region/', data = data)

	hosp = {'username':str(random.random()), 
	        'password':'pass',
	        'first_name':md[0], 
	        'malaria_free':random.randint(0,10), 
	        'tb_free':random.randint(0,10),
	        'dengue_free':random.randint(0,10),
	        'pincode':md[3],
	        'type_user':'D'
	        }

	r = requests.post(url = 'http://ddb281c5.ngrok.io/db/hospital/', data = hosp)
	print r

