# -*- coding: utf-8 -*-
"""QA System.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wuYtpU1NCve2D2HvO1GLOQSmlCTugfAe
"""

!pip install comet-llm

!pip install torch

import torch

import comet_llm

!pip install transformers

from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# Function to load model and tokenizer
def load_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    return tokenizer, model

# Configure the model and tokenizer using DistilBERT
MODEL_NAME = "bert-large-uncased-whole-word-masking-finetuned-squad"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForQuestionAnswering.from_pretrained(MODEL_NAME)

def answer_question(question, context):
    # Tokenize the input
    inputs = tokenizer(question, context, return_tensors='pt')

    # Get the model's predictions
    outputs = model(**inputs)

    # Decode the model's output to get the answer
    answer_start = torch.argmax(outputs.start_logits) # Find the start of the answer
    answer_end = torch.argmax(outputs.end_logits) + 1 # Find the end of the answer
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end]))

    # Calculate confidence scores for the start and end tokens
    start_confidence = torch.max(outputs.start_logits).item()
    end_confidence = torch.max(outputs.end_logits).item()


    # Log the prompt and output to Comet LLM
    comet_llm.log_prompt(
        prompt=f"Question: {question}\nContext: {context}",
        output=answer,
        workspace="koded-ii",
        project="My-QA System",
        metadata={
            "model": MODEL_NAME,
            "api_key": "",
            "start_confidence": start_confidence,
            "end_confidence": end_confidence
        }
    )
    return answer

# Example questions and contexts
questions_and_contexts = [
    {
        "context": "Comet LLMs are a type of large language model designed for various tasks, including code understanding, research exploration, and knowledge retrieval.",
        "question": "What tasks are Comet LLMs designed for?"
    },
    {
        "context": "Donald Trump was a President",
        "question": "Who was Donald Trump?"
    },

]

# Process each question and context
for item in questions_and_contexts:
    context = item["context"]
    question = item["question"]
    answer = answer_question(question, context)
    print(f"Question: {question}\nAnswer: {answer}\n")