import pathlib
import re
import datetime as dt
from abc import ABC
from typing import Text, List, Any, Dict
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

names = pathlib.Path("data/names.txt").read_text().split("\n")


class ValidateHealthForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_health_form"

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict"
    ) -> List[Text]:
        return ["exercise", "sleep", "diet", "goal"]


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
        if len(first_name) <= 2 or str(first_name).lower() not in names:
            dispatcher.utter_message(text="That's a very interesting name lol but ok...")
            return [{"first_name": first_name}]
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


class Question1(Action):

    def name(self) -> Text:
        return "check_q1_filled"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Validate `first_name` value."""

        answer = tracker.get_slot("quiz_ans")
        answer = str(answer).lower()
        # If the name is super short, it might be wrong.
        # print(f"First name given =" + first_name + "length = {len(slot_value)}")
        if answer == "realistic":
            print("correct")
            dispatcher.utter_message(text=f"Correct!")
            return []
        else:
            dispatcher.utter_message(text=f"Incorrect, the answer was Realistic")
            return []


class Question2(Action):

    def name(self) -> Text:
        return "check_q2_filled"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Validate `first_name` value."""

        answer = tracker.get_slot("quiz_ans")
        answer = str(answer).lower()
        # If the name is super short, it might be wrong.
        # print(f"First name given =" + first_name + "length = {len(slot_value)}")
        if answer == "long term goal":
            dispatcher.utter_message(text=f"Correct!")
            return []
        else:
            dispatcher.utter_message(text=f"Incorrect, the answer was Long Term Goal")
            return []


class Question3(Action):

    def name(self) -> Text:
        return "check_q3_filled"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Validate `first_name` value."""

        answer = tracker.get_slot("quiz_ans")
        answer = str(answer).lower()
        # If the name is super short, it might be wrong.
        # print(f"First name given =" + first_name + "length = {len(slot_value)}")
        if answer == "achievable":
            dispatcher.utter_message(text=f"Correct!")
            return []
        else:
            dispatcher.utter_message(text=f"Incorrect, the answer was Achievable")
            return []


class Question4(Action):

    def name(self) -> Text:
        return "check_q4_filled"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Validate `first_name` value."""

        answer = tracker.get_slot("quiz_ans")
        answer = str(answer).lower()
        # If the name is super short, it might be wrong.
        # print(f"First name given =" + first_name + "length = {len(slot_value)}")
        if answer == "r":
            dispatcher.utter_message(text=f"Correct!")
            return []
        else:
            dispatcher.utter_message(text=f"Incorrect, the answer was R")
            return []


