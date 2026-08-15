


'''

What is Langchain  : Langchain is opensource Python framework designed to help developers to huild applications
                     using large language models .. 

Prompt Template    : It is a resuable prompt in which we can put in dynamic variables like
                     prompt = "Classify the following requirement : {message}"

Output Parser      : A tool in langchain that takes raw text output from llm and converts it into clean text
                     or a python dictionary or a specific string or boolean if required

Routing /Branching : When we take output from one prompt and dynamically send another input prompt corresponding
                     to that output

''' 

import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# when llm returns output , it gives complex ai message OBJECT , to convert it into a string we need 
# strOutputParser for string output cleaned to showcase in terminal 
from langchain_core.output_parsers import StrOutputParser

# RunnableLambda turns python functions to Langchain compatible steps
# so that they can be easily integrable in modern langchain pipelines
from langchain_core.runnables import RunnableLambda

# loading env file for api key 
# currently google gemini 

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key :
    print("API_KEY loading error , please check")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=api_key,
    temperature=0.0 #for most probable outcome to showcase , we dont llm to be creative for long output
)

#----------------------
# Classification Prompt
# ---------------------
classification_prompt = PromptTemplate.from_template(
    """You are an issue triage assistant. Analyze the incoming user message and classify it into EXACTLY ONE of the following four categories:
- bug_report : something in the software is broken or behaving incorrectly
- feature_request : a suggestion for new or improved functionality
- documentation_issue : the docs/README/guide are missing, unclear, or incorrect
- question : a general how-do-I / clarification question that isn't a bug or a request

Return ONLY the category name in lowercase without any punctuation, explanations, or extra text.

User message:
{message}

Category:"""
)

classifier_chain = classification_prompt | llm | StrOutputParser()
# classifier chain is made using pipe ( | ) operator .
# they are steps in the chain
# first prompt of classification -> llm gives ai message object output back -> parsert converts to string



#---------------------------
# CATEGORY SPECIFIC PROMPTS
#---------------------------

# Prompt template 1: Used when an issue is classified as a 'bug_report'
bug_prompt = PromptTemplate.from_template(
    """You are a helpful software support assistant.
The user reported a bug:
"{message}"

Write a professional and polite first reply:
1. Acknowledge the bug.
2. Ask for reproduction steps, environment/version details (OS, browser, app version), and expected vs. actual behavior if not already provided.
"""
)

# Prompt template 2: Used when an issue is classified as a 'feature_request'
feature_prompt = PromptTemplate.from_template(
    """You are a helpful software product assistant.
The user submitted a feature request:
"{message}"

Write a professional and polite first reply:
1. Thank the user for the suggestion.
2. Ask what specific problem this feature would solve or how they envision using it.
3. Note that their request will be reviewed and considered by the product team.
"""
)

# Prompt template 3: Used when an issue is classified as a 'documentation_issue'
docs_prompt = PromptTemplate.from_template(
    """You are a helpful documentation support assistant.
The user reported an issue with documentation:
"{message}"

Write a professional and polite first reply:
1. Acknowledge the documentation gap or confusion.
2. Ask which specific page, guide, or section was unclear.
3. Thank them for helping improve the documentation.
"""
)

# Prompt template 4: Used when an issue is classified as a general 'question'
question_prompt = PromptTemplate.from_template(
    """You are a knowledgeable technical support assistant.
The user asked a question:
"{message}"

Write a helpful and direct reply:
1. Answer the question directly and clearly if possible.
2. If more context is needed, politely guide them on where to look or what additional information to provide.
"""
)


# Now we are in loop 2 
# WE NEED TO CREATE SUBCHAINS FOR EACH SPECIFIC ANSWER 

bug_chain  = bug_prompt | llm | StrOutputParser()
feature_chain = feature_prompt | llm | StrOutputParser()
docs_chain = docs_prompt | llm | StrOutputParser()
question_chain = question_prompt | llm | StrOutputParser()


# ----------------
# ROUTER FUNCTION
#-----------------

def route_and_generate(data: dict) -> str:
    """
    This function takes a dictionary containing the classified category and original message.
    It inspects the category and routes the request to the appropriate sub-chain.
    """
    # Clean up the category text: strip leading/trailing spaces and convert to lowercase
    category = data["category"].strip().lower()
    # Extract the original user message text
    message = data["message"]
    
    # Check which category was detected and call .invoke() on the matching chain
    # .invoke() runs the entire chain and returns the final string
    if "bug_report" in category:
        return bug_chain.invoke({"message": message})
    elif "feature_request" in category:
        return feature_chain.invoke({"message": message})
    elif "documentation_issue" in category:
        return docs_chain.invoke({"message": message})
    else:
        # Fallback to the general question chain for anything else
        return question_chain.invoke({"message": message})


#------------------
# FULL PIPELINE 
#------------------


def process_issue(message: str):
    """
    Takes a raw user message, runs classification, routes it to draft a reply,
    and prints formatted results directly to the terminal.
    """
    # Run the classifier chain to determine what kind of issue this is
    raw_category = classifier_chain.invoke({"message": message})
    # Clean up the returned string (removing whitespace/newlines)
    clean_category = raw_category.strip().lower()
    
    # 2. Pass both the classification result and the original message to our router
    reply = route_and_generate({"category": clean_category, "message": message})
    
    # 3. Print the results clearly to the terminal for easy inspection and screenshots
    print("=" * 70)
    print(f"INPUT MESSAGE:\n{message}")
    print("-" * 70)
    print(f"CLASSIFICATION RESULT: {clean_category}")
    print("-" * 70)
    print(f"GENERATED REPLY:\n{reply}")
    print("=" * 70 + "\n")




#--------------
# CODE EXECUTED
#--------------

if __name__ == "__main__":
    # List of 4 distinct test inputs representing each target category
    test_cases = [
        # 1. Bug Report
        "When I click on the 'Export to PDF' button, the application crashes with a 500 internal server error.",
        
        # 2. Feature Request
        "It would be great to have dark mode support and a shortcut to toggle between themes.",
        
        # 3. Documentation Issue
        "The installation instructions in the README are missing the step to install libssl-dev on Ubuntu.",
        
        # 4. Question
        "How do I reset my account password if I don't have access to my registered recovery phone?"
    ]
    
    # Iterate through each test message and run the complete triage workflow
    for idx, test_msg in enumerate(test_cases, start=1):
        print(f">>> TEST CASE {idx} <<<")
        process_issue(test_msg)
        time.sleep(15)

