import streamlit as st
from ollama import Client
from firebase_utils import get_players, get_matches, get_match_actions
from data_to_context_utils import build_context
from openai import OpenAI
from dotenv import load_dotenv
import os

st.set_page_config(page_title="JF League Assistant", page_icon="⚽", layout="centered")
st.title("⚽ Jaume – JF League Team Balancer")

with st.spinner("Loading league data..."):
    players = get_players()
    matches = get_matches()
    actions = get_match_actions()
context = build_context(players, matches, actions)

#client = Client()
load_dotenv()
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

system_prompt = f"""
You are Jaume, a charismatic football assistant for the JF League that speaks spanish and loves to use quotes from Andres Montes.
You use data about player performance, team history, and match results to balance teams.

Rules:
- Ask for a list of the players that will play the match
- Distribute all the data evenly between two teams: Team Blanc and Team Negre.
- Explain your reasoning fro the balancing of teams
- When asked to balance teams, return a list of player names like this:

TeamBlanc: [player1, player2, ...]
TeamNegre: [playerA, playerB, ...]

- Include a detailed explanation of your choices after the team lists.
- ignore any questions not related to balancing teams or to the performance of players in the JF League.
- if you are asked a question not related to the JF League, politely decline to answer.
- whenever you talk about Lluis, always add a compliment about him
{context}
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.session_state.needs_greeting = True
else:
    st.session_state.needs_greeting = False


# generate initial greeting
def greeting_generator():
    seed_messages = st.session_state.messages + [
        {"role": "user", "content": "Jaume, saluda a la liga y pide la lista de jugadores disponibles para equilibrar los equipos. Sé divertido y enérgico, como Andrés Montes."}
    ]
    return response_generator(seed_messages)
            
def response_generator(messages):
    response = ""
    for chunk in client.chat.completions.create(
        model="gpt-5-nano",
        messages=messages,
        stream=True,
    ):
        piece = chunk.choices[0].delta.content or ""
        if piece:
            response += piece
            yield piece 
    return response


if st.session_state.needs_greeting:
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("_Jaume is thinking..._")
        st.write_stream(greeting_generator())
    st.session_state.needs_greeting = False 
    
            
for msg in st.session_state.messages[1:]:  # skip system
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Talk to Jaume..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("_Jaume is thinking..._")
        stream_text = st.write_stream(response_generator(st.session_state.messages))
        #placeholder.markdown(stream_text)
    st.session_state.messages.append({"role": "assistant", "content": stream_text})
     

