import base64
import json
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
vertex = Vertex(PROJECT, GCP_LOCATION, MODEL_NAME, app.logger)
app.logger.info(f"vertex agent created, ready for requests!")


@app.route("/chat", methods=["POST"])
def chat():
    app.logger.info("running inference")
    raw_payload = request.files.get("payload")
    payload = json.loads(raw_payload.read())
    prompt = payload["prompt"]
    temperature = payload["temperature"]
    tools = payload["tools"]
    pdfs = []
    for form_field_name, file in request.files.items():
        if form_field_name != "payload":
            pdfs.append(base64.b64encode(file.read()).decode("utf-8"))
    result = vertex.chat_message(prompt, pdfs, temperature, tools)
    app.logger.info("finished running inference")
    return {"result": result}, 200
