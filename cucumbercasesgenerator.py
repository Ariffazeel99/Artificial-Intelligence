import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Environment variables from a .env file

# Set OpenAI API key here
openai.api_key = os.getenv('OPENAI_API_KEY') 

def read_prompt_from_file(file_path):
    """Reads the test case prompt from a text file."""
    with open(file_path, 'r') as file:
        return file.read()

def write_scenario_to_file(file_path, content):
    """Writes the generated scenario to a text file."""
    with open(file_path, 'w') as file:
        file.write(content)

def query_openai_chat_api(prompt):
    """Sends a prompt to the OpenAI API using the `v1/chat/completions` endpoint and returns the response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",  # Adjust this to the correct chat model you have access to
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150  # Set the maximum number of tokens to generate
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    prompt_file_path = '../data.txt'  # Adjust the path to the correct location
    output_file_path = '../output.txt'  # Adjust the path to the correct location
    
    # Read the test case data
    test_case_data = read_prompt_from_file(prompt_file_path)
    
    # Format the prompt with the test case data
    formatted_prompt = f"Convert the following test case into a Gherkin Cucumber scenario: {test_case_data} Please write the scenario in a way that includes background, scenario outline, and examples where appropriate."
    
    response = query_openai_chat_api(formatted_prompt)
    
    if response:
        # Extract the scenario text from the first choice's message content
        scenario_text = response['choices'][0]['message']['content']
        write_scenario_to_file(output_file_path, scenario_text)
        print(f"Generated Cucumber Scenario written to {output_file_path}")
    else:
        print("No response was returned from the API.")

if __name__ == '__main__':
    main()
