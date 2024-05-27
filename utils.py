from openai import OpenAI
from dotenv import load_dotenv
import base64
import json
import sys

load_dotenv()
client = OpenAI()

def get_result_from_image(image_path):
    with open(image_path, "rb") as image:
        base64_image = base64.b64encode(image.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """You are an expert in identifying objects in images. A user sends you an image, and you describe what it is. Use the following JSON format:

{
    "description": "general description of the image",
    "items": [
        {
            "name": "name of the item",
            "details": "details about the item"
        }
    ],
    "overall_explanation": "overall explanation of the image"
}"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Explain the image provided?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            },
        ],
    )

    response_message = response.choices[0].message
    content = response_message.content
    return json.loads(content)

if __name__ == "__main__":
    image_path = sys.argv[1]
    result = get_result_from_image(image_path)
    print(json.dumps(result, indent=4))
