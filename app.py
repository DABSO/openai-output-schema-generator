from schema_generation import generate_schema
from langchain.schema import HumanMessage, AIMessage
from dotenv import load_dotenv
import streamlit as st
import json
from datetime import datetime
import os

def init_app():
    load_dotenv()
    st.set_page_config(layout="wide")
    st.title("OpenAI Structured Output Schema Generator Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if not os.path.exists("generated_schemas"):
        os.makedirs("generated_schemas")

def save_schema(schema_data):
    schema_name = schema_data.get("name", "schema")
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_schemas/{schema_name}_{date_str}.json"
        
    with open(filename, "w") as f:
        json.dump(schema_data, f, indent=2)
        return filename

def display_message(message, index):
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    else:
        with st.chat_message("assistant"):
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                schema_data = json.loads(message.content)
                st.json(schema_data)
            with col2:
                if st.button("💾", key=f"save_{schema_data['name'] + str(index)}"):
                    filename = save_schema(schema_data)
                    st.toast(f"Schema saved as {filename}")

def handle_user_input(user_input):
    if user_input:
        human_message = HumanMessage(content=user_input)
        st.session_state.messages.append(human_message)
    
    output_schema = generate_schema(st.session_state.messages)
    ai_message = AIMessage(content=json.dumps(output_schema))
    st.session_state.messages.append(ai_message)
    st.rerun()

def main():
    init_app()
    
    # Display all messages
    for i, message in enumerate(st.session_state.messages):
        display_message(message, i)
    
    # Create the input area and handle input
    user_input = st.chat_input("Enter your message")
    if user_input or (st.session_state.messages and 
                     isinstance(st.session_state.messages[-1], HumanMessage)):
        handle_user_input(user_input)

if __name__ == "__main__":
    main()




