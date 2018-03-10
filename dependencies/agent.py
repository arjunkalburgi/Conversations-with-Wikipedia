""" have a conversation """

# import re, requests, json, inquirer, unicodedata, Algorithmia, 

import wikipedia, json
import inquirer
import wikipediaapi

from .hiddenkeys import username, password

from watson_developer_cloud import NaturalLanguageUnderstandingV1 as watson
from watson_developer_cloud.natural_language_understanding_v1 import Features, ConceptsOptions, EntitiesOptions, KeywordsOptions, RelationsOptions, SemanticRolesOptions



class conversational_agent():
    """

    """

    def __init__(self): 
        self.watsonobj = watson(username=username, password=password, version="2017-02-27")
        self.wiki_wiki = wikipediaapi.Wikipedia('en')
        self.interestList = []

    def prompt(self): 
        raw_topic = input("What would you like to learn about? \n>>> ")

        if raw_topic in ["quit", "close", "stop"]: 
            exit()

        if "how" in raw_topic: 
            print("Explaining 'how' is not yet supported.")
            return 

        # set proper topic 
        self.__getTopic(raw_topic)

        self.__present_options()

    def __getTopic(self, topic):
        # if match
        if topic in wikipedia.search(topic):
            print("Pulling from wiki page on " + topic + ".")
            self._topic = topic
            self._page = wikipedia.WikipediaPage(self._topic)
            self.wiki_wiki_page = self.wiki_wiki.page(self._topic)

        # if close match
        elif wikipedia.suggest(topic) is not None:
            print("Pulling from " + wikipedia.suggest(topic) +
                  ", if this isn't correct please exit and specify a different query.")
            self._topic = wikipedia.suggest(topic)
        # no matches
        else:
            print("That topic didn't work, please try again")
            exit()

    def __present_options(self): 
        choices = [section.title for section in self.wiki_wiki_page.sections]
        choices.remove("See also")
        choices.remove("References")
        choices.remove("External links")

        questions = [
            inquirer.Checkbox(self._topic,
                              message="Would you like to learn about any of these?",
                              choices=choices,
                              ),
        ]

        answers = inquirer.prompt(questions)

        self.interestList = self.interestList + [self._topic + "::" + interest for interest in answers[self._topic]]

        if len(answers[self._topic]) > 1:
            self.__askfororder(answers[self._topic])
        elif len(self.interestList) > 1:
            self.__askfororder(self.interestList)
        else:
            self.__startLearning(self.interestList[0])

    def __askfororder(self, interests):
        questions = [
            inquirer.List("learnnow",
                            message="Which would you like to learn about first?",
                            choices=interests,
                            ),
        ]

        answer = inquirer.prompt(questions)

        self.__startLearning(answer)

    def __startLearning(self, section):
        # does have subsections? 
            # present subsection options 
            # answer depth vs bredth 

        # start learning 
