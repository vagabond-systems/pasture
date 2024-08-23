import logging
import os

from flask import Flask, request

from vertex import Vertex

app = Flask(__name__)

if __name__ == "entrypoint":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
app.logger.setLevel(logging.INFO)

PROJECT = os.getenv("PROJECT")
app.logger.info(f"using project from env var: {PROJECT}")
GCP_LOCATION = os.getenv("GCP_LOCATION")
app.logger.info(f"using gcp location from env var: {GCP_LOCATION}")
MODEL_NAME = os.getenv("MODEL_NAME")
app.logger.info(f"using model name from env var: {MODEL_NAME}")
vertex = None
app.logger.info(f"polygon booted, ready for requests!")


@app.route("/initialize", methods=["POST"])
def initialize():
    payload = request.json
    system_instructions = payload.get("system_instructions", None)
    global vertex
    vertex = Vertex(PROJECT, GCP_LOCATION, MODEL_NAME, app.logger, system_instructions)
    app.logger.info(f"vertex agent initialized, ready for inference!")
    return {}, 200


@app.route("/chat", methods=["POST"])
def chat():
    app.logger.info("running inference")
    payload = request.json
    prompt = payload["prompt"]
    temperature = payload.get("temperature", 1.0)
    tools = payload.get("tools", None)
    file_uris = payload.get("file_uris", None)
    response_schema = payload.get("response_schema", None)
    result = vertex.chat_message(prompt,
                                 temperature=temperature,
                                 tools=tools,
                                 file_uris=file_uris,
                                 response_schema=response_schema)
    app.logger.info("finished running inference")
    return {"result": result}, 200
