from openai import OpenAI
from dotenv import load_dotenv
from requests.exceptions import HTTPError
import os
import json

# Load env variables
load_dotenv()



# Specify the JSON schema's the AI model should follow in its response
JSON_SCHEMAS = {
    "story_collection": {
        "title": "string",
        "created": {
            "type": "string",
            "format": "date-time"
        },
        "updated": {
            "type": "string",
            "format": "date-time"
        },
        "author": "string",
        "story": "string",
        "summary": "string",
        "image_url": {
            "type": "string",
            "format": "uri"
        }
    },
    "url_collection": {
        "type": "array",
        "items": {
            "type": "string",
            "format": "uri"
        }
    }
    # Add more JSON schemas for other analysis types
}


def process_content_with_openai(setup_prompt, content, answer_format, schema):
    try:
        # Set up the OpenAI client
        client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )

        if not setup_prompt:
            setup_prompt = "You are a helpful assistant designed to output JSON. Your task is to process the given HTML content."

        if not answer_format:
            answer_format = "Please return the URLs to the news stories in a JSON array."

        # Call the OpenAI API
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": setup_prompt},
                    {"role": "system", "content": answer_format},
                    {"role": "system", "content": f"Please follow this schema: {json.dumps(schema)}"},
                    {"role": "user", "content": content}
                ]
            )
            print("response", response)
            content = response.choices[0].message.content
            if 'error' in json.loads(content):
                return None
            else:
                return content
        except HTTPError as e:
            print(f"An error occurred: {e}")
            return None
    except Exception:
        return None