"""
ai_generator.py
---------------
Uses Groq API to generate:
- Mission briefings per wave
- Continuing narrative storyline across waves
- Level layouts (wall rectangles)
"""

import os
import json
import random
from groq import Groq
from dotenv import load_dotenv
from settings import WIDTH, HEIGHT, WALL_THICKNESS

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL  = "meta-llama/llama-4-scout-17b-16e-instruct"

_story_history = []

STYLES = [
    "corridor-style: long horizontal and vertical walls forming narrow passages with clear entrances",
    "open arena: 3-4 large rectangular cover blocks placed symmetrically with wide open spaces",
    "maze-like: many small scattered walls creating tight corners and multiple chokepoints",
    "cross-divided: 4 long walls from centre outward dividing arena into quadrants with gaps at each end",
    "asymmetric: one large L-shaped wall on the right side, small scattered cover on the left",
    "room-within-room: large hollow rectangle in centre with one opening per side",
    "corner clusters: groups of 2-3 walls in each corner, completely open centre",
    "bunker: 3-4 thick parallel horizontal walls running across the arena with gaps between",
]


def generate_mission_briefing(wave: int) -> str:
    try:
        history_text = ""
        if _story_history:
            history_text = "Previous events:\n" + "\n".join(
                f"- Wave {i+1}: {s}" for i, s in enumerate(_story_history)
            )

        is_boss = wave == 5
        prompt = f"""You are a military narrator for a top-down shooter game called Run & Gun.
The player is an elite soldier fighting through enemy-controlled territory.
{history_text}

Write a mission briefing for Wave {wave + 1}.
{"BOSS WAVE: The enemy commander has been located. Make this dramatic, high-stakes, and intense." if is_boss else ""}
Requirements:
- Exactly 1-2 sentences, no more
- Military jargon, urgent tone
- Build on previous events naturally if available
- End with a clear objective
- No hashtags, markdown, quotes, or formatting — plain text only
- Be specific and varied, avoid generic phrases like "hostile forces detected"
"""
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80,
            temperature=0.9,
        )
        briefing = response.choices[0].message.content.strip()
        summary  = briefing[:80] + "..." if len(briefing) > 80 else briefing
        _story_history.append(summary)
        return briefing

    except Exception as e:
        print(f"[AI] Mission briefing failed: {e}")
        fallbacks = [
            "Alpha squad, your insertion point is hot — enemy patrols are converging. Clear the sector.",
            "Command has lost contact with Bravo team. Move in, neutralise all threats, and find out why.",
            "Satellite imaging shows heavy reinforcements inbound. Hold the line until they're all down.",
            "We've intercepted enemy comms — they know you're here. Adapt and eliminate every last one.",
            "The commander is barricaded ahead. This ends now — take him down at all costs.",
        ]
        return fallbacks[wave % len(fallbacks)]


def generate_level_layout(wave: int):
    try:
        import pygame
        screen = pygame.display.get_surface()
        W, H = screen.get_size() if screen else (900, 600)
        t = WALL_THICKNESS
        style = STYLES[wave % len(STYLES)]

        # Express coordinates as percentages of W and H for resolution independence
        prompt = f"""You are an expert level designer for a top-down arcade shooter.
Arena: {W} x {H} pixels. Player spawns at ({int(W*0.15)}, {H//2}). Enemies at corners/edges.

STYLE FOR THIS WAVE: {style}

Generate walls as a JSON array [[x, y, width, height], ...].

MANDATORY BORDER WALLS (copy exactly):
[0, 0, {W}, {t}], [0, {H-t}, {W}, {t}], [0, 0, {t}, {H}], [{W-t}, 0, {t}, {H}]

INNER WALLS — follow the style strictly:
- Count: 8 to 14 walls
- Spread walls across the FULL {W}x{H} space — use all 4 quadrants
- Horizontal walls: width {int(W*0.08)}-{int(W*0.20)}, height {t}-{t*2}
- Vertical walls: width {t}-{t*2}, height {int(H*0.08)}-{int(H*0.25)}
- Minimum gap between any two walls: {int(W*0.07)}px
- Keep x < {int(W*0.20)} completely clear (player spawn zone)
- NO walls within {int(W*0.06)}px of screen edges (border walls excluded)
- Vary positions — no two walls at the same x or y coordinate

RETURN: raw JSON array only. Zero explanation. Zero markdown."""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7,
        )
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        # If response is missing outer brackets, wrap it
        stripped = text.strip()
        if not stripped.startswith("["):
            stripped = "[" + stripped + "]"
        elif not stripped.startswith("[["):
            # Has outer bracket but items aren't wrapped — already correct
            pass
        # Ensure it's wrapped as array of arrays
        try:
            layout_raw = json.loads(stripped)
        except json.JSONDecodeError:
            # Last resort: find outermost [ ] 
            start = text.find("[")
            end   = text.rfind("]") + 1
            layout_raw = json.loads("[" + text[start:end] + "]")
        layout = [tuple(int(v) for v in wall) for wall in layout_raw]
        print(f"[AI] Wave {wave+1} — '{style[:35]}...' — {len(layout)} walls at {W}x{H}")
        return layout

    except Exception as e:
        print(f"[AI] Level generation failed: {e}")
        return None


def reset_story():
    global _story_history
    _story_history = []