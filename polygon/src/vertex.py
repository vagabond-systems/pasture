import mimetypes
import os

import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig, Tool, grounding


class Vertex:
    def __init__(self, project, gcp_location, model_name, logger):
        self.logger = logger
        self.logger.info(f"creating new Vertex agent")
        vertexai.init(project=project, location=gcp_location)
        self.model = GenerativeModel(
            model_name=model_name,
            system_instruction=[]
        )
        self.chat = self.model.start_chat()

    def chat_message(self, prompt, temperature=1.0, tools=None, file_uris=None, response_schema=None):
        self.logger.info(f"Vertex agent received generate request")
        prompt_parts = [prompt]

        active_tools = []
        if tools is not None:
            if "google_search" in tools:
                active_tools.append(Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval()))

        if file_uris is not None:
            for file_uri in file_uris:
                file_extension = os.path.splitext(file_uri)[1].lower()
                mimetype = mimetypes.types_map[file_extension]
                data_part = Part.from_uri(file_uri, mime_type=mimetype)
                prompt_parts.append(data_part)

        if response_schema is None:
            generation_config = GenerationConfig(
                temperature=temperature)
        else:
            generation_config = GenerationConfig(
                temperature=temperature,
                response_mime_type="application/json",
                response_schema=response_schema
            )

        stream = self.chat.send_message(
            prompt_parts,
            generation_config=generation_config,
            tools=active_tools,
            stream=True)
        result_chunks = []
        for chunk in stream:
            try:
                result_chunks.append(chunk.text)
            except Exception as error:
                break
        result = "".join(result_chunks)
        return result
