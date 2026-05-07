"""
ai_generator.py
---------------
Week 2: hook this up to the Claude API to generate
- level layouts (list of wall rects)
- mission briefings (flavour text)

For now it returns placeholder data so the game runs without an API key.
"""

# Uncomment in Week 2:
# import anthropic
# client = anthropic.Anthropic(api_key="YOUR_KEY_HERE")


def generate_mission_briefing(wave: int) -> str:
    """Return a short mission briefing string for the current wave."""
    # --- Week 2: replace with real API call ---
    placeholders = [
        "Hostile forces detected. Eliminate all targets.",
        f"Wave {wave}: Reinforcements incoming. Hold your ground.",
        "Intel reports a heavy unit in the area. Stay sharp.",
        "Enemy comms intercepted. Ambush likely — watch your flanks.",
        f"Wave {wave}: All units are hostile. No survivors.",
    ]
    return placeholders[wave % len(placeholders)]


def generate_level_layout(wave: int):
    """
    Return a list of (x, y, w, h) wall tuples for the given wave.
    Week 2: ask Claude to invent a new layout each run.
    """
    # For now just return None → level.py will use default_layout()
    return None