
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, Response, session
from datetime import date
from collections import ChainMap
from bson.objectid import ObjectId
import random
import json
import uuid
import time
import os

#Connect to local 
client = MongoClient('mongodb://localhost:27017/')  

#Database
db = client['DSairlines']

#Collections
users = db['Users']
flights = db['Flights']
bookings = db['Bookings']


#Flask
app = Flask(__name__)

user_session = {}   
admin_session={}              
user_bookings = []           

#############################################################################################
#All functions needed
def create_session(email , category):
    user_uuid = str(uuid.uuid1())
    if category == "admin":
        admin_session[user_uuid] = (email, time.time())
        return user_uuid 

    else:
        user_session[user_uuid] = (email, time.time())
        return user_uuid 

def is_session_valid(user_uuid):
    return user_uuid in user_session

def is_admin_session_valid(user_uuid):
    return user_uuid in admin_session



#######################################################################################################################################################################################
#Endpoints for user registration and authentication


#Signup
@app.route('/user.signup', methods=['POST'])
def signup():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "email" in data  or not "username" in data or not "firstname" in data or not "lastname" in data  or not "password" in data or not "passport" in data :
        return Response("Information incomplete",status=500,mimetype="application/json")

    #Check if email or nickname or passport exists
    er=0
    if  int(data["passport"]) >= 1000000 or int(data["passport"]) <=9999999:
        if db.users.find.one({"email": data['email'] }):
            er=1
            return Response({"Email address already in use"},status=400,mimetype="application/json"),
        
        if db.users.find.one({"username": data['username'] }):
            er=1
            return Response({"Username already in use"},status=400,mimetype="application/json"),
        
        if db.users.find.one({"passport": data['passport'] }):
            er=1
            return Response({"Passport  already in use"},status=400,mimetype="application/json"),
            
        if er==0 :
            user = {'email': data["email"], 'username': data["username"], 'firstname': data["firstname"], 'lastname': data["lastname"], 'password': data["password"], 'passport': data["passport"],'category': ["user"]}
            users.insert_one( user)
            return Response("Successful signup.",status=200,mimetype="application/json")
    else: 
        return Response("Invalid passport number.",status=400,mimetype="application/json")



#Login
@app.route('/login', methods=['POST'])
def login():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "email" in data  or not "urename" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")


    info = users.find_one( {"email" : data['email'] ,"username" : data['username'] , "password" : data['password']} )
    
    if info:
        email = data['email']
        username = data['username']
        password = info['password']
        category = info['category']
        user_uuid = create_session(email ,category)
        res = {"uuid": user_uuid, "email": data['email'], "username": data['username']}
        return Response(json.dumps(res), mimetype='application/json' , status=200)   
    else:  
       return Response("Wrong data.Please try again.",mimetype='application/json', status=400)


#Logout
@app.route('/logout', methods=['POST'])
def logout():
    
    uuid=request.headers.get("authorization")
    verify=is_session_valid(uuid)
    
    if uuid != None:
        if verify:
           del user_session[uuid]
           return Response("Successful logout.", status=200, mimetype="application/json")
        else:
            return Response("No active session. Please login.", mimetype="application/json", status=400)
    else:
        return Response("Authorization key is missing.", status=400, mimetype="application/json")




#######################################################################################################################################################################################
#Endpoints for User's Actions

#Search flight
@app.route('/searchFlight', methods=['GET'])
def searchFlight():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "from" in data  or not "to" in data and not "date" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")


    uuid=request.headers.get("authorization")
    verify=is_session_valid(uuid)

    if verify:
        if "from" and "to" and "date" in data:
            availableFlightsList = flights.find({'from':data["from"],'to':data["to"],'date':data["date"]})
            availableFlights=[]
            for flight in availableFlightsList:
                if flight["tickets_left"] > 0 :
                    flight = {'date': flight["date"], 'from': flight["from"], 'to': flight["to"],'price': flight["price"],'hours': flight["hours"],'tickets_left': flight["tickets_left"],'flightID': flight["flightID"]}
                    availableFlights.insert_one(flight)
            if  availableFlights!= []:
                return Response(json.dumps(availableFlights,indent=4)+"\n", status=200, mimetype='application/json')
            else:
                return Response("No flights found.\n")
        else:
            return Response("Please enter departure location,destination location and a date.", mimetype='application/json' , status=400)
    else: 
        return Response("No active session. Please login.", mimetype="application/json", status=400)
	

