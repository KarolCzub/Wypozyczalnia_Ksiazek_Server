from flask import Flask, request, jsonify, Response
import pyrebase
from json2table import convert
from flask_api import status
from time import sleep
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

config = {
	#config removed to not compromise access to firebase
}

cred = credentials.Certificate("F:/fff/fireserver-7b2e2-firebase-adminsdk-st08b-83ffc77818.json")
firebase_admin.initialize_app(cred)


firebase = pyrebase.initialize_app(config)
db = firebase.database()
	
		
while True:
	all_noti = db.child("notifications").get()
	all_not = all_noti.val()
	while type(all_not) == type(None):
		sleep(10)
		all_noti = db.child("notifications").get()
		all_not = all_noti.val()
	for noti in all_noti.each():
		topic = noti.val().get("topic")
		topic_id = noti.val().get("id")
		topic_title = noti.val().get("n_title")
		topic_message = noti.val().get("n_message")
		key = noti.key()
		topic_message = topic_message.split("|")[0]
		message = messaging.Message(
	    data={
	        'id': topic_id,
	        'n_title': topic_title + ' ' + topic_message,
	    },
	    topic= topic,
		)
		print(topic)
		response = messaging.send(message)
		print('Successfully sent message:', response)
		db.child("notifications").child(key).remove()
	