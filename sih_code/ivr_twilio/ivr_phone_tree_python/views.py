from flask import (
    flash,
    render_template,
    redirect,
    request,
    session,
    url_for,
    jsonify,
)
from twilio.twiml.voice_response import VoiceResponse

from ivr_phone_tree_python import app, socketio
from ivr_phone_tree_python.view_helpers import twiml


from flask_socketio import send, emit, SocketIO

import threading

# socketio = SocketIO(beforeapp)


callcounter = 6

callerNumber = ''
sympUpdateSet = set()
diseaseUpdate = -1
universal_symptoms = {'0': 'high fever',
                      '1': 'profuse sweating',
                      '2': 'headache',
                      '3': 'nausea',
                      '4': 'vomiting'
                      }







languagePreference = 'h' 
# h or e

voice = 'Polly.Aditi'
language = 'hi-IN'



@app.route('/')
@app.route('/ivr')
def home():
    return render_template('index.html')



@app.route('/ivr/newelcome', methods=['POST'])
def newelcome():
  global callcounter 
  global callerNumber
  global language

  callerNumber = request.form['From'].replace('+91','')
  # callerNumber = str(callerNumber.encode('utf8')).strip()
  print 'Caller = ', callerNumber
  callcounter += 1

  response = VoiceResponse()
  with response.gather(
      num_digits=1, action=url_for('welcome'), method="POST"
    ) as g:
        g.say(message=", , , For English, press 1", voice='alice', language='en-GB')
        g.say(message=", , , Hindi ke liye 2 dabayein, ,", voice='Polly.Aditi', language="hi-IN")

  return twiml(response)


@app.route('/ivr/welcome', methods=['POST'])
def welcome():
  global language

  selected_option = request.form['Digits']
  option_actions = {'1': _setEnglish,
                    '2': _setHindi}

  option_actions[selected_option]()


  response = VoiceResponse()
  with response.gather(
      num_digits=1, action=url_for('menu'), method="POST"
  ) as g:
      if language == 'h' :
        g.say(message="I O Hackers Helpline ko call karne ke liye dhanyawad, , ,  "+     
            "lakshan dene ke liye kripya 1 dabayein , ," +
            "rog ki jaankari praapt karne ke liye 2 dabayein , ,"+
            "nikatatam nagarpaalika pratinidhi se sampark karne ke liye 3 dabayein , ,",voice="Polly.Aditi", language="hi-IN",loop=3)
      else :
        g.say(message="Thanks for Calling I O Hacker Helpline , , , " +
              "Please Press 1 to get symptom wise information , ," +
              "Press 2 to get disease information , , "+
              "Press 3 to dial nearest Municipal representative , ,", voice='alice',language='',loop=3)

  return twiml(response)

def _setEnglish():
  global language
  language = 'e'

def _setHindi():
  global language
  language = 'h'



@app.route('/ivr/menu', methods=['POST'])
def menu():
    sympUpdateSet.clear()
    diseaseUpdate = -1

    selected_option = request.form['Digits']
    option_actions = {'1': _give_symp,
                      '2': _list_disease,
                      '3': _callmcd,
                      '9': _redirect_welcome,
                      '0' : _disconnect}

    if option_actions.has_key(selected_option):
      if selected_option == '3' :
        response = VoiceResponse()
        _callmcd()
        return _disconnect(response, "for Municipal Contact")
      
      else:
        response = VoiceResponse()
        option_actions[selected_option](response)
        return twiml(response)

    return _redirect_welcome()


# @app.route('/ivr/planets', methods=['POST'])
# def planets():
#     selected_option = request.form['Digits']
#     option_actions = {'2': "+12024173378",
#                       '3': "+12027336386",
#                       "4": "+12027336637"}

#     if selected_option in option_actions:
#         response = VoiceResponse()
#         response.dial(option_actions[selected_option])
#         return twiml(response)

#     return _redirect_welcome()



@app.route('/ivr/symplist', methods=['POST'])
def symplist():
  selected_option = request.form['Digits']

  response = VoiceResponse()

  if selected_option == '6' :
    # send_sms()

    analyzeAndSendSms(sympUpdateSet)

    print 'All selected symptoms:', sympUpdateSet
    # clear not req. but for safety.
    sympUpdateSet.clear()
    return _disconnect(response)

  sympUpdateSet.add(selected_option)
  
  if language == 'h' :
    response.say("ab aur lakshan chunen. , , ,",voice="Polly.Aditi", language="hi-IN")
  else : 
    response.say("Now select more symptioms.", voice='alice', language='en-GB')
  
  return _give_symp(response)

  # return twiml(response)

