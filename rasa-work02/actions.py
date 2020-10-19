
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet,Form,ReminderScheduled,ActionReverted,UserUtteranceReverted,FollowupAction,AllSlotsReset
from rasa.core.slots import Slot
import datetime
import time
from threading import Timer
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
    
class ActionInactivityScheduler(Action):
    def name(self):
        return "action_inactivity_scheduler"
    def run(self, dispatcher, tracker, domain):
        result = []
        # slot_to_fill = tracker.get_slot("requested_slot")
        # if slot_to_fill == " name1":
        #     result.append(SlotSet("name1", None))
        # else:
        #     result.append(SlotSet("user_confirm", None))
        result.append(ReminderScheduled(intent_name="EXTERNAL_second",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=10),
                                        name="second_remind",
                                        kill_on_user_message=True))
        return result
        
class RemindLast(Action):
    def name(self):
        return "action_turn_off"
    def run(self,dispatcher,tracker,domain):
        result = []
        result.append(ReminderScheduled(intent_name="EXTERNAL_last",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=10),
                                        name="last_remind",
                                        kill_on_user_message=True))
        return result

class ActionInactivitySchedulerFinal(Action):
    def name(self):
        return "action_inactivity_scheduler_final"
    def run(self, dispatcher, tracker, domain):
        return [Form(None),SlotSet("requested_slot", None)]

class AskNameForm(FormAction):

    def name(self) -> Text:
        return "ask_name_form"
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text] :
        return ["name1","user_confirm"]
    
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        )  ->List[Dict]:
        dispatcher.utter_message("cảm ơn bạn")
        return []
        
    def slot_mappings(self):
        
        return{
            "name1": [
                self.from_entity(entity="name1",intent="give_name")
             ],
            "user_confirm": [
                self.from_intent(intent="affirm",value = True),
                self.from_intent(intent="deny",value = False)
            ]
          }
    
    def validate(self, dispatcher, tracker, domain):
        result = []
        result.append(ReminderScheduled(intent_name="EXTERNAL_reminder",
                                        trigger_date_time=datetime.datetime.now()
                                        + datetime.timedelta(seconds=10),
                                        name="first_remind",
                                        kill_on_user_message=True))
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        value = tracker.latest_message.get("text")
        slot_to_fill = tracker.get_slot("requested_slot")
        if slot_to_fill: 
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        intent = tracker.latest_message.get("intent", {}).get("name")
        for slot, value in slot_values.items():
            result.append(SlotSet(slot, value))

        if slot_to_fill == "name1":
            if intent == "chitchat":
                result.append(SlotSet("name1",None))
                return result             
        if slot_to_fill == "user_confirm": 
            if intent =="affirm":
                result.append(SlotSet("user_confirm", value))
                return result
            if intent == "chitchat":
                result.append(SlotSet("user_confirm",None))
                return result
            if intent == "deny":
                dispatcher.utter_message("result la: {}".format(result))
                result[1]=SlotSet("name1",None)
                return result
            else:
                return [result]
        return result
    
        
        
            
   
