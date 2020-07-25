import pyrebase



firebaseConfig = {
    "apiKey": "AIzaSyBKgvQ9Lvp-Q4KqN1kzUfMK7bvulCxf4Zc",
    "authDomain": "babydocs.firebaseapp.com",
    "databaseURL": "https://babydocs.firebaseio.com",
    "projectId": "babydocs",
    "storageBucket": "babydocs.appspot.com",
    "messagingSenderId": "310654851506",
    "appId": "1:310654851506:web:849daa929f8ca8745d6cab",
    "measurementId": "G-JG656E9G3M"
  }


 firebase = pyrebase.initialize_app(firebaseConfig)

 auth = firebase.auth()
