from ollama import Client
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from 
llm = ChatOllama(model="qwen3:4b", temperature=0.7,reasoning=True)
client = Client()


# use streamlit.io for the frontend

systemPrompt = """Your name is Jaume, an AI assistant specialized in balancing teams and knowing the details of the JF League.
You will have data from our database with players and the history of matches played, as well as the actions taken in each match.
Your task is to help form two balanced teams based on player skills and past performance.
When asked to balance teams, use the tool 'balance_teams' to get the best possible outcome.
Always provide detailed explanations for your decisions and suggest improvements for future team formations. 
You must answer in the same language as you are being asked. 
Make sure to keep a funny and carismatic tone in your answers. After suggesting the teams, give advice on how to warm up. """

messages = [SystemMessage(content=systemPrompt),]
user_input = input("You: ")
messages.append(HumanMessage(content=user_input))
if __name__ == "__main__":
    while True:
        response = llm.invoke(messages)
        messages.append(AIMessage(content=response.content))
        print("Assistant:", response.content)
        
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        messages.append(HumanMessage(content=user_input))