# Coughing up blood. (T)
# Chest pain, or pain with breathing or coughing. (T)
# high fever. (D&M)
# profuse sweating.(D&M)
# headache.(D&M)




diseasesympmatrix = {'1':['3'],
                      '2': ['3'],
                      '3':['1','2'],
                      '4':['2'],
                      '5':['1'],
                      }


diseasesympmatrixEnglish = {'1':'Coughing up blood',
                      '2': 'Chest pain or coughing',
                      '3':'High fever',
                      '4':'Profuse sweating',
                      '5':'Headache',
                      }
from collections import Counter


def analyzeAndSendSms(myset):
  symtext = 'For the symptoms '
  for i,k in enumerate(myset) :
    symtext+= '\n '+str(i)+' '+k





  # responsemessage = {'1':'''\nPrediction : Malaria. Please take following precautions: 
  #             1) Take antimalarial drugs (Chemoprophylaxis) when appropriate, to prevent infection from developing into clinical disease.
  #             2) Immediately seek Diagnosis and treatment if a fever develops 1 week or more after entering an area where there is a malaria risk and up to 3 months (or, rarely, later) after departure from a risk area.
  #             Visit I/O Hackers<url> to locate nearest hospitals and dispensaries. Stay Healthy! Stay Tuned!
  #             '''}

  # responsemessage = {'2':'''\nPrediction : Dengue. Please take following precautions: 
  #                         1) Take antimalarial drugs (Chemoprophylaxis) when appropriate, to prevent infection from developing into clinical disease.
  #                         2) Immediately seek Diagnosis and treatment if a fever develops 1 week or more after entering an area where there is a malaria risk and up to 3 months (or, rarely, later) after departure from a risk area.
  #                         Visit I/O Hackers<url> to locate nearest hospitals and dispensaries. Stay Healthy! Stay Tuned!
  #                         '''}

  # responsemessage = {'3':'''\nPrediction : Tuberculosis. Please take following precautions: 
  #                         Please take the following precautions: 
  #                         1) Spend as much time as possible outdoors
  #                         2) If possible, sleep alone in a separate, adequately ventilated room
  #                         3) Spend as little time as possible on public transport
  #                         Visit I/O Hackers<url> to locate nearest hospitals and dispensaries. Stay Healthy! Stay Tuned!
  #                         '''}
  responsemessage = {}
  responsemessage['1'] = "Prediction Malaria. Take antimalarial drugs. Seek Diagnosis Immediately if fever for more than a week. I/O Hackers."
  responsemessage['2'] = "Prediction Dengue. Take AntiDengue Drugs. Seek Diagnosis Immediately. I/O Hackers."
  responsemessage['3'] = "Prediction Tuberculosis. Spend time outside. Sleep seperately. Do not use piblic transport. I/O Hackers."
  
  global diseasesympmatrix


  allList = []

  for x in myset:
    allList.extend(diseasesympmatrix[x])

  ft = Counter(allList).keys() # equals to list(set(words))
  t = Counter(allList).values() 
  disease = ft[t.index(max(t))]


  # symtext+responsemessage[disease]

  sendSMS(responsemessage[disease])
  # socketio.emit('android',{'message':symtext+responsemessage[disease], 'contact':callerNumber},broadcast=True)


@app.route('/ivr/hits')
def hits():
  return jsonify(
        count=24
    )



@app.route('/ivr/diseaselist', methods=['POST'])
def diseaselist():
  selected_option = request.form['Digits']
  option_actions = {'1': "_disease_msg",
                    '2': "_disease_msg",
                    "3": "_disease_msg",
                    "4": "_redirect_welcome"}

  if option_actions.has_key(selected_option):
    if selected_option == "4" :
      return _redirect_welcome()


    response = VoiceResponse()
    return _disease_msg(response,selected_option)
    # return twiml(response)

  return _incorrect_select()


