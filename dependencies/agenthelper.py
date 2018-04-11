import wikipedia, inquirer, random
from .pyteaser import Summarize
from watson_developer_cloud.natural_language_understanding_v1 import Features, ConceptsOptions

class PromptMixin():

    def gettopic(self, topic):
        topic = topic.strip()
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

class ConverseMixin(): 
    
    def askfororder(self, interests):
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

        self.breakDownSection(answer["learnnow"])

    def breakDownSection(self, sectionname):
        # find the section in the wikipedia page 
        section = next((x for x in self.wiki_wiki_page.sections if x.title == sectionname), None)

        if not section.sections:
            self.learnSection(section)
        else:
            self.learnSubsection(section)

    def learnSection(self, sectionObject):
        # goes here when page section does not have subsections
        # create summary using section
        print(Summarize(" ".join([self._topic, sectionObject.title]), sectionObject.text, 3))

        # Ask for more explore
        self.exploreSection(sectionObject)

        # remove from interest list
        self.interestList.remove(sectionObject.title)

    def learnSubsection(self, sectionObject):
        # goes here when page section has subsections
        # get all subsection titles
        keywords = [x.title for x in sectionObject.sections]
        for section in sectionObject.sections:
            keywords = keywords + [x.title for x in section.sections]

        # create summary using subsection titles as query
        print(Summarize(" ".join(keywords), str(sectionObject), 7))

        # Ask for more explore
        self.exploreSection(sectionObject)

        # remove from interest list
        self.interestList.remove(sectionObject.title)

    def exploreSection(self, sectionObject, keywords=None):
        prompt = random.choice(["Do you have any interests here?",
                                "Does anything interest you, I can explain further."])
        answer = input(prompt + " \n>>> ")

        # analyse for "no"
        if answer.lower().strip() == "no":
            return

        # Did they ask for a subsection

        if keywords is None:
            keywords = []
        keywords.append(answer)

        self.summarizewithkeywords(keywords, str(sectionObject))
        # Feature: provide own section list
        # print("This section has it's own related link")
        # def suggestTopicResources(self, sectionObject):

        self.exploreSection(sectionObject, " ".join(keywords))

    def summarizewithkeywords(self, keywords, text, words=None): 
        try:
            concepts = self.watsonobj.analyze(text=keywords, features=Features(concepts=ConceptsOptions(limit=3)))
            print(Summarize(" ".join([c['text'] for c in concepts['concepts']]), text, words))
        except Exception:
            print(Summarize(" ".join(keywords), text, words))
