#playing around with firebase

#sets up the connection to the database

from firebase import firebase
firebase = firebase.FirebaseApplication('https://cookietest-a4f79.firebaseio.com', None)

print("Here's the first value from your database")

temperature = 42
humidity = 41


#Patches on extra data without making a random number identifier
result = firebase.patch('/sensor/dht/', {'First_Vals': 5, 'Sec_Vals': 6})

#Patches on extra data without making a random number identifier
result = firebase.patch('/sensor/dht2/', {'First_Vals': 4, 'Sec_Vals': 2})


#reads the database
result = firebase.get('/dht', None)
print(result)



"""
#reads the database at /dht/humidity to get that value
result = firebase.get('/dht/humidity', None)
print(result)

#deletes code from the database
firebase.delete('/datas', None)
print("Right, that's deleted. Lets run the read database code again and see if it's gone")

#write to the database (PUT MEANS UPDATE)
firebase.put("/dht", "/humidity", "0.00")
firebase.put("/dht", "/humidity", "1.00")

#POSTS  to the database (POST means create)
data = {"temp": temperature, "humidity": humidity}
firebase.post('/dht', data)
"""

