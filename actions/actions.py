# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from rasa_sdk.forms import FormValidationAction
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests 
import json
import ast
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def convert_format_a_to_b(data_a):
    data_b = {
        "payload": "cardsCarousel",
        "data": []
    }

    for item in data_a["data"][0]["val"]:
        card = {
            "image": item.get("image_url", ""),
            "title": item.get("title", ""),
            "subtitle": item.get("subtitle", ""),
            "buttons": [
                {
                    "title": "Happy",
                    "payload": "Happy",
                    "type": "postback"
                },
                {
                    "title": "Sad",
                    "payload": "Sad",
                    "type": "postback"
                }
            ]
        }
        data_b["data"].append(card)

    return data_b

# def convert_format_it(data_a):
#     data_b = {
#         "payload": "cardsCarousel",
#         "data": []
#     }

#     for item in data_a["data"][0]["val"]:
#         card = {
#             "image": item.get("image_url", ""),
#             "title": item.get("title", ""),
#             "subtitle": item.get("itinerary", ""),  # assuming there's a description key in your data
#             "buttons": [
#                 {
#                     "title": "Modify",               # added Modify as an option for the itinerary
#                     "payload": "Modify itinerary",
#                     "type": "postback"
#                 },
#                 {
#                     "title": "Confirm",             # added Confirm as another option
#                     "payload": "Confirm itinerary",
#                     "type": "postback"
#                 }
#             ]
#         }
#         data_b["data"].append(card)

#     return data_b


# class ValidateDaysAndBudgetForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_days_and_budget_form"

#     async def required_slots(
#         self,
#         slots_mapped_in_domain: Dict[Text, Any],
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]
#     ) -> List[Text]:
#         # Check for required slots and send custom messages if necessary
#         required_slots = []

#         if not tracker.get_slot("DATE"):
#             required_slots.append("DATE")
#             dispatcher.utter_message(text="Please provide the date for your plan.")
        
#         if not tracker.get_slot("MONEY"):
#             required_slots.append("MONEY")
#             dispatcher.utter_message(text="Please specify your budget.")

#         return required_slots

#     async def validate_DATE(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         # You can add further validation here if necessary
#         return {"DATE": slot_value}

#     async def validate_MONEY(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         # You can add further validation here if necessary
#         return {"MONEY": slot_value}

class ValidateDaysAndBudgetForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_days_and_budget_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: Dict[Text, Any],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Text]:
        # Define all required slots
        required_slots = ["DATE", "MONEY"]
        
        # Check which slots are filled and remove them from the required list
        for slot_name in required_slots:
            if tracker.get_slot(slot_name):
                required_slots.remove(slot_name)

        # Instead of sending the message here, let Rasa handle it based on the stories and responses.
        return required_slots

    async def validate_DATE(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        # You can add further validation here if necessary
        return {"DATE": slot_value}

    async def validate_MONEY(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        # You can add further validation here if necessary
        return {"MONEY": slot_value}
        
# class ValidateDaysAndBudget(Action):
#     def name(self) -> str:
#         return "validate_days_and_budget"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> List[Dict[Text, Any]]:
#         days = tracker.get_slot("DATE")
#         budget = tracker.get_slot("MONEY")

        # if days and budget:
        #     # If both are filled
        #     dispatcher.utter_message(text=f"You've provided {days} days and a budget of {budget}.")
        #     return []
#         elif days and not budget:
#             # If only days is filled
#             dispatcher.utter_message(text=f"You've provided {days} days. What is your budget?")
#             return [SlotSet("MONEY", None)]
#         elif budget and not days:
#             # If only budget is filled
#             dispatcher.utter_message(text=f"You've mentioned a budget of {budget}. How many days is your journey?")
#             return [SlotSet("DATE", None)]
#         else:
#             # If none are filled
#             dispatcher.utter_message(text="Let me know the number of days you'll be visiting and your budget.")
#             return [SlotSet("DATE", None), SlotSet("MONEY", None)]

class ActionLangchainPayload(Action):

    def name(self) -> str:
        return "action_langchain_payload"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        date_value = tracker.get_slot("DATE")
        # Get session ID (sender_id) from tracker
        session_id = tracker.sender_id
        
        payload = {
            "num_days": date_value,
            "num_adults": 3,
            "num_boys": 2,
            "num_girls": 2,  
            "user_query": "query",
            "hashkey": 123
        }

        # start_time = datetime.now()
        res = requests.post(url = 'http://18.117.181.137:3890/disney/get_itinerary', data = json.dumps(payload))
        # return res.json()
        # end_time = datetime.now()
        # response_time = (end_time - start_time).total_seconds()
        dispatcher.utter_message(text=str(res.json()))
        # logger.info(f"API Response Time: {response_time} seconds")

        return []
        

# class ActionShowItinerary(Action):

#     def name(self) -> str:
#         return "action_show_itinerary"

#     def run(self, dispatcher: CollectingDispatcher, tracker, domain):
#         date_value = tracker.get_slot("DATE")
#         session_id = tracker.sender_id
        
#         payload = {
#             "num_days": "{date_value}",
#             "num_adults": 3,
#             "num_boys": 2,
#             "num_girls": 2,  
#             "user_query": "query",
#             "hashkey": "{session_id}"
#         }
        
#         res = requests.post(url='http://18.117.181.137:3890/disney/get_itinerary', data=json.dumps(payload))
#         api_response = res.json()

#         carousel_data = convert_format_it(api_response)
        
#         dispatcher.utter_message(json_message=carousel_data)
#         return []

class ActionSaveUserQuestion(Action):

    def name(self) -> str:
        return "action_save_user_question"

    def run(self, dispatcher, tracker, domain):
        # Get the last user message
        user_query = tracker.latest_message.get('text')

        # Set the user_message slot with the value
        return [SlotSet("user_query", user_query)]


class ActionHandleInquiry(Action):
    def name(self):
        return "action_handle_inquiry"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain):

        # Get slot values from the form
        query_value = tracker.get_slot('user_query')
        # Get session ID (sender_id) from tracker
        session_id = tracker.sender_id

        payload = {
            "followup_question": query_value,
            "query": "",
            "budget": "",
            "hashkey": session_id,
            "is_followup": "no"
        }

        # dispatcher.utter_message(text=f"{payload}")
        # start_time = datetime.now()
        res = requests.post(url = 'http://18.117.181.137:3890/disney/get_hotel_followup', data = json.dumps(payload))
        # return res.json()
        # end_time = datetime.now()
        # response_time = (end_time - start_time).total_seconds()
        # logger.info(f"API Response Time: {response_time} seconds")
        dispatcher.utter_message(text=str(res.json()))

class ActionRecommend(Action):

    def name(self) -> str:
        return "action_recommend"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        budget_value = tracker.get_slot("MONEY")
        
        payload = {
            "query": "query",
            "budget":f"{budget_value}"
        }
        
        # dispatcher.utter_message(text=payload)
        # start_time = datetime.now()
        res = requests.post(url = 'http://18.117.181.137:3890/disney/get_hotel', data = json.dumps(payload))
        # return res.json()
        # end_time = datetime.now()
        # response_time = (end_time - start_time).total_seconds()
        # carousel_data = convert_format_a_to_b(res)
        dispatcher.utter_message(json_message=res.json())
        # dispatcher.utter_message(text=str(res.json()))
        # logger.info(f"API Response Time: {response_time} seconds")
        return []


class ActionLangchainPayload2(Action):

    def name(self) -> str:
        return "action_langchain_payload2"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        date_value = tracker.get_slot("DATE")
        user_query= tracker.get_slot("user_query")
        # Get session ID (sender_id) from tracker
        session_id = tracker.sender_id
        payload = {
            "num_days": "{date_value}",
            "num_adults": 3,
            "num_boys": 2,
            "num_girls": 2,  
            "user_query": "{user_query}",
            "hashkey": "{session_id}"
        }
        # start_time = datetime.now()
        res = requests.post(url = 'http://18.117.181.137:3890/disney/get_itinerary', data = json.dumps(payload))
        # return res.json()
        # end_time = datetime.now()
        # response_time = (end_time - start_time).total_seconds()
        # logger.info(f"API Response Time: {response_time} seconds")
        dispatcher.utter_message(text=str(res.json()))

class ActionSaveHotelQuestion(Action):

    def name(self) -> str:
        return "action_save_hotel_question"

    def run(self, dispatcher, tracker, domain):
        # Get the last user message
        user_query = tracker.latest_message.get('text')

        # Set the user_message slot with the value
        return [SlotSet("hotel_query", user_query)]


class ActionHandleHotelInquiry(Action):
    def name(self):
        return "action_handle_hotel_inquiry"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain):

        # Get slot values from the form
        query_value = tracker.get_slot('hotel_query')
        # Get session ID (sender_id) from tracker
        session_id = tracker.sender_id

        payload = {
            "followup_question": query_value,
            "query": "",
            "budget": "",
            "hashkey": session_id,
            "is_followup": "no"
        }

        # start_time = datetime.now()
        # dispatcher.utter_message(text=f"{payload}")
        res = requests.post(url = 'http://18.117.181.137:3890/disney/get_hotel_followup', data = json.dumps(payload))
        # return res.json()
        # end_time = datetime.now()
        # response_time = (end_time - start_time).total_seconds()
        # logger.info(f"API Response Time: {response_time} seconds")
        dispatcher.utter_message(text=str(res.json()))

class ActionFallbackLangchain(Action):
    def name(self) -> str:
        return "action_fallback_langchain"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the last user message
        user_message = tracker.latest_message['text']
        # date_value = tracker.get_slot("DATE")
        # Get session ID (sender_id) from tracker
        session_id = tracker.sender_id

        # Define the Langchain API endpoint and parameters
        langchain_url = "http://18.117.181.137:3890/disney/get_hotel_followup"
        # headers = {
        #     "Content-Type": "application/json",
        #     "Authorization": "Bearer YOUR_API_TOKEN"
        # }
        payload = {
            "followup_question": user_message,
            "query": "",
            "budget": "",
            "hashkey": session_id,
            "is_followup": "no"
        }
        # start_time = datetime.now()

        # Send a request to the Langchain API
        response = requests.post(langchain_url, data= json.dumps(payload))
        # end_time = datetime.now()
        # response_time = (end_time - start_time).total_seconds()
        # logger.info(f"API Response Time: {response_time} seconds")
       
        dispatcher.utter_message(text=str(response.json()))

        return []


