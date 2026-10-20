from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# model = ChatGroq(
#     # model="openai/gpt-oss-120b",
#     # model = "minimaxai/minimax-m2.7",
#     model = "qwen/qwen3.8-27b",
#     # temperature=0,
# )

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash")

eval_model = "gpt-6-luna"

# response = model.invoke(
#     "Tell me 2 facts about the Sun in 2 sentences."
# )

# print(response.content)
