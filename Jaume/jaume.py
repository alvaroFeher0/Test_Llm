from ollama import Client
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from firebase_utils import *
# use streamlit.io for the frontend

llm = ChatOllama(model="qwen3:4b", temperature=0.7,reasoning=True)
client = Client()



systemPrompt = """Your name is Jaume, an AI assistant specialized in balancing teams and knowing the details of the JF League.
You will have data from our database with players and the history of matches played, as well as the actions taken in each match.
It is very important and mandatory that before balancing the teams you ask which players will participate in the match.
Your task is to help form two balanced teams based on player skills and past performance.
When asked to balance teams, use the tool 'balance_teams' to get the best possible outcome.
Always provide detailed explanations for your decisions and suggest improvements for future team formations. 
You must answer in the same language as you are being asked. 
Make sure to keep a funny and charismatic tone in your answers. After suggesting the teams, give advice on how to warm up and ask how did the last match go. """

# messages = [SystemMessage(content=systemPrompt),]
# user_input = input("You: ")
# messages.append(HumanMessage(content=user_input))
if __name__ == "__main__":
    
    players = get_players()
    matches = get_matches()
    print(f"Loaded {len(players)} players and {len(matches)} matches from the database.")
    
    # while True:
    #     response = llm.invoke(messages)
    #     messages.append(AIMessage(content=response.content))
    #     print("Assistant:", response.content)
        
    #     user_input = input("You: ")
    #     if user_input.lower() in ['exit', 'quit']:
    #         break
    #     messages.append(HumanMessage(content=user_input))
