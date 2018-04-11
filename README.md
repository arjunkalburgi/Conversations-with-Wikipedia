# Conversations with Wikipedia

### How it works / Introduction

The goal of this project is to create an educational experience that is quick and context dependent, just like that of conversing with a teacher or peer. 

Chat-based teaching can be an effective way to learn but is difficult to scale while maintaining flexibility of topic. This tool is an attempt to create a conversational agent that can teach you about anything you'd like to know. 

```
from dependencies.agent import ConversationalAgent
agent = ConversationalAgent()
```

The system uses Wikipedia as a knowledge base and hosts conversations using Wikipedia pages. Answering it's prompt will search Wikipedia for an article on the topic. 

```
agent.prompt()
```

The agent then starts the conversation by summarizing the topic using the PyTeaser summarizer on the article's introduction. 

```
agent.summarize()
```

The agent then delves into the article, attempting to find more information for you to learn about. It takes advantage of page’s structure to help find you more information, constantly asking you if you'd like to explain further. 

```
agent.converse()
```

When you are ready to end the conversation, the agent asks one final time if there's anything else you'd like to learn about the topic and attempts to find that information for you from the article. 

```
agent.followup()
```

Work still needs to be done to improve the text summarization and the overall conversational flow.


### Build instructions 
 - `python setup.py`


### Run instructions 
 - `python learn.py`