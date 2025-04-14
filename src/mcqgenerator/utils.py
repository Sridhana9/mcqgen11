import os
import re
import json
import PyPDF2

def clean_text(text):
    return re.sub(r'\[\d+\]', '', text)

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return clean_text(text)
        except Exception:
            raise Exception("Error reading the PDF file.")
    elif file.name.endswith(".txt"):
        raw_text = file.read().decode("utf-8")
        return clean_text(raw_text)
    else:
        raise Exception("Unsupported file format. Only PDF and TXT files are supported.")

def get_table_data(quiz_str):
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [f"{k}: {v}" for k, v in value["options"].items()]
            )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Options": options, "Correct": correct})

        return quiz_table_data

    except Exception as e:
        return [{"MCQ": "Error", "Options": str(e), "Correct": "N/A"}]
