import os
import time
from groq import Groq
import cohere
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

cohere_client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

class Model:
    def __init__(self, prompt):
        self.prompt = prompt

    @staticmethod
    def OPENAI_MODEL(prompt):
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt, }],
            model="llama-3.3-70b-versatile", temperature=0.1
        )
        return (chat_completion.choices[0].message.content)

    @staticmethod
    def Cohere_Model(prompt):
        response = cohere_client.generate(
            model="command",
            prompt=prompt,
            max_tokens=2500,
            temperature=0.1,
        )
        return (response.generations[0].text)








