# -*- coding: utf-8 -*-
from os.path import dirname, abspath
import sys
import requests
import json
import threading

sys.path.append(abspath(dirname(__file__)))

from adapt.intent import IntentBuilder
try:
    from mycroft.skills.core import MycroftSkill
except:
    class MycroftSkill:
        pass

import RPi.GPIO as GPIO

__author__ = 'blackgame'


class GPIO_ControlSkill(MycroftSkill):
    def on_led_change(self):
        self.speak("Led is %s" % status)

    def __init__(self):
        super(GPIO_ControlSkill, self).__init__(name="GPIO_ControlSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))

        command_intent = IntentBuilder("IoCommandIntent").require("command").require("ioobject").optionally("ioparam").build()
        system_intent = IntentBuilder("SystemQueryIntent").require("question").require("systemobject").build()

        self.register_intent(command_intent, self.handle_command_intent)
        self.register_intent(system_intent, self.handle_system_intent)

    def handle_system_intent(self, message):
        if message.data["systemobject"] == "Name":
            self.speak_dialog("name")
            self.speak(__name__)
        elif message.data["systemobject"] == "GPIO":
            self.speak_dialog("check")
            if GPIO.is_imported:
                self.speak("GPIO is Imported")
            else:
                self.speak("GPIO is not Imported")
        elif message.data["systemobject"] == "Modules":
            self.speak_dialog("modules")
            for module in sys.modules:
                self.speak(module)
        elif message.data["systemobject"] == "Path":
            self.speak_dialog("path")
            for path in sys.path:
                self.speak(path)

    def handle_command_intent(self, message):
        if message.data["command"].upper() == "BLINK":
            self.speak_dialog("ledblink")
            if self.blink_active:
                self.blink_active = False
            else:
                self.blink_active = True
                self.blink_led()
        elif message.data["command"].upper() == "STATUS":
            if message.data["ioobject"].upper() == "LED":
                self.on_led_change()
        elif message.data["command"].upper() == "TURN":
            if message.data["ioobject"].upper() == "LED":
                if "ioparam" in message.data:
                    if message.data["ioparam"].upper() == "ON":
                        status = "On"
                        GPIO.output(7,True) 
                    elif message.data["ioparam"].upper() == "OFF":
                        status = "Off"
                        GPIO.output(7,False)        
                else:
                    self.speak_dialog("ipparamrequired")

def create_skill():
    """This function is to create the skill"""
    return GPIO_ControlSkill()