#Book a flight
@app.route('/bookFlight', methods=['POST'])
def bookFlight():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "flightID" in data or not "firstname" in data or not "lastname" in data  or not "passport" in data  or not "card" in data :
        return Response("Information incomplete",status=500,mimetype="application/json")

    uuid=request.headers.get("authorization")
    verify=is_session_valid(uuid)

    if verify:
        if  int(data["card"]) >= 1000000000000000 or int(data["card"]) <=9999999999999999:
            bookingList = flights.find({'flightID':data["flightID"],'fistname':user_session[uuid][2],'lastname':user_session[uuid][3]})

            for booking in bookingList:
                thisFlight=flights.find_one({"flightID" : ObjectId(booking['flightID'])})
                prod= int(thisFlight['tickets_left']) - 1 

                user_bookings.update_one({"email" : user_session[uuid][0]}, {'$set': {'bookings' : thisFlight}})
                flights.update_one({"flightID" : ObjectId(booking['flightID'])}, {'$set': {'tickets_left' : prod }})

                booking = {'flightID': data["flightID"],'price': thisFlight["price"],'date': thisFlight["date"],'from': thisFlight["from"],'to': thisFlight["to"],'hour': thisFlight["hour"], 'email': data["email"], 'username': data["username"], 'fistname': data["fistname"], 'lastname': data["lastname"], 'passport': data["passport"],'category': ["user]"]}
                bookings.insert_one( booking)
                
                return Response("Successful booking./n",json.dumps(booking,indent=4)+"\n", status=200, mimetype='application/json')
        else:
         return Response("Invalid card number.Try again.", mimetype="application/json", status=400)
    else: 
        return Response("No active session. Please login.", mimetype="application/json", status=400)
	

#Search booking
@app.route('/searchBooking', methods=['GET'])
def searchBooking():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "flightID" :
        return Response("Please enter flightID",status=500,mimetype="application/json")

    uuid=request.headers.get("authorization")
    verify=is_session_valid(uuid)

    if verify:
        if "flightID" in data:
            userBookingList = user_bookings.find({'flight':data["flightID"]})
            
            if  userBookingList != []:
                return Response(json.dumps(user_bookings,indent=4)+"\n", status=200, mimetype='application/json')
            
            else:
                return Response("No booking found.\n")
        else:
            return Response("Please enter flightID.", mimetype='application/json' , status=400)
    else: 
        return Response("No active session. Please login.", mimetype="application/json", status=400)
	

#Cancel booking
@app.route('/cancelBooking', methods=['GET'])
def cancelBooking():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "flightID" :
        return Response("Please enter the flightID",status=500,mimetype="application/json")

    uuid = request.headers.get('authorization')
    verify = is_session_valid(uuid)

    if uuid != None:
        if verify :
            refound=0
            for i in range(len(user_bookings)):
                if user_bookings[i]['flightID'] == data['flightID']:
                    refound=1
                    refound_price = user_bookings[i]['price']
                    refound_card = user_bookings[i]['card']

            if refound == 1:
                del user_bookings[i]
                return Response("You have successfully canceled your booking! You will be refunded the amount:'"+refound+"' to your card:'"+refound_card+"'",mimetype='application/json' , status=200)

            else:
                return Response("The flightID doesn't match with your bookings." , mimetype='application/json' , status=400)
        else:
            return Response("No active session. Please login.." , mimetype='application/json' , status=400)
    else:
        return Response ("Authorization key is missing." , status = 401)


#Show your bookings by order(asc/desc)
@app.route('/sortBookings', methods=['GET'])
def sortBookings():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "order" :
        return Response("Please enter asc or desc order",status=500,mimetype="application/json")

    uuid=request.headers.get("authorization")
    verify=is_session_valid(uuid)

    if uuid != None:
        if verify:
            if  user_bookings != []:
                if "order" == 'asc':
                    res=user_bookings.sort([("date", pymongo.ASCENDING)])
                    return Response(json.dumps(res), status=200, mimetype='application/json')
                elif "order" =='desc':
                    res=user_bookings.sort([("date", pymongo.DESCENDING)])
                    return Response(json.dumps(res), status=200, mimetype='application/json')
                else:
                    return Response("Please enter asc or desc order",status=400,mimetype="application/json")
            else:
                return Response("You have no bookings." , status=400,mimetype='application/json')
        else:
            return Response("No active session. Please login.", mimetype="application/json", status=400)
	   
    else:
       return Response("Authorization key is missing.", status=400, mimetype="application/json")


#Show your bookings by destination
@app.route('/getBookingByDestination', methods=['GET'])
def getBookingsByDestination():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "to" :
        return Response("Please enter destination",status=500,mimetype="application/json")

    uuid=request.headers.get("authorization")
    verify=is_session_valid(uuid)

    
    if verify:
        if  user_bookings != []:
            if "to" in data:
                res= user_bookings.find({'to':data["to"]})
                
                if  res!= []:
                    return Response(json.dumps(res,indent=4)+"\n", status=200, mimetype='application/json')
                else:
                    return Response("No bookings found with that destination.\n")
            else:
                return Response("Please enter destination.", mimetype='application/json' , status=400)
        else:
             return Response("No bookings found .\n")
    else:
        return Response("No active session. Please login.", mimetype="application/json", status=400)
	

