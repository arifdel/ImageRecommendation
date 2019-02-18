# @apps.route('/signIn' , methods=['POST'])
# def signIn():
#   if request.method == 'POST':
#     email = request.form['email']
#     passw = request.form['passw']
#     try:
#       user = auth.sign_in_with_email_and_password(email,passw)
#       print email
#       session_id=user['idToken']
#       request.session['uid']=str(session_id)
#       print user
#     except:
#       message = 'Invalid Credentials'
#       logger.info(message)
#   return 'Success'




import numpy
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from keras.models import model_from_json
from keras.models import load_model
import h5py
import base64
import json



# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# load dataset
dataframe = pd.read_csv("iris.csv", header=None)
dataset = dataframe.values
X = dataset[:,0:4].astype(float)
Y = dataset[:,4]
  
# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

# define baseline model
  # create model
model = Sequential()
model.add(Dense(8, input_dim=4, activation='relu'))
model.add(Dense(3, activation='softmax'))
print (model)
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# create our KerasClassifier
estimator = KerasRegressor(build_fn=model, epochs=200, batch_size=5, verbose=0)
print (estimator)

# k-Fold Cross Validation
kfold = KFold(n_splits=10, shuffle=True, random_state=seed)

results = model.fit(X, dummy_y)
# print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

model.save('my_model.h5')

model = load_model('my_model.h5')

with open("/home/arif/Downloads/FlowerImg/flower1.jpg", "rb") as imageFile:
    string = base64.b64encode(imageFile.read())
    print (string)
    obj = json.loads(string)

with h5py.File('my_model.h5', 'r') as f:
    x_data = f[obj]
    model.predict(x_data)
