"""State-based decision: stopping and explanation precede motion guards."""
from __future__ import annotations
from step2 import *

ACTIONS = ["forward", "stop", "turn_left", "turn_right", "carry", "make",
           "note", "explain", "refuse", "ignore"]
REASONS = ["ok", "not_understood", "not_permitted", "not_possible", "not_for_me"]


def decide(intent: str, arguments: str | None, confidence: float,
           state: dict) -> tuple[str, str]:
    if intent == "not_for_me":
        return "ignore", "not_for_me"
    # An understood emergency stop never depends on a confidence threshold.
    if intent == "stop":
        return "stop", "ok"
    if intent == "unparsed":
        return "refuse", "not_understood"
    # A person ahead must not prevent answering the operator's question.
    if intent == "why":
        return "explain", "ok"
    if intent == "assert_conveyor":
        return "note", "ok"
    if state.get("person_ahead"):
        return "refuse", "not_permitted"
    if intent in ("carry", "make") and arguments not in PRODUCTS:
        return "refuse", "not_understood"
    if confidence < state.get("threshold", 0.5):
        return "refuse", "not_understood"
    if intent == "carry":
        return ("refuse", "not_possible") if state.get("carrying") else ("carry", "ok")
    if intent == "make":
        conveyor = state.get("product_conveyor", {}).get(arguments)
        if conveyor is None or state.get("conveyors", {}).get(conveyor) != "free":
            return "refuse", "not_possible"
        return "make", "ok"
    if intent in ("forward", "turn_left", "turn_right"):
        return intent, "ok"
    return "refuse", "not_understood"
