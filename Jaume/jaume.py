from ollama import Client
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from firebase_utils import *
from data_to_context_utils import *
# use streamlit.io for the frontend

llm = ChatOllama(model="qwen3:4b", temperature=0.7,reasoning=True)
client = Client()

players = get_players()
matches = get_matches()
actions = get_match_actions()
# de cada player q saque una puntuacion
# normalizar las puntuaciones
# al systenm no hay que darlae acciones, es describir lo que es y como lo ha de hacer
# meter un human msg q diga que quiero
context = build_context(players, matches, actions)
systemPrompt = f"""
You are Jaume, a charismatic football assistant for the JF League.
You use data about player performance, team history, and match results to balance teams.

Rules:
- Before balancing teams, make sure you know the players available, ask for the list if needed.
- Distribute all the data evenly between two teams: TeamBlanc and TeamNegre.
- Explain your reasoning and include a funny warm-up suggestion.
- When asked to balance teams, return a list of player names like this:

TeamBlanc: [player1, player2, ...]
TeamNegre: [playerA, playerB, ...]

- Include a detailed explanation of your choices after the team lists.

{context}
"""


messages = [SystemMessage(content=systemPrompt),]

# add streaming of the tokens 

if __name__ == "__main__":
    print("""     _   _   _   _ __  __ _____                                    
    | | / \ | | | |  \/  | ____|                                   
 _  | |/ _ \| | | | |\/| |  _|                                     
| |_| / ___ \ |_| | |  | | |___                                    
 \___/_/   \_\___/|_|  |_|_____|       _                           
| |_ ___  __ _ _ __ ___   | |__   __ _| | __ _ _ __   ___ ___ _ __ 
| __/ _ \/ _` | '_ ` _ \  | '_ \ / _` | |/ _` | '_ \ / __/ _ \ '__|
| ||  __/ (_| | | | | | | | |_) | (_| | | (_| | | | | (_|  __/ |   
 \__\___|\__,_|_| |_| |_| |_.__/ \__,_|_|\__,_|_| |_|\___\___|_|   """)
    while True:
        user_input = input("\n\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        messages.append(HumanMessage(content=user_input))
        #response = llm.invoke(messages)
        #messages.append(AIMessage(content=response.content))
        print("\n\nJaume: ", end="", flush=True)
        response_text = ""
        for chunk in llm.stream(messages):
            token = chunk.content
            print(token, end="", flush=True)
            response_text += token

        messages.append(AIMessage(content=response_text))
        print()

        
   