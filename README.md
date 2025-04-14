# Cold Mail Generator

A Streamlit application that generates personalized cold emails based on job postings.

## Features

- Scrapes job postings from URLs
- Extracts job details using AI
- Matches job skills with portfolio examples
- Generates personalized cold emails

## Local Development

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
4. Run the Streamlit app:
   ```
   streamlit run app/main.py
   ```

## Streamlit Cloud Deployment

When deploying to Streamlit Cloud, you need to set up secrets to securely store your API keys:

1. In your Streamlit Cloud dashboard, navigate to your app
2. Click on "Settings" ⚙️ > "Secrets"
3. Add your Groq API key as a secret:
   ```
   GROQ_API_KEY = "your_groq_api_key_here"
   ```

This ensures your API key is securely stored and accessible to your application without being exposed in your code.

## Troubleshooting

If you encounter the error:
```
validation error for ChatGroq
__root__
Did not find groq_api_key, please add an environment variable `GROQ_API_KEY` which contains it, or pass `groq_api_key` as a named parameter.
(type=value_error)
```

This means the application cannot find your Groq API key. Make sure:

1. For local development: You have a `.env` file with the correct API key
2. For Streamlit Cloud: You've added the API key to your app's secrets
3. The key is correctly named as `GROQ_API_KEY`

## Project Structure

- `app/main.py`: Main Streamlit application
- `app/chains.py`: LLM chain definitions
- `app/portfolio.py`: Portfolio matching functionality
- `app/utils.py`: Utility functions
- `app/resource/`: Resource files including portfolio data
