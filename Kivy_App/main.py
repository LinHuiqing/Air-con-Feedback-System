# import packages

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock

from backend.firebase import firebase_data  # import package with backend code (link to firebase)


class loginScreen(Screen):  # login screen
    def __init__(self, **kwargs):  # screen layout and initialisation
        Screen.__init__(self, **kwargs)

        layout = BoxLayout(padding=40, spacing=50, orientation='vertical')  # layout = container containing whole page
        logo = Image(source='images/LOGO.png')  # logo = logo of product
        # textbox = textbox to key in otp
        self.input_widget = textbox = TextInput(hint_text='Enter OTP', size_hint=(1, 0.4))
        self.warn_widget = warning = Label(size_hint=(1, 0.5))  # warning = label to notify user if password is invalid

        layout.add_widget(logo)
        layout.add_widget(textbox)
        layout.add_widget(warning)
        self.add_widget(layout)

        nextPage = Button(text='NEXT', size_hint=(None, None), pos_hint={'right': 1}, size=(150, 60),
                          on_press=self.check_pw)  # nextPage = button to enter password and move to next page
        self.add_widget(nextPage)

    # definition of functions
    def check_pw(self, instance):
        '''
        inputs:
            - self: takes all variables defined within self
        outputs:
            - None
        description:
        function checks password entered,
            - if password is valid:
                - set appropriate room
                - clear blank and notif (if any)
                - move on to screen with temperatures
            - else:
                - notify user of invalid code
                - clear input box
        '''
        try:  #try if input is valid
            firebase_data.check_pw(data, self.input_widget.text)  # check input through firebase
            self.warn_widget.text = ''  # reset invalid notif (if any)
            self.input_widget.text = ''  # reset text input
            self.manager.transition.direction = 'left'
            self.manager.current = 'temp'
        except Exception:  # if not valid, error is raised. Following code is run.
            self.warn_widget.text = 'Please key in a valid code.'  # invalid notif for user
            self.input_widget.text = ''
            print('Please key in a valid code.')


class tempScreen(Screen):  #screen to display temperatures
    def __init__(self, **kwargs):  # screen layout and initialisation
        Screen.__init__(self, **kwargs)

        layout = BoxLayout(orientation='horizontal')  # layout = container containing whole page
        # temps = label to indicate room and temperatures
        self.label_widget = temps = Label(font_size=20, halign='center', valign='center', size=self.size,
                                          text='Loading...')
        layout.add_widget(temps)
        self.add_widget(layout)

        nextPage = Button(text='NEXT', size_hint=(None, None), pos_hint={'right': 1}, size=(150, 60),
                          on_press=self.change_to_feedback)  # nextPage = button to move to next page
        backPage = Button(text='BACK', size_hint=(None, None), pos_hint={'left': 1}, size=(150, 60),
                          on_press=self.change_to_login)  # backPage = button to go to previous page
        self.add_widget(nextPage)
        self.add_widget(backPage)

    def on_enter(self, *args):
        '''
        inputs:
            - self: takes all variables defined within self
        outputs: None
        description:
        function sets label text indicating the room and temperatures upon entering the screen,
        and calls it again every 3s
        '''
        self.get_temp(0)
        Clock.schedule_interval(self.get_temp, 3)  # calls self.get_temp function every 2 second

    def on_leave(self, *args):
        '''
        inputs:
            - self: takes all variables defined within self
        outputs: None
        description:
        function stops Clock from calling get_temp every 3s
        '''
        Clock.unschedule(self.get_temp)

    def get_temp(self, dt):
        # print(value)
        self.label_widget.text = "Room: {}\n\nROOM TEMPERATURE: {}\nOUTSIDE TEMPERATURE: {} \nAIRCON TEMPERATURE: {}" \
            .format(firebase_data.get_room(data),
                    firebase_data.get_temp(data, 'inside'), firebase_data.get_temp(data, 'outside'),
                    firebase_data.get_temp(data, 'aircon'))  # display temp on label

    def change_to_login(self, value):
        '''
        inputs:
            - self: takes all variables defined within self
        outputs: None
        description:
        function changes screen to login screen
        '''
        self.manager.transition.direction = 'right'
        self.manager.current = 'login'

    def change_to_feedback(self, value):
        '''
        inputs:
            - self: takes all variables defined within self
        outputs: None
        description:
        function changes screen to feedback screen
        '''
        self.manager.transition.direction = 'left'
        self.manager.current = 'feedback'


