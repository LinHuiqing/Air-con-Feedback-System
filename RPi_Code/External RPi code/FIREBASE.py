#=============================INITIALISATION START================================
import firebase_admin
from firebase_admin import credentials, firestore

#=============================INITIALISATION END================================

#==============================FIREBASE CLASS===================================
class firebase_data:
    def __init__(self, room='0'):
        # Initialization.
        # include in same folder, file 'firebase_key.json' - file created on Firebase
        cred = credentials.Certificate('firebase_key.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        self.room = room                            # self.room = room number
        self.temp = db.collection(u'temp')          # self.temp = collection for temperatures
        self.login = db.collection(u'login')        # self.login = collection for one time passwords

    # Function to send data to firebase
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
                'outside': inp
                }, merge=True
            )
