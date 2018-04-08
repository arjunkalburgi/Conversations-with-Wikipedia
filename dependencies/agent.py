""" have a conversation """

# import re, requests, json, inquirer, unicodedata, Algorithmia, 

import wikipedia, wikipediaapi
import inquirer, random

# This project
from .helper import PromptMixin, ConverseMixin
from .hiddenkeysfilled import username, password
from .pyteaser import Summarize

# Watson API
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as watson
from watson_developer_cloud.natural_language_understanding_v1 import Features, ConceptsOptions, EntitiesOptions, KeywordsOptions, RelationsOptions, SemanticRolesOptions


class ConversationalAgent(PromptMixin, ConverseMixin):
    """

    """

    def __init__(self): 
        self.watsonobj = watson(username=username, password=password, version="2017-02-27")
        self.wikiapi = wikipediaapi.Wikipedia('en')
        self.interestList = []

    def prompt(self): 
        print("Hello, ", end='')
        question = random.choice(["What would you like to learn about?",
                                  "What topic do you want to know more about?", 
                                  "What do you want to learn about?"])
        raw_topic = input(question + " \n>>> ")

        if raw_topic in ["quit", "close", "stop"]: 
            exit()

        if "how" in raw_topic: 
            print("Explaining 'how' is not yet supported.")
            return 

        self.gettopic(raw_topic)

    def summarize(self): 
        if self.wiki_wiki_page.summary != "":
            print(Summarize(self._topic, self.wiki_wiki_page.summary))

    def converse(self): 
        choices = [section.title for section in self.wiki_wiki_page.sections]
        if "See also" in choices : choices.remove("See also")
        if "References" in choices : choices.remove("References")
        if "Further reading" in choices : choices.remove("Further reading")
        if "External links" in choices : choices.remove("External links")
        choices.append("None of these")
        choices.append("Exit")

        question = random.choice(["Would you like to learn about any of these?",
                                  "Are you interested in any of these?", 
                                  "Which of these would you like to learn about?", 
                                  "Here are a list of subtopics I found about "+self._topic+", which of these intrigue you?",
                                  "In "+self._topic+", I found these subtopics. What interests you?", 
                                  "In "+self._topic+", I found these subtopics. Which would you like to learn about?", 
                                  self._topic+" has some subtopics. What interests you?", 
                                  self._topic+" has some subtopics. Which would you like to learn about?"])

        questions = [
            inquirer.Checkbox(self._topic,
                              message=question,
                              choices=choices,
                              ),
        ]

        answers = inquirer.prompt(questions)[self._topic]

        if answers is []: 
            print("Please select one by using the right arrow key.")
            self.converse()

        if "None of these" in answers:
            print("The ability to request custom content on a page is not implemented yet")
            return 
        if "Exit" in answers: 
            print("What to do here is not implemented yet")
            return 

        self.interestList = self.interestList + [interest for interest in answers]

        while len(self.interestList) > 0:
            if len(answers) > 1:
                self.askfororder(answers)
                answers = []
            elif len(self.interestList) > 1:
                self.askfororder(self.interestList)
            else:
                print("Alright, looking into " + self.interestList[0])
                self.breakDownSection(self.interestList[0])

    def followup(self):
        prompt = random.choice(["Do you have any more questions about this topic?",
                                "Were you hoping to learn anything else about this topic?"])
        answer = input(prompt + " \n>>> ")

        # analyse for "no"
        if answer.lower() == "no":
            print("Alright, ask again soon!") 
            exit()

        try:
            concepts = self.watsonobj.analyze(text=answer, features=Features(concepts=ConceptsOptions(limit=3)))
            print(Summarize(" ".join([c['text'] for c in concepts['concepts']]), self.wiki_wiki_page.text, 5))
        except Exception:
            print(Summarize(answer, self.wiki_wiki_page.text, 10))

        self.followup()

