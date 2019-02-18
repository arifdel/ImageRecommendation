import firebase_admin
import pyrebase	
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db
from collections import OrderedDict


cred = credentials.Certificate('/home/arif/Downloads/FoodApp-f159b8af6d71.json')
default_app = firebase_admin.initialize_app(cred , {'databaseURL': 'https://foodapp-beb00.firebaseio.com'})



UID = 'wVWdMgiq94b2VDM43cYHaDSMdGA2'

ref1 = db.reference('Consumption/wVWdMgiq94b2VDM43cYHaDSMdGA2/15 Feb, 2019/Breakfast')

fetchdict = ref1.get()
for i in fetchdict:
	UserInfo = fetchdict.get(i)
	Calorie = UserInfo.get('calorie1')
	# print Calorie 
print 'User Calorie Info : ' + Calorie

start = float(Calorie) - 0.1*float(Calorie)
end = float(Calorie) + 0.1*float(Calorie)

LowerLimit = int(start)
UpperLimit = int(end)

print 'range lower limit : ' + str(LowerLimit)
print 'range upper limit : ' + str(UpperLimit)




dbValue = []
ref = db.reference('FoodData/item')
fetchdict = ref.get()
print 'Reading database for the calorific range'
for i in fetchdict:
	FoodItem = fetchdict.get(i)
	Energy = FoodItem.get('energy')
	if Energy != 'None':
		dbValue = Energy
		print dbValue
print 'Readed all values in range successfully'
recommendlist = []
for dbValue in range(LowerLimit , UpperLimit):
	recommendlist.append(dbValue)

print str(len(recommendlist)) + ' items recommended'
ref2 = db.reference('FoodData/item')
for items in recommendlist:
	snapshot = ref2.order_by_child('energy').equal_to(float(items)).get()
	ordered_dict = OrderedDict(snapshot)
	for whtever in ordered_dict:
		snapshot1 = ordered_dict.get(whtever)
		FoodName = [snapshot1.get('shrt_Desc')]
	print FoodName


print 'Recommendation Completed successfully'