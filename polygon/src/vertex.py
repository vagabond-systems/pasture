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

    def chat_message(self, prompt, file_urls, temperature, requested_tools):
        self.logger.info(f"Vertex agent received generate request")
        active_tools = []
        if "google_search" in requested_tools:
            active_tools.append(Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval()))
        prompt_parts = [prompt]
        for file_url in file_urls:
            pdf_file = Part.from_uri(file_url, mime_type="application/pdf")
            prompt_parts.append(pdf_file)
        stream = self.chat.send_message(
            prompt_parts,
            generation_config=GenerationConfig(
                temperature=temperature,
            ),
            tools=active_tools,
            stream=True)
        response_text_chunks = []
        for chunk in stream:
            try:
                response_text_chunks.append(chunk.text)
            except Exception as error:
                break
        response_text = "".join(response_text_chunks)
        return response_text
