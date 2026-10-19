from pydantic import BaseModel, Field

class Answer(BaseModel):
    answer: str = Field(
        description="A clear and relevant response to the user's question."
    )

    conversation: bool = Field(
        default=True,
        description=(
            "Indicates whether the conversation should continue. "
            "Set to True if the agent needs more information, must ask "
            "a follow-up question, or needs to continue discussing the issue. "
            "Set to False when the issue has been fully resolved, "
            "the refund decision has been finalized, and no further "
            "conversation is required."
        )
    )

class PurchaseItem(BaseModel):
    name: str = Field(
        description="The name of the item purchased by the user."
    )
