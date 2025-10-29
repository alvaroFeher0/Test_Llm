from collections import Counter
from datetime import datetime

def summarize_players(players):
    return "\n".join([f"- {p.get('name', 'Unknown')}" for p in players])

def make_player_lookup(players):
    return {p.get("id") or p.get("playerId"): p.get("name") for p in players}

def summarize_matches(matches, player_lookup):
    summaries = []
    for m in matches[-5:]:  # last 5 only
        team_blanc_ids = m.get("teamBlanc", [])
        team_negre_ids = m.get("teamNegre", [])
        team_blanc = [player_lookup.get(pid, pid) for pid in team_blanc_ids]
        team_negre = [player_lookup.get(pid, pid) for pid in team_negre_ids]
        winner = m.get("winner", "unknown")

        summaries.append(
            f"{m.get('matchId', '?')} — Blanc ({', '.join(team_blanc)}) "
            f"vs Negre ({', '.join(team_negre)}) — Winner: {winner}"
        )
    return "\n".join(summaries)


def summarize_match_actions(actions):
    stats = {}
    for a in actions:
        name = a.get("playerName", "Unknown")
        act = a.get("action") or a.get("Action")
        stats.setdefault(name, Counter())[act] += 1

    lines = []
    for player, actions in stats.items():
        acts_text = ", ".join([f"{k}: {v}" for k, v in actions.items()])
        lines.append(f"{player} — {acts_text}")
    return "\n".join(lines)

def build_context(players, matches, actions):
    lookup = make_player_lookup(players)
    player_names = ", ".join([p["name"] for p in players])
    match_summary = summarize_matches(matches, lookup)
    action_summary = summarize_match_actions(actions)

    return f"""
=== JF League Snapshot ===

Players:
{player_names}

Recent Matches:
{match_summary}

Recent Player Actions:
{action_summary}
"""