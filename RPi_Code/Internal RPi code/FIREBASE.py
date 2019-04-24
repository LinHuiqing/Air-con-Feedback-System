# Firebase class code

#========================INITIALISATION START=================================
from firebase_admin import credentials, firestore
import firebase_admin
import random

#==========================INITIALISATION END=================================

class firebase_data:
    def __init__(self, room='0'):
        # Initialise your firebase and database
        cred = credentials.Certificate('firebase_key.json')  # this is the security key to your firebase account
        firebase_admin.initialize_app(cred)
        db = firestore.client()  

        self.room = room                        # self.room = room number
        self.temp = db.collection(u'temp')      # self.temp = collection for temperatures
        self.login = db.collection(u'login')    # self.login = collection for one-time passwords
        self.OTP = 0                            # self.OTP = password to room

    def send_temperature(self, inp):
        '''
        inputs:
            - self: takes all variables defined within self
            - inp: temperature measured
        outputs: None
        description:
        function updates firebase with the temperature measured
        '''
        store = self.temp.document('1.413')
        temperatures = store.collection(u'temperatures').document(u'temperatures')
        temperatures.set(
            {
                'inside':inp
            }, merge=True
        )

    def get_temperature(self):
        '''
        inputs:
            - self: takes all variables defined within self
            - inp: type of temperature to be obtained from firebase
        outputs:
            - temperatures[inp]: temp retrieved from firebase
        description:
        function retrieves the appropriate temperature from firebase
        '''
        store = self.temp.document('1.413')
        temperature_doc = store.collection(u'temperatures').document(u'temperatures')
        feedback_doc = store.collection(u'feedback').document(u'feedback')
        temp = temperature_doc.get().to_dict()
        feedback = feedback_doc.get().to_dict()
        return temp, feedback

    # Function to reset all feedbacks after reading them every hour
    def reset_feedback(self):
        '''
        inputs:
            - self: takes all variables defined within self
        outputs: None
        description:
        function resets all feedbacks on firebase
        '''
        store = self.temp.document('1.413')
        feedback = store.collection(u'feedback').document(u'feedback')
        feedback.set(
            {
                'cold': 0,
                'hot': 0,
                'just_nice': 0
            }, merge=True
        )

    # Function to generate OTP (Password) for students to login in
    def loginotp(self):
        '''
        inputs:
            - self: takes all variables defined within self
        outputs: None
        description:
        function sets a new password and pushes it to firebase
        '''
        self.OTP = random.randrange(10000000, 20000000)
        storage = self.login.document('otp')
        storage.set(
            {
                '1.413': self.OTP
            }, merge=True
        )