class CalculateJobForm(Action):

    def name(self) -> Text:
        return "action_submit_all_forms_calc_score"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        practical = tracker.get_slot("practical")
        athletic = tracker.get_slot("athletic")
        straightforward = tracker.get_slot("straightforward")
        mechanicalproblem = tracker.get_slot("mechanicalproblem")
        pitchatent = tracker.get_slot("pitchatent")
        playsport = tracker.get_slot("playsport")
        tinkermachine = tracker.get_slot("tinkermachine")
        workoutdoor = tracker.get_slot("workoutdoor")
        physcialactive = tracker.get_slot("physcialactive")
        inquisitive = tracker.get_slot("inquisitive")
        analytical = tracker.get_slot("analytical")
        scientific = tracker.get_slot("scientific")
        abstractly = tracker.get_slot("abstractly")
        mathproblem = tracker.get_slot("mathproblem")
        physicstheories = tracker.get_slot("physicstheories")
        exploreidea = tracker.get_slot("exploreidea")
        usecomputer = tracker.get_slot("usecomputer")
        workindepen = tracker.get_slot("workindepen")
        creative = tracker.get_slot("creative")
        intuitive = tracker.get_slot("intuitive")
        imaginative = tracker.get_slot("imaginative")
        sketch = tracker.get_slot("sketch")
        intuition = tracker.get_slot("intuition")
        musical = tracker.get_slot("musical")
        originalways = tracker.get_slot("originalways")
        fiction = tracker.get_slot("fiction")
        verbalabilities = tracker.get_slot("verbalabilities")
        friendly = tracker.get_slot("friendly")
        helpful = tracker.get_slot("helpful")
        idealistic = tracker.get_slot("idealistic")
        insightful = tracker.get_slot("insightful")
        trainothers = tracker.get_slot("trainothers")
        feelingclearly = tracker.get_slot("feelingclearly")
        groupdiscussion = tracker.get_slot("groupdiscussion")
        interpersonalskills = tracker.get_slot("interpersonalskills")
        helppeople = tracker.get_slot("helppeople")
        leadgroups = tracker.get_slot("leadgroups")
        selfconfident = tracker.get_slot("selfconfident")
        asser = tracker.get_slot("asser")
        sociable = tracker.get_slot("sociable")
        initiativeprojects = tracker.get_slot("initiativeprojects")
        thingsyourway = tracker.get_slot("thingsyourway")
        promoteideas = tracker.get_slot("promoteideas")
        affectingothers = tracker.get_slot("affectingothers")
        energyordrive = tracker.get_slot("energyordrive")
        speechesortalks = tracker.get_slot("speechesortalks")
        detailsandnumbers = tracker.get_slot("detailsandnumbers")
        numbercrunching = tracker.get_slot("numbercrunching")
        methodical = tracker.get_slot("methodical")
        systemororganisation = tracker.get_slot("systemororganisation")
        writereports = tracker.get_slot("writereports")
        accuraterecords = tracker.get_slot("accuraterecords")
        definedprocedures = tracker.get_slot("definedprocedures")
        tablesandgraphs = tracker.get_slot("tablesandgraphs")
        workwithnumbers = tracker.get_slot("workwithnumbers")
        realistic_count = 0
        investigative_count = 0
        artistic_count = 0
        social_count = 0
        enterprising_count = 0
        conventional_count = 0
        if practical == "yes":
            realistic_count = realistic_count + 1
        if athletic == "yes":
            realistic_count = realistic_count + 1
        if straightforward == "yes":
            realistic_count = realistic_count + 1
        if mechanicalproblem == "yes":
            realistic_count = realistic_count + 1
        if pitchatent == "yes":
            realistic_count = realistic_count + 1
        if playsport == "yes":
            realistic_count = realistic_count + 1
        if tinkermachine == "yes":
            realistic_count = realistic_count + 1
        if workoutdoor == "yes":
            realistic_count = realistic_count + 1
        if physcialactive == "yes":
            realistic_count = realistic_count + 1
        if inquisitive == "yes":
            investigative_count = investigative_count + 1
        if analytical == "yes":
            investigative_count = investigative_count + 1
        if scientific == "yes":
            investigative_count = investigative_count + 1
        if abstractly == "yes":
            investigative_count = investigative_count + 1
        if mathproblem == "yes":
            investigative_count = investigative_count + 1
        if physicstheories == "yes":
            investigative_count = investigative_count + 1
        if exploreidea == "yes":
            investigative_count = investigative_count + 1
        if usecomputer == "yes":
            investigative_count = investigative_count + 1
        if workindepen == "yes":
            investigative_count = investigative_count + 1
        if creative == "yes":
            artistic_count = artistic_count + 1
        if intuitive == "yes":
            artistic_count = artistic_count + 1
        if imaginative == "yes":
            artistic_count = artistic_count + 1
        if sketch == "yes":
            artistic_count = artistic_count + 1
        if intuition == "yes":
            artistic_count = artistic_count + 1
        if musical == "yes":
            artistic_count = artistic_count + 1
        if originalways == "yes":
            artistic_count = artistic_count + 1
        if fiction == "yes":
            artistic_count = artistic_count + 1
        if verbalabilities == "yes":
            artistic_count = artistic_count + 1
        if friendly == "yes":
            social_count = social_count + 1
        if helpful == "yes":
            social_count = social_count + 1
        if idealistic == "yes":
            social_count = social_count + 1
        if insightful == "yes":
            social_count = social_count + 1
        if trainothers == "yes":
            social_count = social_count + 1
        if feelingclearly == "yes":
            social_count = social_count + 1
        if groupdiscussion == "yes":
            social_count = social_count + 1
        if interpersonalskills == "yes":
            social_count = social_count + 1
        if helppeople == "yes":
            social_count = social_count + 1
        if leadgroups == "yes":
            social_count = social_count + 1
        if selfconfident == "yes":
            enterprising_count = enterprising_count + 1
        if asser == "yes":
            enterprising_count = enterprising_count + 1
        if sociable == "yes":
            enterprising_count = enterprising_count + 1
        if initiativeprojects == "yes":
            enterprising_count = enterprising_count + 1
        if thingsyourway == "yes":
            enterprising_count = enterprising_count + 1
        if promoteideas == "yes":
            enterprising_count = enterprising_count + 1
        if affectingothers == "yes":
            enterprising_count = enterprising_count + 1
        if energyordrive == "yes":
            enterprising_count = enterprising_count + 1
        if speechesortalks == "yes":
            enterprising_count = enterprising_count + 1
        if detailsandnumbers == "yes":
            conventional_count = conventional_count + 1
        if numbercrunching == "yes":
            conventional_count = conventional_count + 1
        if methodical == "yes":
            conventional_count = conventional_count + 1
        if systemororganisation == "yes":
            conventional_count = conventional_count + 1
        if writereports == "yes":
            conventional_count = conventional_count + 1
        if accuraterecords == "yes":
            conventional_count = conventional_count + 1
        if definedprocedures == "yes":
            conventional_count = conventional_count + 1
        if tablesandgraphs == "yes":
            conventional_count = conventional_count + 1
        if workwithnumbers == "yes":
            conventional_count = conventional_count + 1
        print(realistic_count)
        print(investigative_count)
        print(artistic_count)
        print(social_count)
        print(enterprising_count)
        print(conventional_count)
        lst = [realistic_count, investigative_count, artistic_count, social_count, enterprising_count,
               conventional_count]

        if max(lst) == realistic_count:
            dispatcher.utter_message(
                text="You scored " + str(realistic_count) + "/9 for realistic. That was your highest!")
            dispatcher.utter_message(response="utter_realistic")
        elif max(lst) == investigative_count:
            dispatcher.utter_message(
                text="You scored " + str(investigative_count) + "/9 for investigative. That was your highest!")
            dispatcher.utter_message(response="utter_investigative")
        elif max(lst) == artistic_count:
            dispatcher.utter_message(
                text="You scored " + str(artistic_count) + "/9 for artistic. That was your highest!")
            dispatcher.utter_message(response="utter_artistic")
        elif max(lst) == social_count:
            dispatcher.utter_message(
                text="You scored " + str(social_count) + "/9 for social. That was your highest!")
            dispatcher.utter_message(response="utter_social")
        elif max(lst) == enterprising_count:
            dispatcher.utter_message(
                text="You scored " + str(enterprising_count) + "/9 for enterprising. That was your highest!")
            dispatcher.utter_message(response="utter_enterprising")
        elif max(lst) == conventional_count:
            dispatcher.utter_message(
                text="You scored " + str(conventional_count) + "/9 for conventional. That was your highest!")
            dispatcher.utter_message(response="utter_conventional")

        return []

