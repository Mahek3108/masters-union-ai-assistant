
import base64

import streamlit as st
from rag_Chatbot import generate_answer, general_answer
from course_config import COURSES
def detect_program_intent(query):

    program_keywords = [
        "program",
        "programme",
        "course",
        "curriculum",
        "fees",
        "duration",
        "eligibility",
        "ai",
        "data science",
        "marketing",
        "finance"
    ]

    q = query.lower()

    return any(word in q for word in program_keywords)
st.set_page_config(page_title="Masters Union AI Assistant")
st.markdown("""
<style>
.block-container{
background: rgba(255,255,255,0.15);
backdrop-filter: blur(8px);
padding:30px;
border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

#background

def add_bg_from_local(image_file):

    with open(image_file, "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}

        /* 60% dark overlay for readability */

        .stApp::before {{
            content: "";
            position: fixed;
            top:0;
            left:0;
            width:100%;
            height:100%;
            background: rgba(0,0,0,0.6);
            z-index:-1;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )



add_bg_from_local("background.jpeg")

st.title("🎓 Masters Union AI Assistant")

st.markdown(
"""
Hello 👋  

Welcome to **Masters Union AI Assistant**

How may I help you?
"""
)
#mode state

if "mode" not in st.session_state:
    st.session_state.mode = None

# BUTTONS


col1, col2 = st.columns(2)

with col1:
    if st.button("Course Query"):
        st.session_state.mode = "course"

with col2:
    if st.button("Others"):
        st.session_state.mode = "others"

# COURSE QUERY MODE


if st.session_state.mode == "course":

    category = st.selectbox(
        "Choose Level of Study",
        ["Choose Level of Study"] + list(COURSES.keys())
    )

    if category != "Choose Level of Study":

        course = st.selectbox(
            "Choose Programme",
            ["Choose Programme"] + COURSES[category]
        )

        if course != "Choose Programme":

            st.success(f"Great choice! 🎓 You selected **{course}**")

            st.write("What would you like to know about this programme?")

            user_question = st.chat_input("Ask your question")

            if user_question:

                with st.chat_message("user"):
                    st.write(user_question)

                answer, sources = generate_answer(
                    user_question,
                    course
                )

                with st.chat_message("assistant"):

                    st.write(answer)

                    if sources:
                        st.markdown("**Sources:**")
                        for s in sources:
                            st.write("-", s)


# OTHERS MODE


if st.session_state.mode == "others":

    st.write("Ask anything about Masters Union.")

    user_question = st.chat_input("Ask your question")

    if user_question:

        with st.chat_message("user"):
            st.write(user_question)

        q = user_question.lower()

        programme_keywords = [
            "program","programme","course","curriculum",
            "fees","duration","eligibility","ai",
            "data science","marketing","finance",
            "sports","management","pgp","ug"
        ]

        institute_keywords = [
            "masters union","institute","campus",
            "location","founder","faculty","about",
            "gurugram"
        ]

       
        # PROGRAMME QUESTION
        

        if any(word in q for word in programme_keywords):

            with st.chat_message("assistant"):

                st.warning(
                    "You're asking about a programme.\n\n"
                    "Please use **Course Query** above to explore programme details."
                )

        # INSTITUTE QUESTION
        

        elif any(word in q for word in institute_keywords):

            answer = general_answer(user_question)

            with st.chat_message("assistant"):
                st.write(answer)

        # UNKNOWN QUESTION
      

        else:

            with st.chat_message("assistant"):

                st.markdown(
                """
                I can help with information about **Masters Union** and its programmes.

                Please either:

                • Use **Course Query** above to explore programmes  
                • Contact us at **info@mastersunion.org**
                """
                )