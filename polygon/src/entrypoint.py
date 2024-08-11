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

BUCKET_NAME = os.getenv("BUCKET_NAME")
app.logger.info(f"using bucket name from env var: {BUCKET_NAME}")
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
    payload = request.json
    prompt = payload["prompt"]
    selected_files = payload["selected_files"]
    temperature = payload["temperature"]
    tools = payload["tools"]
    file_urls = [f"gs://{BUCKET_NAME}/{file_name}" for file_name in selected_files]
    response = vertex.chat_message(prompt, file_urls, temperature, tools)
    app.logger.info("finished running inference")
    return {"response": response}, 200
