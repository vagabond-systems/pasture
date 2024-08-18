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

    def chat_message(self, prompt, temperature, requested_tools, mimetype_blob_tuples, response_schema):
        self.logger.info(f"Vertex agent received generate request")
        active_tools = []
        if "google_search" in requested_tools:
            active_tools.append(Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval()))
        prompt_parts = [prompt]
        for mimetype, blob in mimetype_blob_tuples:
            data_part = Part.from_data(blob, mime_type=mimetype)
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