#Inactivate Account
@app.route('/inactivateAccount', methods=['POST'])
def inactivateAccount():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    

    uuid=request.headers.get("authorization")
    verify=is_session_valid(uuid)
    
    if uuid != None:
        if verify:
            activateCode=random.randint(100000000000,999999999999)
            users.update_one({"email" : user_session[uuid][0]}, {'$set': {'inactivate' : True, 'activateCode' : activateCode}})
            return Response("You have successfully inactivated your account! If you want to login again use this password:'"+activateCode+"'",mimetype='application/json' , status=200)

        else:
            return Response("No active session. Please login.", mimetype="application/json", status=400)
    else:
        return Response("Authorization key is missing.", status=400, mimetype="application/json")


#Activate Account
@app.route('/inactivateAccount', methods=['POST'])
def inactivateAccount():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "email" in data  or not "urename" in data or not "password" in data or not "activateCode" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
        
    info = users.find_one( {"email" : data['email'] ,"username" : data['username'] , "password" : data['password'],"activateCode" : data['activateCode']} )
    
    if info:
        email = data['email']
        username = data['username']
        password = info['password']
        category = info['category']
        activateCode = info['activateCode']

        user_uuid = create_session(email ,category)
        res = {"uuid": user_uuid, "email": data['email'], "username": data['username']}
        return Response(json.dumps(res), mimetype='application/json' , status=200)   
    else:  
       return Response("Wrong data.Please try again.",mimetype='application/json', status=400)
    


#######################################################################################################################################################################################
#Endpoints for Admins's Actions

#Add new admin
@app.route('/addAdmin', methods=['POST'])
def addAdmin():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "email" in data  or not "firstname" in data or not "lastname" in data or not "adminCode" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    uuid=request.headers.get("authorization")
    verify= is_admin_session_valid(uuid)

    if uuid != None:
        if verify:
            if db.users.find.one({"email": data['email'] }):
                return Response({"Email address already in use"},status=400,mimetype="application/json"),
            else:
                 user = {'email': data["email"],'firstname': data["firstname"], 'lastname': data["lastname"], 'password': data["password"], 'category': ["admin"]}
                 users.insert_one( user)
                 return Response("Successfully added a admin.",status=200,mimetype="application/json")
        else: 
         return Response("No active admin session.", mimetype="application/json", status=400)   
    else:
       return Response("Authorization key is missing.", status=400, mimetype="application/json")


#Add new flight
@app.route('/addFlight', methods=['POST'])
def addFlight():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "date" in data  or not "from" in data or not "to" in data or not "price" in data or not "hours" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    uuid=request.headers.get("authorization")
    verify= is_admin_session_valid(uuid)

    if uuid != None:
        if verify:
            ####??????????########
            flightID = 'from'[0] + 'to'[0] +  'date'[0] + 'date'[1] + 'date'[2] + 'hour'[0]
            newflight = {'date': data["date"],'from': data["from"], 'to': data["to"], 'price': data["price"], 'hours': data["hours"],  'tickets_left': ["220"], 'flightID':[flightID]}
            flights.append(newflight)
            return Response("Successfully added a new flight.",status=200,mimetype="application/json")
        else: 
         return Response("No active admin session.", mimetype="application/json", status=400)   
    else:
       return Response("Authorization key is missing.",  mimetype="application/json",status=400)


#Update price of flight
@app.route('/updatePrice', methods=['POST'])
def updateFlight():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "flightID" in data  or not "newPrice" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    uuid=request.headers.get("authorization")
    verify= is_admin_session_valid(uuid)

    if uuid != None:
        if verify:
            flightsList = flights.find({'flight':data["flightID"]})
            if  flightsList != []:
                if "newPrice" > 0:
                    if flights.tickets_left == 220:
                        flights.update_one({"flightID" : data(['flightID'])}, {'$set': {'price' : data["newPrice"] }})
                        return Response("Successfully updated a flight.",status=200,mimetype="application/json")
                    else:
                         return Response("Bookings started. You can't update the price.",status=200,mimetype="application/json")
                else:
                    return Response("Invalid number price.", mimetype="application/json", status=400)  
                    
            else:  
                return Response("The flightID doesn't match with any flight.", mimetype="application/json", status=400)   
        else: 
         return Response("No active admin session.", mimetype="application/json", status=400)   
    else:
       return Response("Authorization key is missing.",  mimetype="application/json",status=400)


#Delete a flight
@app.route('/deleteFlight', methods=['POST'])
def deleteFlight():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "flightID" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    uuid=request.headers.get("authorization")
    verify= is_admin_session_valid(uuid)

    if uuid != None:
        if verify:
            flightsList = flights.find({'flightID':data["flightID"]})
            if  flightsList != []:
                flight = {'date': flight["date"], 'from': flight["from"], 'to': flight["to"],'price': flight["price"],'hours': flight["hours"],'tickets_left': flight["tickets_left"],'flightID': flight["flightID"]}
                flights.delete_one(flight)
                return Response("Successfully deleted a flight.",status=200,mimetype="application/json")
            else:  
                return Response("The flightID doesn't match with any flight.", mimetype="application/json", status=400)   
        else: 
         return Response("No active admin session.", mimetype="application/json", status=400)   
    else:
       return Response("Authorization key is missing.", mimetype="application/json", status=400)

      