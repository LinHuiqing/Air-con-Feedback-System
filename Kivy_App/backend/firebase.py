import firebase_admin
from firebase_admin import credentials, firestore


class firebase_data:
    def __init__(self, room='1.413'):
        # Initialise your firebase and database
        cred = credentials.Certificate('backend/key.json')  # this is the security key to your firebase account
        firebase_admin.initialize_app(cred)  # this is your firebase instance
        db = firestore.client()  # this is your database instance

        self.room = room                        #self.room = room number
        self.temp = db.collection(u'temp')      #self.temp = collection for temperatures
        self.login = db.collection(u'login')    #self.login = collection for one-time passwords

    def check_pw(self, inp):
        '''
        inputs:
            - self: takes all variables defined within self
            - inp: the password entered
        outputs: None
        description:
        function checks if the password is in firebase (aka whether it is valid)
        '''
        store = self.login.document(u'otp').get().to_dict()
        key_found = False
        for key, value in store.items():
            if inp == str(value):
                key_found = True
                self.room = key
                print('Entering {}...'.format(self.room))
        if not key_found:
            raise Exception('Invalid code')

    def get_temp(self, inp):
        '''
        inputs:
            - self: takes all variables defined within self
            - inp: type of temperature to be obtained from firebase
        outputs:
            - temperatures[inp]: temp retrieved from firebase
        description:
        function retrieves the appropriate temperature from firebase
        '''
        store = self.temp.document(self.room)
        temperatures = store.collection(u'temperatures').document(u'temperatures').get().to_dict()
        return temperatures[inp]

    def get_room(self):
        '''
        inputs:
            - self: takes all variables defined within self
        outputs:
            - self.room: room number retrieved from firebase
        description:
        function returns room number previously retrieved from firebase
        '''
        return self.room

    def send_signal(self, inp):
        '''
        inputs:
            - self: takes all variables defined within self
            - inp: key which vote would be added to
        outputs: None
        description:
        function updates firebase based on feedback from users
        '''
        store = self.temp.document(self.room)
        feedback = store.collection(u'feedback').document(u'feedback')
        print('feedback:', inp)
        # use .set() method to update your firestore data. If name of document not found, it will
        # automatically create a new document.
        # inside set() need to put as a dictionary format, with keys and values
        feedback.set(
            {
                inp: feedback.get().to_dict()[inp] + 1,
            }, merge=True
        )
