
# DONOT RUN AGAIN!! <-- Time : 24 mins -->


import torch

from serverconnect import db 

from ('model.pkl','w') as f:
	model = f.read()

model.eval()


# dataset from twitter
tw = db.apicall('192.168.0.1:5000/dbcall/tweets')
fb = db.apicall('192.168.0.1:5000/dbcall/facebook')
news = db.apicall('192.168.0.1:5000/dbcall/news')

hosp = db.apicall('192.168.0.1:5000/dbcall/hosp')
user = db.apicall('192.168.0.1:5000/dbcall/hosp')
lab = db.apicall('192.168.0.1:5000/dbcall/lab')


# case thresh rate : 20 in 1 day

finalscore_pinwise = 0.1*model(tw) + 0.1*model(fb) + 0.1*model(news) + 0.2*hosp['intensity'] + 0.2*user['intensity'] + 0.2*lab['intensity']

with open('model.txt') as f:
	f.write(str(finalscore_pinwise))