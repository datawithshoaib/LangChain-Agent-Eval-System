from uuid import uuid4

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from models import model
from tools import (
    calculate_right_refund,
    get_user_purchase_history,
    issue_refund_ticket,
    get_today_date,
)
from prompts import agent_system_prompt
from objects import Answer

load_dotenv()

checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    tools=[
        get_user_purchase_history,
        calculate_right_refund,
        issue_refund_ticket,
        get_today_date,
    ],
    system_prompt=agent_system_prompt,
    response_format=Answer,
    checkpointer=checkpointer,
)


def run_conversation():
    config = {
        "configurable": {
            "thread_id": str(uuid4()),
        }
    }

    question = HumanMessage(
        content="Hello, I would like to request a refund for my recent purchase."
    )

    conversation = True

    while conversation:
        response = agent.invoke(
            {"messages": [question]},
            config=config,
        )

        structured_response = response["structured_response"]

        print(f"Agent: {structured_response.answer}")

        conversation = structured_response.conversation

        if conversation:
            user_input = input("User: ").strip()

            if not user_input:
                print("Please enter a message.")
                continue

            question = HumanMessage(content=user_input)

    print("Conversation ended. Thank you for using our refund service.")


if __name__ == "__main__":
    run_conversation()
