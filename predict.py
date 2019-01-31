from flask import Flask, request , json
from flask_restful import Resource, Api

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import logging


import pyrebase

logger = logging.getLogger(__name__)

config = {
    "apiKey": "AIzaSyC8NZSJ-PTtz6KcGyMC8ifUtK2Pkp13FWE",
    "authDomain": "food-recognition-1159f.firebaseapp.com",
    "databaseURL": "https://food-recognition-1159f.firebaseio.com",
    "projectId": "food-recognition-1159f",
    "storageBucket": "food-recognition-1159f.appspot.com",
    "messagingSenderId": "257470759667"
    }

firebase = pyrebase.initialize_app(config)

auth=firebase.auth()
db=firebase.database()
storage=firebase.storage()


apps = Flask(__name__)
api = Api(apps)

app = ClarifaiApp(api_key='8d0acbf6536d4cd1bfca14e99b3aa8ca')

@apps.route('/', methods=['GET'])
def get_info():
	if request.method == 'GET':
		model = app.models.get('food-items-v1.0')
		image = ClImage(url='https://i2.wp.com/learningindia.in/wp-content/uploads/2015/06/Ordering.jpg?w=640&ssl=1')
		data = model.predict([image])

		response = apps.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    	)
    	return response

@apps.route('/imageurl' , methods=['POST'])
def image_url():
  	if request.method == 'POST':
  		url = request.form['url']
  		print url
  		model = app.models.get('food-items-v1.0')
  		image = ClImage(url='%s' % (url))
  		data = model.predict([image])

		response = apps.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    	)
    	return response

@apps.route('/predict' , methods=['POST'])
def predict_url():
  if request.method == 'POST':
    upload = request.files['upload']
    imgpath = "/home/arif/Downloads/Food_Images/"+upload.filename
    print imgpath
    logger.info(imgpath)
    model = app.models.get('food-items-v1.0')
    data = model.predict_by_filename(filename=imgpath)

    response = apps.response_class(
      response=json.dumps(data),
      status=200,
      mimetype='application/json'
      )
    return response    


if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)
    apps.run(debug=True)