def _disease_msg(response,msg):
  textopdict = {    '1': "Malaria",
                    '2': "Dengue",
                    "3": "Tuberculosis"}   
  diseaselist = msg

  msg =  str(msg.encode('utf8'))
  print type(msg)

  responsemessage = {}
  # responsemessage['1'] = ['''Malaria. Please take following precautions: 1) Take antimalarial drugs (Chemoprophylaxis) when appropriate, to prevent infection from developing into clinical disease.''',
  #                       '''2) Immediately seek Diagnosis and treatment if a fever develops 1 week or more after entering an area where there is a malaria risk and up to 3 months (or, rarely, later) after departure from a risk area.''',
  #                        '''Visit I/O Hackers<url> to locate nearest hospitals and dispensaries. Stay Healthy! Stay Tuned!''']

  # responsemessage['2'] = '''Dengue. Please take following precautions: 
  #                         1) Take antimalarial drugs (Chemoprophylaxis) when appropriate, to prevent infection from developing into clinical disease.
  #                         2) Immediately seek Diagnosis and treatment if a fever develops 1 week or more after entering an area where there is a malaria risk and up to 3 months (or, rarely, later) after departure from a risk area.
  #                         Visit I/O Hackers<url> to locate nearest hospitals and dispensaries. Stay Healthy! Stay Tuned!
  #                         '''

  # responsemessage['3'] = '''Tuberculosis. Please take following precautions: Please take the following precautions: 
  #                         1) Spend as much time as possible outdoors
  #                         2) If possible, sleep alone in a separate, adequately ventilated room
  #                         3) Spend as little time as possible on public transport
  #                         Visit I/O Hackers<url> to locate nearest hospitals and dispensaries. Stay Healthy! Stay Tuned!
  #                         '''


  responsemessage['1'] = "Malaria. Take antimalarial drugs. Seek Diagnosis Immediately if fever for more than a week. I/O Hackers."
  responsemessage['2'] = "Dengue. Take AntiDengue Drugs. Seek Diagnosis Immediately. I/O Hackers."
  responsemessage['3'] = "Tuberculosis. Spend time outside. Sleep seperately. Do not use piblic transport. I/O Hackers."
  # send SMS here
  # t1 = threading.Thread(target=sendSMSList, args=(responsemessage[msg]))
  # t1.start()

  # t1.join()

  sendSMS(responsemessage[msg])

  # socketio.emit('android',{'message':responsemessage[msg], 'contact':callerNumber},broadcast=True)


  print 'Selected Disease is :',textopdict[msg]
  return _disconnect(response,op=textopdict[msg])


def _incorrect_select(response):
  global language

  if language == 'h':
    response.say("galat vikalp chuna gaya , , ,",voice="Polly.Aditi", language="hi-IN")
  else:
    response.say("Incorrect Option Selected", voice='alice', language='en-GB')

  return _redirect_welcome()


def _disconnect(response,op=""):
  global language

  if language == 'h' :
    response.say("aap jald hee aavashyak jaanakaaree"+op+" SMS se praapt karenge , , , , " +
               "i o haikars helpline par sampark karane ke liye dhanyavaad ",voice="Polly.Aditi", language="hi-IN")
  else :
    response.say("You will soon receive the required information "+ op +" via SMS " +
               "Thank you for calling I O Hackers Helpline ",voice="alice", language="en-GB")


  response.hangup()
  return twiml(response)


def _list_disease(response):

  global language


  with response.gather(
      numDigits=1, action=url_for('diseaselist'), method="POST"
  ) as g:
      if language == 'h':
        g.say("Malaria report karne ke liye, 1 dabayein. , , ,"+
              "Dengue report karne ke liye, 2 dabayein. , , ,"+
              "Tuberculosis report karne ke liye, 3 dabayein. , , ,"
              "Main menyoo par jane ke liye 4 dabayein. , , ,"
              
              ,voice="Polly.Aditi", language="hi-IN", loop=3)
      else :
        g.say("To report Malaria, press 1."+
            "To report Dengue, press 2."+
            "To report Tuberculosis, press 3."
            "Press 4 to go the main menu."
            ,
            voice="alice", language="en-GB", loop=3)

  return twiml(response)



# Coughing up blood. (T)
# Chest pain, or pain with breathing or coughing. (T)
# high fever. (D&M)
# profuse sweating.(D&M)
# headache.(D&M)

