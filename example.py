from dependencies.agent import conversational_agent
from dependencies.pyteaser import Summarize

agent = conversational_agent()

agent.getTopic("Cooking")

# read summary
if agent.wiki_wiki_page.summary != "":
    print(Summarize(agent._topic, agent.wiki_wiki_page.summary))

# present subtopic options
agent.present_options()

# # anything more
# agent.anymore_questions()


# exec(open("example.py").read())
