from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
import pyrebase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.clock import Clock
FirebaseConfig = {
  'apiKey': "AIzaSyDcdRZkPeEFL_yczg9dLgMQeUngWTBJWqA",
  'authDomain': "irrigation-control-test.firebaseapp.com",
  'databaseURL': "https://irrigation-control-test-default-rtdb.firebaseio.com",
  'projectId': "irrigation-control-test",
  'storageBucket': "irrigation-control-test.appspot.com",
  'messagingSenderId':"968190474106",
  'appId': "1:968190474106:web:c32a2edf5e406668b3c8c3",
  'measurementId': "G-9TJEYJPCQ4"
}
from kivy.lang import Builder

class P(FloatLayout):
    btn = ObjectProperty(None)
    l1 = ObjectProperty(None)
    def btn_enable(self,*args):
        self.l1.text = "SUCESSFULLY SWITCHED ON"
    def show_message(self,*args):
        self.l1.text= "SUCESSFULLY SWITCHED OFF"
class MainPage(Screen):
    output = ObjectProperty(None)
    m_label= ObjectProperty(None)
    def GetData(self):
        firebase = pyrebase.initialize_app(FirebaseConfig)
        db = firebase.database()
        status = db.child("motor_status").get()
        print(status.val())
        if (status.val()==1):
            self.output.text = "Irrigation is ON"
        else:
            self.output.text = "Irrigation is OFF"
    def GetMoisture(self):
        firebase = pyrebase.initialize_app(FirebaseConfig)
        db = firebase.database()
        moisture = db.child("moisture content").get()
        print(moisture.val())
        str1=str(moisture.val())
        self.m_label.text="The moisture is "+str1

    def CloseProgram(self):
        App.get_running_app().stop()
        Window.close()
    pass
class SecondPage(Screen):
    def MakeHigh(self):
        firebase = pyrebase.initialize_app(FirebaseConfig)
        db = firebase.database()
        db.update({"motor_status": 1})
    def MakeLow(self):
        firebase = pyrebase.initialize_app(FirebaseConfig)
        db = firebase.database()
        db.update({"motor_status": 0})
    def popUp(self):
        show_popup(self)
    def offPop(self):
        show_offpopup(self)
class ManageScreen(ScreenManager):
    #handles transition between windows
    pass
kv = Builder.load_file("my.kv")
class MainApp(App):

    def build(self):
        Window.clearcolor = (168/255, 50/255, 88/255,1)
        self.title = "Irrigation Controller"
        return kv
def show_popup(self):
    sh = P()
    popupWindow = Popup(title="Switching Process", content=sh, size_hint=(None, None), size=(470, 400))
    popupWindow.open()
    Clock.schedule_once(sh.btn_enable,3)
def show_offpopup(self):
    sh = P()
    popupWindow = Popup(title="Switching Process", content=sh, size_hint=(None, None), size=(470, 400))
    popupWindow.open()
    Clock.schedule_once(sh.show_message, 3)
if __name__ == "__main__":
    MainApp().run()