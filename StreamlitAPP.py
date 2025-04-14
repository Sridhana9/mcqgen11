import streamlit as st
import os
from dotenv import load_dotenv
import json
from src.mcqgenerator.utils import read_file
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

# Load .env variables
load_dotenv()
st.set_page_config(page_title="MCQs Creator", layout="centered")

st.title("🦜📚 MCQs Creator with Mistral + LangChain")
st.markdown("---")

# Sidebar: Input controls
st.sidebar.title("📄 Input Configuration")
uploaded_file = st.sidebar.file_uploader("Upload a PDF or TXT file", type=['pdf', 'txt'])
num_mcqs = st.sidebar.number_input("Number of MCQs", min_value=1, max_value=20, step=1, value=5)
subject = st.sidebar.text_input("Subject", value="Biology")
tone = st.sidebar.selectbox("Tone of Questions", ["simple", "medium", "difficult"], index=0)

# Main panel logic
if uploaded_file is not None:
    file_text = read_file(uploaded_file)

    st.subheader("📜 Extracted Text")
    st.write(file_text[:1000] + "..." if len(file_text) > 1000 else file_text)

    if st.button("✨ Generate MCQs"):
        with st.spinner("Generating MCQs with Mistral..."):
            try:
                # Define the expected JSON format for MCQs
                response_json_format = """
{
  "1": {
    "mcq": "multiple choice question",
    "options": {
      "a": "choice here",
      "b": "choice here",
      "c": "choice here",
      "d": "choice here"
    },
    "correct": "correct answer"
  }
}
"""

                # Use .invoke() instead of .run() to handle multiple outputs
                result = generate_evaluate_chain.invoke({
                    "text": file_text,
                    "number": num_mcqs,
                    "subject": subject,
                    "tone": tone,
                    "response_json": response_json_format
                })

                # Display generated quiz
                st.subheader("📝 Generated MCQs")
                try:
                    quiz = json.loads(result["quiz"])
                    for q_id, q_data in quiz.items():
                        st.markdown(f"**Q{q_id}. {q_data['mcq']}**")
                        for opt_key, opt_val in q_data['options'].items():
                            st.markdown(f"- ({opt_key.upper()}) {opt_val}")
                        st.markdown(f"✅ **Correct Answer:** {q_data['correct']}")
                        st.markdown("---")
                except Exception as e:
                    st.error("❌ Could not parse the quiz JSON. Showing raw text instead:")
                    st.code(result["quiz"])

                # Display review section
                st.subheader("🧠 Expert Review")
                st.success(result["review"])

            except Exception as e:
                st.error("❌ Error while generating MCQs:")
                st.exception(e)
else:
    st.info("👈 Upload a file to get started.")
