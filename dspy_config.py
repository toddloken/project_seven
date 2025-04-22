import dspy
from dotenv import load_dotenv
import os


class DSPyConfigurator:
    def __init__(self, model_name="openai/gpt-4", env_var="OPENAI_API_KEY"):
        self.model_name = model_name
        self.env_var = env_var
        self.api_key = None
        self.llm = None

    def load_api_key(self):
        load_dotenv()
        self.api_key = os.getenv(self.env_var)
        if not self.api_key:
            raise ValueError(f"API key not found in environment variable '{self.env_var}'")

    def configure(self):
        self.load_api_key()
        self.llm = dspy.LM(self.model_name, api_key=self.api_key)
        dspy.settings.configure(lm=self.llm)

# # Example usage
# if __name__ == "__main__":
#     config = DSPyConfigurator()
#     config.configure()
#
# print(config)