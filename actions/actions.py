import re
import datetime as dt
from abc import ABC
from typing import Text, List, Any, Dict
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


# import spacy
#
# nlp = spacy.load("en_core_web_sm")


class ValidateNameForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_name_form"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Validate `first_name` value."""

        first_name = tracker.get_slot("first_name")
        # If the name is super short, it might be wrong.
        # print(f"First name given =" + first_name + "length = {len(slot_value)}")
        if len(first_name) <= 2:
            dispatcher.utter_message(text="That's a very short name. I'm assuming you mis-spelled.")
            dispatcher.utter_message(text="Enter your name again please")
            return [{"first_name": None}]
        else:
            return [{"first_name": first_name}]


class Name(Action):

    def name(self) -> Text:
        return "check_name_filled"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Validate `first_name` value."""

        first_name = tracker.get_slot("first_name")
        # If the name is super short, it might be wrong.
        # print(f"First name given =" + first_name + "length = {len(slot_value)}")
        if first_name is None:
            dispatcher.utter_message(response="utter_reply_no_name")
            dispatcher.utter_message(response="utter_ask_permission")
            return []
        else:
            dispatcher.utter_message(response="utter_reply_name")
            return []


class NameCheck(Action):

    def name(self) -> Text:
        return "change_name_filled"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Validate `first_name` value."""

        first_name = tracker.get_slot("first_name")
        # If the name is super short, it might be wrong.
        # print(f"First name given =" + first_name + "length = {len(slot_value)}")
        if first_name is not None:
            dispatcher.utter_message(response="utter_name_already_given")
            return []


class ValidateEmail(FormValidationAction):
    def name(self) -> Text:
        return "validate_email_form"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        """Validate `email` value."""
        email = tracker.get_slot("email")
        valid = re.search(r"[\w-]{1,20}@\w{2,20}\.\w{2,3}$", str(email))
        # If the name is super short, it might be wrong.

        if valid:
            print("valid email")
            dispatcher.utter_message(response="utter_subscribed")
            dispatcher.utter_message(response="utter_help")
            return [{"email": email}]
        else:
            dispatcher.utter_message(text=f"Actually, {email} is an invalid email. Try again.")
            dispatcher.utter_message(response="utter_ask_email")
            print(f"{email} is invalid")
            return [{"email": None}]


# class SayName(Action):
#     def name(self) -> Text:
#         return "reply_name"
#
#     def reply_name(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#
#         first_name = tracker.get_slot("first_name")
#
#         if len(first_name) <= 0:
#             dispatcher.utter_message(text=f"You haven't given me your name yet.")
#         else:
#             dispatcher.utter_message(text=f"Your name is {first_name}")


class ActionTime(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        now = dt.datetime.now().strftime("Today's date is %d/%m/%Y 🗓 and the time is %H:%M ⌚️")

        dispatcher.utter_message(text=f"{now}️")
        print("telling the time")
        return []
