# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import pandas as pd
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from random import choice


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionIdentifyPerson(Action):

    def name(self) -> Text:
        return "action_identify_person"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        person_name = tracker.get_slot("person_name")

        df = pd.read_excel("actions/list_new.xlsx")
        df = df.fillna(0)

        print("Person Name--------->",person_name)
        name = person_name

        data_name = len(df[df['Name'] == name])
        # data_event = len(df[df['Event'] == name])
        if data_name > 0:
            # if entity == "name":
            data_title = df[(df['Name'] == name) & (df['Title'] != 0)]
            data_movie_title = df[(df['Name'] == name) & (df['Movie Title'] != 0)]

        # elif entity == "event":
        else:
            data_title = df[(df['Event'] == name) & (df['Title'] != 0)]
            data_movie_title = df[(df['Event'] == name) & (df['Movie Title'] != 0)]

        data_title = " / ".join(data_title['Title'].values)

        print("data_title ---->",data_title)

        data_movie_title = " / ".join(data_movie_title['Movie Title'].values)

        print("data_movie_title---->",data_movie_title)

        info = ""
        if len(data_title) > 0:
            info += "Titles ("+data_title+") "
        if len(data_movie_title) > 0:
            info += "Movie Titles ("+data_movie_title+")"

        if info != "":
            temp = "For ({}) we have ({})".format(person_name, info)
        else:
            temp = "For ({}) we don't have any information".format(person_name)

        dispatcher.utter_message(temp)

        return []

class ActionIdentifyEvent(Action):

    def name(self) -> Text:
        return "action_identify_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        event_name = tracker.get_slot("event_name")
        
        df = pd.read_excel("actions/list_new.xlsx")
        df = df.fillna(0)

        print("Event Name--------->",event_name)

        data_title = df[(df['Event'] == event_name) & (df['Title'] != 0)]
        data_movie_title = df[(df['Event'] == event_name) & (df['Movie Title'] != 0)]
        print("Event================")
        print(data_title.head())

        data_title = " | ".join(data_title['Title'].values)

        print("data_title ---->",data_title)

        data_movie_title = " | ".join(data_movie_title['Movie Title'].values)

        print("data_movie_title---->",data_movie_title)


        temp = "For ({}) we have (and then the info from the list)".format(event_name)

        dispatcher.utter_message(temp)

        return []

class ActionDefaultFallback(Action):
    """
    Default Action Fallback for the Input below Threshold value
    """

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "action_default_fallback"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:

        li = ["I didn't get you. Can you please re-phrase it", "I think i am not trained for this yet", "Sorry, Didn't get you. Can you please re-phrase it"]
        print("Response -> ",li)
        text = choice(li)
        dispatcher.utter_message(text=text)

        return []
