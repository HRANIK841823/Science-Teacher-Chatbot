import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)
from chatbot import run_chatbot

load_dotenv()


#================================
# Header
#================================
st.header("Science Teacher Chatbot")


#================================
# Create the chat history only once
#================================


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


#================================
# Display previous messages
#================================


for message in st.session_state.chat_history:

    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)

    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)

#================================  
# Sidebar
#================================  

with st.sidebar:
    st.subheader("Science Tutor Chatbot")
    st.subheader("Topics:")
    st.markdown("""
    - Physics
    - Chemistry
    - Biology
    - Mathematics

  """)

    st.divider()

    st.subheader("Chat History")
    messages=[
        message
        for message in st.session_state.chat_history
        if isinstance(message,(HumanMessage,AIMessage)) 
         
    ]
    if not messages:
        st.caption("No Conversation Yet")
    else:
        for message in st.session_state.chat_history:
            if isinstance(message,HumanMessage):
                with st.chat_message("User"):
                   st.write(message.content)
            
            if isinstance(message,AIMessage):
                with st.chat_message("assistant"):    
                   st.write(message.content)
    #================================            
    # Clear Chat
    #================================

    if st.button("Clear Chat",use_container_width=True):
        st.session_state.chat_history=[]
        st.rerun()



#================================            
#Take User input
#================================


user_input=st.chat_input("Type Your Question")

if user_input:
    if user_input.strip().lower()=="exit":
        st.stop()


    #================================
    #Store the user message
    #================================
    st.session_state.chat_history.append(HumanMessage(content=user_input))



    #================================
    #disply the user message
    #================================
    with st.chat_message("user"):
        st.write(user_input)


    #================================
    #Model Input
    #================================
    
    result=run_chatbot(user_input)
    answer=result['answer']
    subject=result['subject']
    previous_knowledge = result.get("previous_knowledge",[])

    
    #================================
    #Chat History Text
    #================================
    
    history_text = f"**Definition:** {answer.definition}\n\n**Explanation:** {answer.explanation}"
    st.session_state.chat_history.append(AIMessage(content=history_text))

    #================================
    #Output
    #================================

    with st.chat_message("assistant"):
        
       st.markdown('### Definition')
       st.markdown(answer.definition)


       st.markdown('### Explanation')
       st.markdown(answer.explanation)


       st.markdown('### Formula')
       st.markdown(answer.formula)

       st.markdown('### Example')
       st.markdown(answer.example)


       st.markdown('### Common Mistakes')
       for index, mistake in enumerate(answer.common_mistake,start=1):
           st.write(f"{index}. {mistake}")


       st.markdown("### Confidence")
       st.markdown(answer.confidence)


       st.markdown('### Required Knowledge')
       for index,topic in enumerate(previous_knowledge.topic,start=1):
           st.write(f"{index}. {topic}")
           