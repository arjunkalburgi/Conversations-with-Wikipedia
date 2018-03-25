""" have a conversation """

# import re, requests, json, inquirer, unicodedata, Algorithmia, 

import wikipedia, wikipediaapi
import inquirer, random

from .hiddenkeysfilled import username, password
from .pyteaser import Summarize

from watson_developer_cloud import NaturalLanguageUnderstandingV1 as watson
from watson_developer_cloud.natural_language_understanding_v1 import Features, ConceptsOptions, EntitiesOptions, KeywordsOptions, RelationsOptions, SemanticRolesOptions



class conversational_agent():
    """

    """

    def __init__(self): 
        self.watsonobj = watson(username=username, password=password, version="2017-02-27")
        self.wikiapi = wikipediaapi.Wikipedia('en')
        self.interestList = []

    def prompt(self): 
        question = random.choice(["What would you like to learn about?",
                                  "What topic do you want to know more about?", 
                                  "What do you want to learn about?"])
        raw_topic = input(question + " \n>>> ")

        if raw_topic in ["quit", "close", "stop"]: 
            exit()

        if "how" in raw_topic: 
            print("Explaining 'how' is not yet supported.")
            return 

        # set proper topic 
        self.getTopic(raw_topic)

        # read summary 
        if self.wiki_wiki_page.summary != "":
            print(Summarize(self._topic, self.wiki_wiki_page.summary))

        # present subtopic options 
        self.present_options()

        # anything more 
        self.anymore_questions()

    def getTopic(self, topic):
        # if match
        if topic in wikipedia.search(topic):
            print("Pulling from wiki page on " + topic + ".")
            self._topic = topic
            # self.wiki_page = wikipedia.WikipediaPage(self._topic)
            self.wiki_wiki_page = self.wikiapi.page(self._topic)

        # if close match
        elif wikipedia.suggest(topic) is not None:
            print("Pulling from " + wikipedia.suggest(topic) +
                  ", if this isn't correct please exit and specify a different query.")
            self._topic = wikipedia.suggest(topic)
        # no matches
        else:
            print("That topic didn't work, please try again")
            exit()

    def present_options(self): 

        choices = [section.title for section in self.wiki_wiki_page.sections]
        if "See also" in choices : choices.remove("See also")
        if "References" in choices : choices.remove("References")
        if "External links" in choices : choices.remove("External links")
        choices.append("Other")
        choices.append("None of these")

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
            self.present_options()

        if "Other" in answers: 
            print("Other is not implemented yet")
            return 
        if "None of these" in answers: 
            print("What to do here is not implemented yet")
            return 

        self.interestList = self.interestList + [interest for interest in answers]

        while len(self.interestList) > 0:
            if len(answers) > 1:
                self.__askfororder(answers)
            elif len(self.interestList) > 1:
                self.__askfororder(self.interestList)
            else:
                self.__breakDownSection(self.interestList[0])

    def anymore_questions(self):
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

        self.anymore_questions()






    def __askfororder(self, interests):
        question = random.choice(["Which would you like to learn about first?",
                                  "Which of these would you like to learn about first?",
                                  "Which one should I go over first?"])

        questions = [
            inquirer.List("learnnow",
                            message=question,
                            choices=interests,
                            ),
        ]

        answer = inquirer.prompt(questions)

        self.__breakDownSection(answer["learnnow"])

    def __breakDownSection(self, sectionname):
        # find the section in the wikipedia page 
        section = next((x for x in self.wiki_wiki_page.sections if x.title == sectionname), None)

        if not section.sections:
            self.__learnSection(section)
        else:
            self.__learnSubsection(section)

    def __learnSection(self, sectionObject): 
        # goes here when page section does not have subsections 
        # create summary using section 
        Summarize(" ".join([self._topic, sectionObject.title]),sectionObject.text)

        # Ask for more explore 
        self.__exploreSection(sectionObject)

        # remove from interest list 
        self.interestList.remove(sectionObject.title)

    def __learnSubsection(self, sectionObject): 
        # goes here when page section has subsections
        # get all subsection titles 
        # create summary using subsection titles as query 
        print("__learnSubsection")

    def __exploreSection(self, sectionObject, keywords=None): 
        prompt = random.choice(["Do you have any interests here?",
                                "Does anything interest you, I can explain further."])
        answer = input(prompt + " \n>>> ")

        # analyse for "no"
        if answer.lower() == "no":
            return 

        if keywords is None: 
            keywords = []

        keywords.append(answer)

        try:
            concepts = self.watsonobj.analyze(text=answer, features=Features(concepts=ConceptsOptions(limit=3)))
            concepts = concepts + keywords
            print(Summarize(" ".join([c['text'] for c in concepts['concepts']]), sectionObject.text))
        except Exception:
            print(Summarize(keywords, self.wiki_wiki_page.text))

        # Feature: provide own section list 
        # print("This section has it's own related link")
        # def __suggestTopicResources(self, sectionObject):

        self.__exploreSection(sectionObject, keywords)
