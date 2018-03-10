
from dependencies.agent import conversational_agent


agent = conversational_agent() 

print("Hello, ", end='')

while True: 
    agent.prompt()


    

