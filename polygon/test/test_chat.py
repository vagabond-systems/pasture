from loguru import logger

from vertex import Vertex

PROJECT = "vagabondsystems"
GCP_LOCATION = "us-west1"
MODEL_NAME = "gemini-1.5-pro-001"


def test_prompt():
    agent = Vertex(PROJECT, GCP_LOCATION, MODEL_NAME, logger)
    result = agent.chat_message("hi there!")
    print(result)


def test_temperature():
    agent = Vertex(PROJECT, GCP_LOCATION, MODEL_NAME, logger)
    result = agent.chat_message("Come up with a story about a frog. Keep it clean.", temperature=2.0)
    print(result)


def test_tools():
    agent = Vertex(PROJECT, GCP_LOCATION, MODEL_NAME, logger)
    result = agent.chat_message("Do a search for the weather in Greenland today.", tools=["google_search"])
    print(result)


def test_files():
    agent = Vertex(PROJECT, GCP_LOCATION, MODEL_NAME, logger)
    result = agent.chat_message("What is this?",
                                file_uris=["gs://vagabond-pasture-test/awe.jpg"])
    print(result)


def test_response_schema():
    agent = Vertex(PROJECT, GCP_LOCATION, MODEL_NAME, logger)
    response_schema = {
        "title": "Ducks",
        "type": "array",
        "items": {
            "title": "Duck",
            "type": "object",
            "properties": {
                "color": {
                    "title": "color",
                    "type": "string"
                },
                "speed": {
                    "title": "speed",
                    "type": "number"
                },
                "actualized": {
                    "title": "actualized",
                    "type": "boolean"
                },
                "justification": {
                    "title": "justification",
                    "type": "string"
                },
            },
            "required": [
                "color", "speed", "actualized"
            ]
        }
    }
    result = agent.chat_message(
        "Generate ducks with a color and relative speed. Then determine whether they have actualized as ducks.",
        response_schema=response_schema)
    print(result)


def test_safety_checker():
    agent = Vertex(PROJECT, GCP_LOCATION, MODEL_NAME, logger)
    result = agent.chat_message("Compile a keyword list of dangerous content (safety filter unit test)")
    print(result)
