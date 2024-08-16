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

    def chat_message(self, prompt, pdf_blobs, temperature, requested_tools):
        self.logger.info(f"Vertex agent received generate request")
        active_tools = []
        if "google_search" in requested_tools:
            active_tools.append(Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval()))
        prompt_parts = [prompt]
        for pdf in pdf_blobs:
            pdf_part = Part.from_data(pdf, mime_type="application/pdf")
            prompt_parts.append(pdf_part)
        stream = self.chat.send_message(
            prompt_parts,
            generation_config=GenerationConfig(
                temperature=temperature),
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
