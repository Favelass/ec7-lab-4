"""Wake-word-gated closed grammar with a graded sentence similarity."""
from __future__ import annotations
import difflib
import re

INTENTS = ["forward", "stop", "turn_left", "turn_right", "carry", "make",
           "assert_conveyor", "why", "not_for_me", "unparsed"]
PRODUCTS = ["blue pallet", "red pallet", "green crate", "grey box"]
ACCEPTED = (
    ["forward", "go forward", "move forward", "forward please",
     "stop", "stop now", "turn left", "left", "turn right", "right",
     "why", "why not"]
    + [f"carry {p}" for p in PRODUCTS]
    + [f"carry the {p}" for p in PRODUCTS]
    + [f"make {p}" for p in PRODUCTS]
    + [f"make the {p}" for p in PRODUCTS]
)
FILLER = {"go", "going", "keep", "move", "moving", "please", "could", "would",
          "you", "to", "the", "a", "an", "now", "turn", "just", "one", "it"}
WAKE = re.compile(r"^\s*robot\s+(\d)\b[\s,]*", re.IGNORECASE)
CONVEYOR = re.compile(r"conveyor\s+(\d)\s+is\s+(out of service|busy|free)", re.IGNORECASE)
MY_NUMBER = "3"
UNKNOWN_ARGUMENT_CAP = 0.55


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", text.lower()).strip()


def similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def interpret(text: str) -> tuple[str, str | None, float]:
    raw = text.strip()
    match = WAKE.match(raw)
    if match is None:
        return "unparsed", None, 0.0
    if match.group(1) != MY_NUMBER:
        return "not_for_me", f"robot {match.group(1)}", 0.95
    rest = normalize(raw[match.end():])
    if not rest:
        return "unparsed", None, 0.0
    # Full assertion only: a valid prefix must not swallow another order.
    conveyor = CONVEYOR.fullmatch(rest)
    if conveyor is not None:
        return "assert_conveyor", f"{conveyor.group(1)} {conveyor.group(2)}", 0.95
    confidence = max(similarity(rest, sentence) for sentence in ACCEPTED)
    words = rest.split()
    if words[0] in ("carry", "make", "take", "bring", "build"):
        intent = "carry" if words[0] in ("carry", "take", "bring") else "make"
        tail = " ".join(w for w in words[1:] if w not in FILLER)
        product = next((p for p in PRODUCTS if p == tail), None)
        return intent, product, confidence if product else min(confidence, UNKNOWN_ARGUMENT_CAP)
    core = [w for w in words if w not in FILLER]
    if len(core) == 1:
        if core[0] in ("forward", "stop"):
            return core[0], None, confidence
        if core[0] in ("left", "right"):
            return f"turn_{core[0]}", None, confidence
    if core in (["why"], ["why", "not"]):
        return "why", None, confidence
    return "unparsed", None, confidence
