"""Operator-facing explanations, from the actual refusal and world state."""
from __future__ import annotations
from step3 import *


def explain(entry: dict) -> str:
    world = entry.get("world", {})
    reason = entry.get("reason")
    intent = entry.get("intent")
    if reason == "not_understood":
        if intent in ("carry", "make") and not entry.get("arguments"):
            return f"{intent} what? Say a product I know."
        if intent != "unparsed":
            return f"Uncertain about {intent}; please repeat the full order."
        return "I did not catch that; say it again."
    if reason == "not_permitted":
        distance = world.get("person_distance_m")
        if distance is None:
            return "Person ahead; stopped. Ask supervisor to clear the lane."
        return f"Person {distance:g} m ahead; stopped. Ask supervisor to clear."
    if reason == "not_possible":
        if world.get("carrying"):
            return f"Already holding {world['carrying']}; wait until unloading finishes."
        conveyor = world.get("product_conveyor", {}).get(entry.get("arguments"))
        status = world.get("conveyors", {}).get(conveyor, "unknown")
        if status == "out of service":
            return f"Conveyor {conveyor} out of service; wait for repair."
        return f"Conveyor {conveyor} {status}; please wait."
    if reason == "not_for_me":
        return f"That order addresses {entry.get('arguments')}; I ignore it."
    return ""
