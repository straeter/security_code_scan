llm_prices = {
    "gpt-4o-2024-11-20": {
        "input": 2.5 / 1e6,
        "output": 10 / 1e6,
    },
    "gpt-4o-mini-2024-07-18": {
        "input": 0.150 / 1e6,
        "output": 0.600 / 1e6,
    },
    "mistral-large-2402": {
        "input": 3.8 / 1e6,
        "output": 11.3 / 1e6,
    },
    "mistral-small-2402": {
        "input": 0.9 / 1e6,
        "output": 2.8 / 1e6,
    },
    "claude-3-opus-20240229": {
        "input": 15 / 1e6,
        "output": 75 / 1e6
    },
    "claude-3-sonnet-20240229": {
        "input": 3 / 1e6,
        "output": 15 / 1e6
    },
    "claude-3-haiku-20240307": {
        "input": 0.25 / 1e6,
        "output": 1.25 / 1e6
    },
    "gpt-3.5-ft": {
        "input": 3 / 1e6,
        "output": 6 / 1e6,
        "training": 8 / 1e6
    },
    "gpt-4o-mini-ft": {
        "input": 0.3 / 1e6,
        "output": 1.2 / 1e6,
        "training": 3 / 1e6
    },
}


def get_llm_price(checkpoint: str):
    if checkpoint in llm_prices:
        return llm_prices[checkpoint]

    for key in llm_prices:
        if key.startswith(checkpoint):
            return llm_prices[key]

    if "ft:" in checkpoint:
        if "gpt-3.5" in checkpoint:
            return llm_prices["gpt-3.5-ft"]
        elif "gpt-4o-mini" in checkpoint:
            return llm_prices["gpt-4o-mini-ft"]
    else:
        raise ValueError(f"Checkpoint {checkpoint} not found in llm_prices")
