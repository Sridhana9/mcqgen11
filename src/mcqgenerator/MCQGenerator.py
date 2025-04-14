import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.llms import HuggingFaceHub

# Load environment variables from the .env file
load_dotenv()
hf_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Load Mistral 7B Instruct from HuggingFace
llm = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.1",
    model_kwargs={"temperature": 0.7, "max_new_tokens": 1024},
    huggingfacehub_api_token=hf_key
)

# Prompt to generate MCQs
template = """
Text: {text}

You are an expert MCQ maker. Given the above text, create a quiz of {number} multiple choice questions for {subject} students in a {tone} tone.
Do not repeat any questions. All questions must be based on the provided text.
Ensure the following format exactly:
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template
)

quiz_chain = LLMChain(
    llm=llm,
    prompt=quiz_generation_prompt,
    output_key="quiz",
    verbose=True
)

# Prompt to evaluate and revise the quiz
template2 = """
You are an expert English grammarian and writer. Given a multiple choice quiz for {subject} students, evaluate its complexity and tone.
Write a brief (max 50 words) complexity analysis. If any question is too hard or too easy, revise it to match the students' cognitive level.

Quiz_MCQs:
{quiz}

Evaluation and suggestions from expert:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=template2
)

review_chain = LLMChain(
    llm=llm,
    prompt=quiz_evaluation_prompt,
    output_key="review",
    verbose=True
)

# Full pipeline chain
generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True
)
