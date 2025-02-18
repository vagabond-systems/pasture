import mimetypes
import os

import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig, Tool, grounding, SafetySetting, \
    HarmCategory, HarmBlockThreshold


class Vertex:
    def __init__(self, project, gcp_location, model_name, logger, system_instructions=None):
        self.logger = logger
        self.logger.info(f"creating new Vertex agent with system instructions: {system_instructions}")
        vertexai.init(project=project, location=gcp_location)
        if system_instructions is None:
            system_instructions = []
        self.model = GenerativeModel(
            model_name=model_name,
            system_instruction=system_instructions
        )
        self.chat = self.model.start_chat()
        self.safety_config = [
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH
            ),
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH
            ),
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH
            ),
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH
            )
        ]

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
        self.logger.info(f"performing inference: {prompt}, {temperature}, {tools}, {file_uris}, {response_schema}")
        stream = self.chat.send_message(
            prompt_parts,
            generation_config=generation_config,
            safety_settings=self.safety_config,
            tools=active_tools,
            stream=True)
        result_chunks = []
        try:
            for chunk in stream:
                result_chunks.append(chunk.text)
        except Exception as error:
            self.logger.info(f"inference failed: {error}")
            return error.args[0]
        result = "".join(result_chunks)
        self.logger.info(f"finished inference: {result}")
        return result
