from langchain.tools import tool
from data import users_data
from dotenv import load_dotenv
import logging
from objects import PurchaseItem
from datetime import date

load_dotenv()

@tool
def get_user_purchase_history(user: str) -> dict:
    """This tool takes the username and 
    returns a dictionary of the user purchase history,
    if the user exists
    """
    logging.info(f"Using get_user_purchase_history tool on user: {user}")
    if users_data.get(user):
        return users_data[user]

    return {"status": "no user found"}

@tool
def calculate_right_refund(user: str, items: list[PurchaseItem]) -> str:
    """This tool takes a list of itmes to be returned and 
    the user name and returns the total refund amount for the items 
    if they are eligible for a refund
    """
    logging.info(f"Using calculate_right_refund tool on user: {user} and items: {items}")
    if not users_data.get(user):
        return {"status": "no user found"}

    total_refund = 0
    for item in items:
        item_name = item.name
        if users_data[user].get(item_name):
            purchase_date = date.fromisoformat(users_data[user][item_name]["date"])
            current_date = date.today()
            days_since_purchase = (current_date - purchase_date).days

            if days_since_purchase <= 30:
                total_refund += users_data[user][item_name]["price"]

    return {"total_refund": total_refund}

@tool
def issue_refund_ticket(user: str, refund_amount: float) -> dict:
    """This tool takes the user name and the refund amount
    and issues a refund ticket for the user
    """
    logging.info(f"Using issue_refund_ticket tool on user: {user}")

    # For this example, we'll just return a success message.
    return {
        "status": "success",
        "message": f"Refund ticket issued for user {user} with a refund amount of ${refund_amount}."
    }


@tool
def get_current_date() -> str:
    """This tool returns the current date in YYYY-MM-DD format."""
    logging.info("Using get_current_date tool")
    return date.today().isoformat()


# print(get_user_purchase_history.invoke("user124"))
print(calculate_right_refund.invoke({
    "user124", 
    [PurchaseItem(name="notebook"), PurchaseItem(name="pen")]
    })
)
# print(get_current_date.invoke())