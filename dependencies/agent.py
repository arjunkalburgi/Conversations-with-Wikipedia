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
        self.wiki_wiki = wikipediaapi.Wikipedia('en')
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
        self.__getTopic(raw_topic)

        # read summary 
        if self.wiki_wiki_page.summary != "":
            print(Summarize(self._topic, self.wiki_wiki_page.summary))

        # present subtopic options 
        self.__present_options()

        # anything more 
        self.__anymore_questions()

    def __getTopic(self, topic):
        # if match
        if topic in wikipedia.search(topic):
            print("Pulling from wiki page on " + topic + ".")
            self._topic = topic
            self.wiki_page = wikipedia.WikipediaPage(self._topic)
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

        answers = inquirer.prompt(questions)

        if "Other" in answers: 
            print("Other is not implemented yet")
            exit 
        if "None of these" in answers: 
            print("What to do here is not implemented yet")
            exit 

        self.interestList = self.interestList + [self._topic + "::" + interest for interest in answers[self._topic]]

        if len(answers[self._topic]) > 1:
            self.__askfororder(answers[self._topic])
        elif len(self.interestList) > 1:
            self.__askfororder(self.interestList)
        else:
            self.__startLearning(self.interestList[0])

    def __anymore_questions(self):
        prompt = random.choice(["Do you have any more questions about this topic?",
                                "Were you hoping to learn anything else about this topic?"])
        answer = input(prompt + " \n>>> ")

        # analyse for "no"
        if "no" in answer.lower():
            print("Alright, ask again soon!") 
            exit 

        concepts = self.watsonobj.analyze(text=answer, features=Features(concepts=ConceptsOptions(limit=3)))
        
        Summarize(" ".join([c.text for c in concepts.concepts]), self.wiki_page.text)

        self.__anymore_questions()






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

        self.__startLearning(answer["learnnow"])

    def __startLearning(self, sectionname):
        section = next((x for x in self.wiki_wiki_page.sections if x.title == sectionname), None)

        if not section.sections:
            self.__learnSection(section)
        else:
            self.__learnSubsection(section)

    def __learnSection(self, sectionObject): 
        # goes here when page section does not have subsections 
        # create summary using section 
        # def __requestion(self, )        

    def __learnSubsection(self, sectionObject): 
        # goes here when page section has subsections
        # get all subsection titles 
        # create summary using subsection titles as query 
        # def __requestion(self, )        
