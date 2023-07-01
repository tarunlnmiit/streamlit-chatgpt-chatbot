import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI


def main():
    st.title("ChatGPT ChatBot🤖")
    st.markdown(
        ''' 
            > :black[**A ChatGPT based ChatBot 
            that remembers the context of the conversation.**]
            ''')

    API_KEY = st.text_input(":blue[Enter Your OpenAI API-KEY :]",
                            placeholder="Please enter your OpenAI API key here",
                            type="password")

    if API_KEY:
        st.write("API-KEY received.")

        MODEL = 'gpt-3.5-turbo'
        # An OpenAI instance
        llmObj = ChatOpenAI(openai_api_key=API_KEY,
                            model_name=MODEL)

        # A ConversationEntityMemory object
        K = 3  # number of user interactions as context
        if 'entity_memory' not in st.session_state:
            st.session_state.entity_memory = ConversationEntityMemory(
                llm=llmObj, k=K)

        # The ConversationChain object
        Conversation = ConversationChain(
            llm=llmObj,
            prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
            memory=st.session_state.entity_memory
        )
    else:
        st.markdown('''
            ```
            - 1. Please enter the API Key and hit enter.

            - 2. Start your conversation with the text input widget below.
            ```
            ''')
        st.warning(
            'You need to enter the API key to have a working app.')
        
    # Get the user input
    user_input = st.text_input("You: ", st.session_state["input"],
                                key="input",
                                placeholder="Your Chatbot friend! Ask away ...",
                                label_visibility='hidden')
    
    # Output using the ConversationChain object and the user input, 
    # and storing them in the session
    if user_input:
        output = Conversation.run(input=user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    # Display the conversation history using an expander
    with st.expander("Conversation", expanded=True):
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            st.info(st.session_state["past"][i], icon="🧐")
            st.success(st.session_state["generated"][i], icon="🤖")


if __name__ == '__main__':
    st.set_page_config(page_title='ChatGPT ChatBot🤖', layout='centered')

    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []
    if "input" not in st.session_state:
        st.session_state["input"] = ""

    main()
