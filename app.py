
import streamlit as st
import os
from typing import TextIO

import openai
import pandas as pd
import streamlit as st
from langchain.agents import create_csv_agent, create_pandas_dataframe_agent
from langchain.llms import OpenAI
from utils import get_answer_csv

#openai.api_key = st.secrets["OPENAI_API_KEY"]
def set_openAi_api_key(api_key: str):
            st.session_state["OPENAI_API_KEY"] = api_key
            os.environ['OPENAI_API_KEY'] = api_key
def openai_api_insert_component():
            with st.sidebar:
                st.markdown(
                    """
                    ## Quick Guide 🚀
                    1. Get started by adding your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑
                    2. Easily upload your CSV document
                    3. Engage with the content - ask questions, seek answers💬
                    """
                )

                api_key_input = st.text_input("Input your OpenAI API Key",
                                            type="password",
                                            placeholder="Format: sk-...",
                                            help="You can get your API key from https://platform.openai.com/account/api-keys.")
                
                
                if api_key_input == "" or api_key_input is None:
                        st.sidebar.caption("👆 :red[Please set your OpenAI API Key here]")
                
                
                st.caption(":green[Your API is not stored anywhere. It is only used to generate answers to your questions.]")

                set_openAi_api_key(api_key_input)
def get_answer_csv(file: TextIO, query: str) -> str:
    """
    Returns the answer to the given query by querying a CSV file.

    Args:
    - file (str): the file path to the CSV file to query.
    - query (str): the question to ask the agent.

    Returns:
    - answer (str): the answer to the query from the CSV file.
    """
    # Load the CSV file as a Pandas dataframe
    df = pd.read_csv(file)
    #df = pd.read_csv("titanic.csv")

    # Create an agent using OpenAI and the Pandas dataframe
    #agent = create_csv_agent(OpenAI(temperature=0), file, verbose=False)
    agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=False)

    # Run the agent on the given query and return the answer
    #query = "whats the square root of the average age?"
    answer = agent.run(query)
    return answer
openai_api_insert_component()
os.environ['OPENAI_API_KEY'] = st.session_state['OPENAI_API_KEY']
st.header("MKG: Your CSV Specialist Buddy")
uploaded_file = st.file_uploader("Please Upload a csv file", type=["csv"])

if uploaded_file is not None:
    query = st.text_input("Ask any question related to the document")
    button = st.button("Submit")
    if button:
        st.write(get_answer_csv(uploaded_file, query))
