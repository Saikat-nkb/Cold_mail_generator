import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Chain:
    def __init__(self):
        # Try to get API key from multiple sources
        groq_api_key = self._get_api_key()

        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found. Please add it to your environment variables or Streamlit secrets.")

        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=groq_api_key,
            model_name="meta-llama/llama-4-scout-17b-16e-instruct"
        )

    def _get_api_key(self):
        """Get API key from environment variables or Streamlit secrets"""
        # Try to get from Streamlit secrets first
        try:
            return st.secrets["GROQ_API_KEY"]
        except (KeyError, AttributeError):
            # If not in Streamlit secrets, try environment variables
            return os.getenv("GROQ_API_KEY")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Saikat, a business development executive at XYZ COMPANY. XYZ COMPANY is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools.
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability,
            process optimization, cost reduction, and heightened overall efficiency.
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of XYZ COMPANY
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase XYZ COMPANY portfolio: {link_list}
            Remember you are Saikat, and your signature must be exactly formatted as:

            Saikat
            Business Development Executive
            XYZ COMPANY

            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