class feedbackScreen(Screen):  # screen to collect feedback
    def __init__(self, **kwargs):  # screen layout and initailisation
        Screen.__init__(self, **kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        home = Button(text='HOME', size_hint=(None, None), pos_hint={'top': 1}, size=(90, 50),
                      on_press=self.go_home)  # home = button to go back to login page
        self.add_widget(home)

        prompt = Label(font_size=20, text="How's the temperature today?")  # prompt = label to prompt user for feedback
        layout.add_widget(prompt)

        # hot = button to feedback that it is too hot
        hot = Button(font_size=(self.height+self.width/6)/8, background_normal="images/HOT.jpg")
        hot.bind(on_press=lambda x: self.send_signal_to_firebase('hot'))
        # nice = button to feedback that it is just nice
        nice = Button(font_size=(self.height+self.width/6)/8, background_normal="images/justnice.jpg")
        nice.bind(on_press=lambda x: self.send_signal_to_firebase('just_nice'))
        # cold = button to feedback that it is too cold
        cold = Button(font_size=(self.height+self.width/6)/8, background_normal="images/COLD.jpg")
        cold.bind(on_press=lambda x: self.send_signal_to_firebase('cold'))
        layout.add_widget(hot)
        layout.add_widget(nice)
        layout.add_widget(cold)

        self.add_widget(layout)


    def send_signal_to_firebase(self, inp):
        '''
        inputs:
            - self: takes all variables defined within self
            - inp: key which 'vote' from the user is added to
        outputs: None
        description:
        function sends feedback votes to firebase
        '''
        self.manager.transition.direction = 'left'
        self.manager.current = 'thanks'
        return firebase_data.send_signal(data, inp)

    def go_home(self, value):
        '''
        inputs:
            - self: takes all variables defined within self
        outputs: None
        description:
        function changes screen to 'home' (login screen)
        '''
        self.manager.transition.direction = 'right'
        self.manager.current = 'login'

class thanksScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)

        layout = BoxLayout(orientation='vertical')

        home = Button(text='HOME', size_hint=(None, None), pos_hint={'top': 1}, size=(90, 50),
                      on_press=self.go_home)  # home = button to go back to login page
        self.add_widget(home)
        # thanknote = label to thank user for input
        thanknote = Label(font_size=20, text='Thank you for your feedback!', size=self.size, text_size=self.size)
        layout.add_widget(thanknote)
        self.add_widget(layout)

    def go_home(self, value):
        '''
        inputs:
            - self: takes all variables defined within self
        outputs: None
        description:
        function changes screen to 'home' (login screen)
        '''
        self.manager.transition.direction = 'right'
        self.manager.current = 'login'


class mainApp(App):
    def build(self):
        '''
        inputs:
            - self: takes all variables defined within self (App)
        outputs:
            - sm: screenmanager
        description:
        function builds application, using screen manager and screens
        '''
        sm = ScreenManager()

        sm.bind(size=self._update_rect, pos=self._update_rect)
        with sm.canvas.before:
            self.rect = Rectangle(source='images/hotcold.jpg', size=sm.size,
                                  pos=sm.pos)

        ls = loginScreen(name='login')
        ts = tempScreen(name='temp')
        fs = feedbackScreen(name='feedback')
        ths = thanksScreen(name='thanks')
        sm.add_widget(ls)
        sm.add_widget(ts)
        sm.add_widget(fs)
        sm.add_widget(ths)
        sm.current = 'login'

        return sm

    def _update_rect(self, instance, value):
        '''
        inputs:
            - self: takes all variables defined within self
            - instance: object where the function is called, in this case, the screen manager
        outputs: None
        description:
        function makes rectangle cover the whole screen
        '''
        self.rect.pos = instance.pos
        self.rect.size = instance.size


data = firebase_data()
feedbackApp = mainApp()
feedbackApp.run()
