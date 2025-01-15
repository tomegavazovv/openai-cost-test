import openai
from openai import OpenAI
import tiktoken
import os
from dotenv import load_dotenv
from open_ai_pricing import OPENAI_PRICING
import json
import streamlit as st
# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

st.set_page_config(page_title="Prompt Tester", layout="wide")

def get_token_cost(input_tokens, output_tokens, model="gpt-3.5-turbo"):
    if model not in OPENAI_PRICING:
        raise ValueError(f"Pricing not available for model: {model}. Available models: {', '.join(OPENAI_PRICING.keys())}")
    
    pricing = OPENAI_PRICING[model]
    input_cost = (input_tokens / 1000) * pricing["input"]
    output_cost = (output_tokens / 1000) * pricing["output"]
    total_cost = input_cost + output_cost
    
    return total_cost, input_cost, output_cost

def format_cost(cost):
    """Format cost in dollars"""
    return f"${cost:.4f}"

def estimate_tokens(text, model="gpt-3.5-turbo"):
    """Estimate the number of tokens in a text using tiktoken"""
    encoding = tiktoken.encoding_for_model(model)
    
    return len(encoding.encode(text))

def test_prompt(prompt, model="gpt-3.5-turbo"):
    """Test a prompt and get token usage with costs"""
    # Get the appropriate mode for the selected model
    mode = OPENAI_PRICING[model]["mode"]
    
    # Adjust system message based on mode
    if mode == "json":
        system_message = "You will receive a prompt to evaluate. Respond with a JSON object containing a 'score' field (0-100) and a 'reasoning' field (one sentence, max 150 chars) explaining the score."
    else:
        system_message = "You will receive a prompt to evaluate. Respond with a score from 0-100 and a one sentence reasoning (max 250 chars)."
    
    # Base message structure
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    
    # Configure the API call based on the mode
    if mode == "json":
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={ "type": "json_object" },
        )
        content = json.loads(response.choices[0].message.content)
        score = content["score"]
        reasoning = content["reasoning"]
    else:  # function mode
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            functions=[{
                "name": "get_score",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "number",
                            "description": "The score from 0-100"
                        },
                        "reasoning": {
                            "type": "string",
                            "description": "One sentence explanation for the score (max 250 chars)"
                        }
                    },
                    "required": ["score", "reasoning"]
                }
            }],
            function_call={"name": "get_score"}
        )
        content = json.loads(response.choices[0].message.function_call.arguments)
        score = content["score"]
        reasoning = content["reasoning"]
    
    total_cost, input_cost, output_cost = get_token_cost(
        response.usage.prompt_tokens,
        response.usage.completion_tokens,
        model
    )
    
    return {
        "prompt": prompt,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
        "score": score,
        "reasoning": reasoning
    }

# Example usage
if __name__ == "__main__":
    st.title("AI Prompt Tester")
    
    # Create input area
    prompt = st.text_area("Enter your prompt:", height=200)
    
    # Add a model selector with all available non-embedding models
    available_models = [model for model in OPENAI_PRICING.keys()]
    model = st.selectbox("Select model:", available_models)
    
    if st.button("Test Prompt"):
        if prompt:
            with st.spinner("Testing prompt..."):
                result = test_prompt(prompt, model=model)
                
            # Display results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score", f"{result['score']}/100")
                st.write("Reasoning:", result['reasoning'])
            with col2:
                st.metric("Total Tokens", result['total_tokens'])
            with col3:
                st.metric("Cost", format_cost(result['total_cost']))
