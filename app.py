# -*- coding: utf-8 -*-
"""AI Services for Hiring.ipynb
"""

#pip install google-generativeai

#pip install streamlit

#pip install google-generativeai streamlit

import os
import json
import google.generativeai as genai

genai.configure(api_key="AIzaSyB2j0Sd5ekAdiaOlcOV7-sGKsJ2FHFis-Y")

#Core AI Service Code

# --- Service 1: Job/CV Parsing to Generate Embeddings --- "Job Description Parsing" and "CV Parsing" services that generate "Embeddings". These embeddings are numerical representations
# of the text, perfect for similarity searches in a Vector DB.

def generate_text_embedding(text_content: str, task: str = "RETRIEVAL_DOCUMENT") -> list[float]:

  def generate_text_embedding(text_content: str, task: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    """
    Generates a text embedding for a given piece of text.

    Args:
        text_content: The text from the job description or CV.
        task: The intended task for the embedding. [10, 15]
              'RETRIEVAL_DOCUMENT' is for documents to be stored and searched.
              'RETRIEVAL_QUERY' would be for a search query itself.

    Returns:
        A list of floating-point numbers representing the embedding.
    """
    try:
        # We use the 'gemini-embedding-001' model, which is powerful for creating
        # high-quality embeddings for retrieval tasks. [3, 5]
        result = genai.embed_content(
            model="models/embedding-001",
            content=text_content,
            task_type=task
        )
        return result['embedding']
    except Exception as e:
        print(f"An error occurred during embedding generation: {e}")
        return []


# --- Service 2: Assessment Generation (GenAI) ---
# Your diagram shows an "Assessment Generation (GenAI)" service.
# We can use the Gemini Pro model to create relevant questions based
# on a job description.

def generate_assessment_questions(job_description: str, num_questions: int = 5) -> str:
    """
    Generates assessment questions based on a job description.

    Args:
        job_description: The full text of the job description.
        num_questions: The number of questions to generate.

    Returns:
        A string containing the generated questions.
    """
    #model = genai.GenerativeModel('gemini-pro')
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    prompt = f"""
    Based on the following job description, please generate {num_questions} relevant and insightful assessment questions for a candidate.
    The questions should evaluate both technical skills and soft skills mentioned in the description.

    --- Job Description ---
    {job_description}
    --- End of Job Description ---

    Please provide the questions in a clear, numbered list.
    """
    try:
        # The generate_content method sends the prompt to the model. [4, 6]
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during question generation: {e}"


# --- Service 3: Automated Scoring Engine (GenAI) ---
# Your diagram includes an "Automated Scoring Engine". We can instruct Gemini
# to act as a technical recruiter, scoring a candidate's answers and providing
# a structured JSON response.

def score_assessment_answers(job_description: str, candidate_answers: str) -> dict:
    """
    Scores a candidate's assessment answers against a job description.

    Args:
        job_description: The job description the candidate was assessed for.
        candidate_answers: The candidate's answers to the assessment questions.

    Returns:
        A dictionary containing the score and rationale.
    """
    #model = genai.GenerativeModel('gemini-pro')
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    # This is a sophisticated prompt that instructs the model to return a JSON object.
    # This makes the output predictable and easy to use in downstream applications. [12, 14, 17]
    prompt = f"""
    You are an expert technical recruiter and hiring manager. Your task is to evaluate a candidate's assessment answers based on the provided job description.
    Please provide a score from 1 (poor fit) to 10 (excellent fit) and a detailed rationale for your score.

    Analyze the candidate's answers for technical proficiency, problem-solving skills, and alignment with the company values implied in the job description.

    **Job Description:**
    ---
    {job_description}
    ---

    **Candidate's Answers:**
    ---
    {candidate_answers}
    ---

    Provide your evaluation in a valid JSON format with the following keys:
    - "overall_score": An integer between 1 and 10.
    - "summary": A brief one-sentence summary of the candidate's performance.
    - "strengths": A bulleted list of the candidate's strengths.
    - "weaknesses": A bulleted list of areas for improvement.
    - "final_recommendation": Your final recommendation (e.g., "Recommend for next round," "Proceed with caution," "Not a good fit").

    Do not include any text before or after the JSON object.
    """
    try:
        response = model.generate_content(prompt)
        # Clean up the response to ensure it's valid JSON
        cleaned_text = response.text.strip().lstrip("```json").rstrip("```")
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        return {"error": "Failed to parse the model's response as JSON.", "raw_response": response.text}
    except Exception as e:
        return {"error": f"An error occurred during scoring: {e}"}

genai.configure(api_key="AIzaSyB2j0Sd5ekAdiaOlcOV7-sGKsJ2FHFis-Y")

#This would help us know what models and call functions are available
import google.generativeai as genai
#genai.configure(API_KEY) amarachukwuemenike.2@gmail.com
genai.configure(API_KEY)


# models = genai.list_models()
# for model in models:
#     print(model.name, model.supported_generation_methods)


#proceed to read the documentation of RPM(request per minute), RPD(request per day) and TPM(token per minute) for each model here https://ai.google.dev/gemini-api/docs/rate-limits

import os
import json
import google.generativeai as genai

# --- Hardcode your API Key Here --- Replace "YOUR_API_KEY_HERE" with your actual Google AI Studio API key. For amarachukwuemenike.2@gmail.com
#  load_dotenv()
API_KEY = os.getenv("API_KEY") #plug in your API Key here
# YOUR_API_KEY_HERE = os.getenv("API_KEY")

API_KEY = os.getenv("API_KEY") 

# --- Configuration ---
if API_KEY == "YOUR_API_KEY_HERE":
    print("🔴 Error: Please replace 'YOUR_API_KEY_HERE' with your actual API key.")
else:
    try:
        genai.configure(api_key=API_KEY)
        print("✅ API Key configured successfully.")
    except Exception as e:
        print(f"An error occurred during configuration: {e}")


# ==============================================================================
#  STEP 2: DEFINE THE AI SERVICE FUNCTIONS
# ==============================================================================

def generate_text_embedding(text_content: str, task: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    """Generates a text embedding for a given piece of text."""
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text_content,
            task_type=task
        )
        return result.get('embedding', [])
    except Exception as e:
        print(f"An error occurred during embedding generation: {e}")
        return []

def generate_assessment_questions(job_description: str, num_questions: int = 5) -> str:
    """Generates assessment questions based on a job description."""
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        prompt = f"""
        Based on the following job description, please generate {num_questions} relevant assessment questions for a candidate.
        --- Job Description ---
        {job_description}
        --- End of Job Description ---
        Please provide the questions in a clear, numbered list.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during question generation: {e}"

def score_assessment_answers(job_description: str, candidate_answers: str) -> dict:
    """Scores a candidate's assessment answers against a job description."""
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        prompt = f"""
        You are an expert technical recruiter. Evaluate the candidate's answers based on the job description.
        Provide your evaluation in a valid JSON format with the keys: "overall_score" (1-10), "summary", "strengths", "weaknesses", and "final_recommendation".
        Do not include any text before or after the JSON object.

        **Job Description:**
        ---
        {job_description}
        ---

        **Candidate's Answers:**
        ---
        {candidate_answers}
        ---
        """
        response = model.generate_content(prompt)
        cleaned_text = response.text.strip().lstrip("```json").rstrip("```")
        return json.loads(cleaned_text)
    except Exception as e:
        # Provide a more detailed error message if possible
        raw_response = ""
        if hasattr(e, 'last_response'):
             raw_response = getattr(e, 'last_response').text
        return {"error": f"An error occurred during scoring: {e}", "raw_response": raw_response}

# ==============================================================================
#  STEP 3: RUN THE TESTS
# ==============================================================================

import streamlit as st
import google.generativeai as genai
import json

# ==============================================================================
#  STEP 1: CONFIGURATION
# ==============================================================================


# --- Configure the Google AI client ---
try:
    genai.configure(api_key=API_KEY)
    print("API Key configured successfully for Streamlit app.")
except Exception as e:
    # This error will show in the terminal where you run Streamlit
    print(f"An error occurred during configuration: {e}")


# ==============================================================================
#  STEP 2: DEFINE THE AI SERVICE FUNCTIONS
#  (These are now part of the Streamlit app itself)
# ==============================================================================

# To avoid re-running these functions on every interaction, we can use Streamlit's cache.
# This is optional but improves performance.
@st.cache_data
def generate_text_embedding(text_content: str, task: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    """Generates a text embedding for a given piece of text."""
    print("Generating embedding for:", text_content[:30] + "...") # Log to terminal
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text_content,
            task_type=task
        )
        return result.get('embedding', [])
    except Exception as e:
        st.error(f"An error occurred during embedding generation: {e}")
        return []

@st.cache_data
def generate_assessment_questions(job_description: str, num_questions: int = 5) -> str:
    """Generates assessment questions based on a job description."""
    print("Generating assessment questions...") # Log to terminal
    try:
        model = genai.GenerativeModel('gemini-1.0-pro')
        prompt = f"""
        Based on the following job description, please generate {num_questions} relevant assessment questions for a candidate.
        --- Job Description ---
        {job_description}
        --- End of Job Description ---
        Please provide the questions in a clear, numbered list.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred during question generation: {e}")
        return "An error occurred. Please check the terminal for more details."

@st.cache_data
def score_assessment_answers(job_description: str, candidate_answers: str) -> dict:
    """Scores a candidate's assessment answers against a job description."""
    print("Scoring candidate answers...") # Log to terminal
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        prompt = f"""
        You are an expert technical recruiter. Evaluate the candidate's answers based on the job description.
        Provide your evaluation in a valid JSON format with the keys: "overall_score" (1-10), "summary", "strengths", "weaknesses", and "final_recommendation".
        Do not include any text before or after the JSON object.

        **Job Description:**
        ---
        {job_description}
        ---

        **Candidate's Answers:**
        ---
        {candidate_answers}
        ---
        """
        response = model.generate_content(prompt)
        cleaned_text = response.text.strip().lstrip("```json").rstrip("```")
        return json.loads(cleaned_text)
    except Exception as e:
        st.error(f"An error occurred during scoring: {e}")
        return {"error": "An error occurred. Please check the terminal for more details."}

# ==============================================================================
#  STEP 3: BUILD THE STREAMLIT USER INTERFACE
# ==============================================================================

# --- Page Configuration ---
st.set_page_config(
    page_title="Recruitment AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Services For Hiring")
st.caption("Created by Precious Emenike")

# --- Custom CSS for Professional Landing Page Look ---
st.markdown("""
<style>
    /* Define CSS Variables for easy color changes */
    :root {
        --primary-color: #4A90E2; /* A professional blue */
        --background-color: #0D1B3E; /* Dark blue background */
        --text-color: #FFFFFF;
        --form-background: #FFFFFF;
        --form-text-color: #0D1B3E;
    }

    /* Remove Streamlit's default padding on the main block */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }

    /* Main app background with gradient */
    .stApp {
        background: linear-gradient(135deg, #0D1B3E 0%, #243B55 100%);
    }

    /* Main content text color */
    .stApp, .stApp h1, .stApp h2, .stApp h3, .stApp p {
        color: var(--text-color);
    }
    
    /* Left Column (Main Title & Text) Styling */
    .main-title {
        font-size: 3.5em;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }
    .main-subtitle {
        font-size: 1.2em;
        font-weight: 300;
        margin-bottom: 2rem;
        color: rgba(255, 255, 255, 0.8);
    }

    /* Right Column (Form) Styling */
    .form-container {
        background-color: var(--form-background);
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .form-container h2 {
        color: var(--form-text-color);
        font-weight: 600;
        margin-bottom: 1.5rem;
        text-align: center;
    }

    /* Input widget styling */
    .stTextInput input, .stTextArea textarea {
        background-color: #F0F2F6;
        border: 1px solid #DAE1E7;
        border-radius: 8px;
        color: var(--form-text-color);
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: none;
        background-color: var(--primary-color);
        color: white;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #357ABD; /* A slightly darker blue on hover */
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.4);
    }

</style>
""", unsafe_allow_html=True)

# --- Check for API Key ---
if API_KEY == "YOUR_API_KEY_HERE":
    st.error("🔴 Please replace 'YOUR_API_KEY_HERE' in the script with your actual API key.")
    st.stop() # Stop the app from running further

# --- UI Layout ---
# Use tabs to represent each AI service from your diagram
tab1, tab2 = st.tabs([
    "📝 Assessment Generator",
    "📊 Automated Scorer"
    #"🔍 Embedding Generator"
])


# --- Tab 1: Assessment Generator ---
with tab1:
    st.header("Generate Candidate Assessment Questions")
    st.markdown("Paste a job description below to automatically generate relevant interview questions.")
    jd_for_questions = st.text_area("Job Description for Question Generation", height=250, key="jd_questions")
    if st.button("Generate Questions"):
        if jd_for_questions:
            with st.spinner("Thinking up some insightful questions..."):
                # Direct call to the function defined above
                questions = generate_assessment_questions(jd_for_questions)
                st.markdown(questions)
        else:
            st.warning("Please paste a job description first.")


# --- Tab 2: Automated Scorer ---
with tab2:
    st.header("Automatically Score Candidate Answers")
    st.markdown("Provide the job description and the candidate's answers to get an AI-powered evaluation.")
    col1, col2 = st.columns(2)
    with col1:
        jd_for_scoring = st.text_area("Job Description for Scoring", height=300, key="jd_scoring")
    with col2:
        answers_for_scoring = st.text_area("Candidate's Answers", height=300, key="answers_scoring")

    if st.button("Evaluate Candidate"):
        if jd_for_scoring and answers_for_scoring:
            with st.spinner("Reading answers and evaluating fit..."):
                # Direct call to the function defined above
                score_data = score_assessment_answers(jd_for_scoring, answers_for_scoring)
                if "error" in score_data:
                    st.error(f"An error occurred: {score_data['error']}")
                else:
                    st.subheader(f"Overall Score: {score_data.get('overall_score', 'N/A')} / 10")
                    st.markdown(f"**Recommendation:** {score_data.get('final_recommendation', 'N/A')}")
                    # Use st.json to nicely format the dictionary output
                    st.json(score_data)
        else:
            st.warning("Please provide both the job description and the answers.")


# # --- Tab 3: Embedding Generator ---
# with tab3:
#     st.header("Generate Text Embeddings")
#     st.markdown("This tool converts text (from a CV or job description) into a numerical vector for similarity matching.")
#     text_for_embedding = st.text_area("Paste Job Description or CV Text Here", height=250, key="text_embedding")
#     if st.button("Generate Embedding Vector"):
#         if text_for_embedding:
#             with st.spinner("Converting text to vector..."):
#                 # Direct call to the function defined above
#                 embedding = generate_text_embedding(text_for_embedding)
#                 if embedding:
#                     st.success("Successfully generated embedding!")
#                     st.info(f"Vector Dimensions: {len(embedding)}")
#                     st.text_area("Generated Vector (first 100 dimensions)", value=str(embedding[:100]) + "...", height=150)
#         else:
#             st.warning("Please paste some text to generate an embedding.")

