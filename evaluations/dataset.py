from deepeval.dataset import EvaluationDataset, Golden
from deepeval.test_case import ToolCall


dataset = EvaluationDataset(
    goldens=[
        # Scenario 1: Full refund for multiple eligible items.
        # The book ($23) and pen ($7) are both within the 30-day window.
        Golden(
            input="I am user123, I would like a refund for the book and the pen.",
            expected_output=(
                "A refund ticket for $30 has been issued successfully "
                "for the book and pen."
            ),
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "user123"},
                ),
                ToolCall(
                    name="get_today_date",
                    input_parameters={},
                ),
                ToolCall(
                    name="calculate_right_refund",
                    input_parameters={
                        "user": "user123",
                        "items": [{"name": "book"}, {"name": "pen"}],
                    },
                ),
                ToolCall(
                    name="issue_refund_ticket",
                    input_parameters={
                        "user": "user123",
                        "refund_amount": 30,
                    },
                ),
            ],
        ),

        # Scenario 2: Refund for only one item in a multi-item purchase history.
        # The agent must not refund the pen when the user requests only the book.
        Golden(
            input="I am user123, I would like a refund for the book.",
            expected_output=(
                "A refund ticket for $23 has been issued successfully "
                "for the book."
            ),
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "user123"},
                ),
                ToolCall(
                    name="get_today_date",
                    input_parameters={},
                ),
                ToolCall(
                    name="calculate_right_refund",
                    input_parameters={
                        "user": "user123",
                        "items": [{"name": "book"}],
                    },
                ),
                ToolCall(
                    name="issue_refund_ticket",
                    input_parameters={
                        "user": "user123",
                        "refund_amount": 23,
                    },
                ),
            ],
        ),

        # Scenario 3: Information-only request.
        # The user wants purchase history, not a refund.
        # Do not calculate a refund or issue a ticket.
        Golden(
            input=(
                "I am user123. I do not want a refund; "
                "I only want to know what I purchased."
            ),
            expected_output=(
                "Your purchase history includes a book for $23 "
                "and a pen for $7. No refund ticket was issued."
            ),
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "user123"},
                ),
            ],
        ),

        # Scenario 4: Invalid username.
        # The agent must not disclose purchase information or issue a refund.
        Golden(
            input="I am user999, I would like a refund for the book.",
            expected_output=(
                "The username is invalid. Please provide a valid username "
                "so I can assist with your refund request."
            ),
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "user999"},
                ),
            ],
        ),

        # Scenario 5: Requested item is outside the 30-day refund window.
        # user126 purchased the water bottle on 2026-07-25.
        # As of 2026-10-20, it is ineligible.
        # Do not calculate or issue a refund.
        Golden(
            input=(
                "I am user126, I would like a refund for the water_bottle."
            ),
            expected_output=(
                "No refund will be issued for the water_bottle because "
                "the purchase is older than the 30-day refund window."
            ),
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "user126"},
                ),
                ToolCall(
                    name="get_today_date",
                    input_parameters={},
                ),
            ],
        ),

        # Scenario 6: Partial refund when only one requested item is eligible.
        # Backpack ($45): eligible.
        # Water bottle ($18): ineligible because it is too old.
        # Refund only the backpack.
        Golden(
            input=(
                "I am user126, I would like a refund for the backpack "
                "and water_bottle."
            ),
            expected_output=(
                "A refund ticket for $45 has been issued for the backpack. "
                "The water_bottle is not eligible because its purchase "
                "is outside the 30-day refund window."
            ),
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "user126"},
                ),
                ToolCall(
                    name="get_today_date",
                    input_parameters={},
                ),
                ToolCall(
                    name="calculate_right_refund",
                    input_parameters={
                        "user": "user126",
                        "items": [{"name": "backpack"}],
                    },
                ),
                ToolCall(
                    name="issue_refund_ticket",
                    input_parameters={
                        "user": "user126",
                        "refund_amount": 45,
                    },
                ),
            ],
        ),

        # Scenario 7: Item was never purchased by the identified customer.
        # Do not calculate a refund or issue a ticket for nonexistent purchases.
        Golden(
            input="I am user126, I would like a refund for the sneakers.",
            expected_output=(
                "No refund will be issued because the sneakers "
                "were not found in your verified purchase history."
            ),
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "user126"},
                ),
            ],
        ),

        # Scenario 8: Purchase date is in the future.
        # user129's folder has a date of 2026-10-25.
        # As of 2026-10-20, this is invalid purchase data.
        # The agent must not calculate or issue a refund.
        Golden(
            input="I am user129, I would like a refund for the folder.",
            expected_output=(
                "The purchase date for the folder is in the future, "
                "so the purchase cannot be validated and no refund "
                "will be issued."
            ),
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "user129"},
                ),
                ToolCall(
                    name="get_today_date",
                    input_parameters={},
                ),
            ],
        ),

        # Scenario 9: Purchase exactly 30 days ago.
        # The policy treats the 30-day boundary as eligible.
        # This assumes the test date is 2026-10-20 and the purchase date
        # is 2026-09-20.
        Golden(
            input=(
                "I am user125, I would like a refund for an item "
                "purchased on 2026-09-20."
            ),
            expected_output=(
                "The item is eligible based on the 30-day date policy, "
                "subject to verification that it belongs to your purchases."
            ),
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "user125"},
                ),
                ToolCall(
                    name="get_today_date",
                    input_parameters={},
                ),
            ],
        ),
    ]
)
