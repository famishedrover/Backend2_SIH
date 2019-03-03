import random

def callState(st):
  j = {}
  with open(st+'.txt','w') as f:

    j['graph12'] = random.sample(range(40000),12)
    f.write('graph12'+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+','+str(random.randint(0,40000))+'\n')

    a = random.randint(0,25)
    b = random.randint(0,25)
    c = random.randint(0,25)
    d = 100 - a - b - c
    f.write('graph4'+','+str(a)+','+str(b)+','+str(c)+','+str(d)+'\n')
    j['graph4'] = [a,b,c,d]

    f.write('graph5'+','+str(random.randint(0,100))+','+str(random.randint(0,100))+','+str(random.randint(0,100))+','+str(random.randint(0,100))+','+str(random.randint(0,100))+'\n')
    j['graph5'] = random.sample(range(100),5)


    a = random.randint(0,60)
    b = 100 -a
    j['graph2'] = [a,b]
    f.write('graph2'+','+str(a)+','+str(b)+'\n')

  return j