def _give_symp(response):
  global language

  with response.gather(
      numDigits=1, action=url_for('symplist'), method="POST"
  ) as g:
      if language == "h" :
        g.say(", , khoon ki khaansi honee par 1 dabayein. , , ,"+
            "seene mein dard aur saans lene mein takleef honee par 2 dabayein. , , ,"+
            "tez bukhaar honee par 3 dabayein. , , ,"+
            "yadi adhik paseena aa raha hai, to 4 dabayein. , , ,"+
            "yadi sir dard ho to 5 dabayein. , , "+
            "rog ke jankari lene ke liye 6 dabayein. , , ,",
            voice="Polly.Aditi", language="hi-IN", loop=3)
      else : 
        g.say("For cough and blood, , press 1. , , ,"+
            "For chest pain, , press 2. , , ,"+
            "For high fever, , press 3. , , ,"
            "For profuse sweating, ,press 4. , , ,"+
            "For headache, press 5. , , ,"+
            "To Save and Exit, press 6. , , ,",
            voice="alice", language="en-GB", loop=3)

  return twiml(response)


def _callmcd():
  contact = "+918130156596"

  symtext = "Archit Goyal, nagar palika ke pratinidhi ki jaankari "+contact
  sendSMS(symtext,contact)
  # socketio.emit('android',{'message':symtext, 'contact':callerNumber},broadcast=True)
  # response = VoiceResponse()
  # response.dial(contact)
  # return twiml(response)



def _redirect_welcome():
  global language
  
  response = VoiceResponse()
  if language == 'h' :
    response.say("main menyoo par vaapas laut rahe hai", voice="Polly.Aditi", language="hi-IN")
  else :
    response.say("Returning to the main menu", voice="alice", language="en-GB")

  response.redirect(url_for('welcome'))

  return twiml(response)



def sendSMS(text,caller=''):
  global callerNumber

  con = callerNumber
  if caller != '' :
    con = caller
  socketio.emit('android',{'message':text, 'contact':con},broadcast=True)
  print 'Sent SMS to:',con


import time

def sendSMSList(p1,p2,p3):
  sendSMS(p1)
  time.sleep(4)
  sendSMS(p2)
  time.sleep(4)
  sendSMS(p3)

















# SMS Server Files.


@app.route('/androidab/<text>')
def send_to_android(text):
    # add actual contact & text
    socketio.emit('android',{'message':'toAndroid '+text, 'contact':'8448662434'},broadcast=True)
    return 'done'


@socketio.on("obtain msg")
def handle_incoming_msg(msg):
    print 'received :',msg


@app.route('/android',methods = ['POST'])
def android_page():
    if request.method == 'POST':
        con = request.form['CONTACT']
        tex = request.form['TEXT']


        con = str(con.encode('utf8'))

        print type(con)
        print con



        print con,tex
        socketio.emit('android',{'message':tex, 'contact':con},broadcast=True)

        return  jsonify(success=True)
        
    else :
        return 'Send a POST req'


# NOTIFICATION TO ARCHIT

@app.route('/notif',methods = ['POST'])
def notif_page():
    if request.method == 'POST':
        con = request.form['CONTACT']
        tex = request.form['TEXT']

        con = str(con.encode('utf8'))

        print con,tex
        socketio.emit('notif',{'message':tex, 'contact':con},broadcast=True)

        return  jsonify(success=True)
        
    else :
        return 'Send a POST req'




from populate import callState

j1 = callState('up')
j2 = callState('delhi')
j3 = callState('tn')


# To Sagar on Request
@app.route('/web/up')
def up():

  resp = jsonify(j1)
  resp.headers.add('Access-Control-Allow-Origin','*')
  return resp

@app.route('/web/delhi')
def delhi():
  resp = jsonify(j2)
  resp.headers.add('Access-Control-Allow-Origin','*')
  return resp

@app.route('/web/tn')
def tn():
  resp = jsonify(j3)
  resp.headers.add('Access-Control-Allow-Origin','*')
  return resp

@app.route('/web/createup')
def createup():
  global j1
  j1 = callState('up')
  resp = jsonify(j1)
  resp.headers.add('Access-Control-Allow-Origin','*')
  return resp

@app.route('/web/createdelhi')
def createdelhi():
  global j2
  j2 = callState('delhi')
  resp = jsonify(j2)
  resp.headers.add('Access-Control-Allow-Origin','*')
  return resp


@app.route('/web/createtn')
def createtn():
  global j3
  j3 = callState('tn')
  resp = jsonify(j3)
  resp.headers.add('Access-Control-Allow-Origin','*')
  return resp






