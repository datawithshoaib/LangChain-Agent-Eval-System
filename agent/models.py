from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

model = ChatGroq(model = "openai/gpt-oss-120b")

# response = model.invoke("Tell me 2 facts about the sun in 2 sentences.")
# print(response.content)
