""" have a conversation """

# import re, requests, json, inquirer, unicodedata, Algorithmia, 

import wikipedia, json

from hiddenkeys import username, password

from watson_developer_cloud import NaturalLanguageUnderstandingV1 as watson
from watson_developer_cloud.natural_language_understanding_v1 import Features, ConceptsOptions, EntitiesOptions, KeywordsOptions, RelationsOptions, SemanticRolesOptions



class conversational_agent():
    """

    """

    def __init__(self): 
        self.watsonobj = watson(username=username, password=password, version="2017-02-27")

    def prompt(self): 
        raw_topic = raw_input("Hello, what would you like to learn about? \n>>> ")

        # set proper topic 
        self.__getTopic(raw_topic)

    def __getTopic(self, topic):
        # if match
        if topic in wikipedia.search(topic):
            print("Pulling from wiki page on " + topic + ".")
            self._topic = topic
        # if close match
        elif wikipedia.suggest(topic) is not None:
            print("Pulling from " + wikipedia.suggest(topic) +
                  ", if this isn't correct please exit and specify a different query.")
            self._topic = wikipedia.suggest(topic)
        # no matches
        else:
            print("That topic didn't work, please try again")
            exit()


