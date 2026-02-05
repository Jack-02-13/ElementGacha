from __future__ import annotations

import time
from dataclasses import dataclass

import config
from save import SaveData


@dataclass(frozen=True)
class TicketRule:
    interval_seconds: int
    cap: int


def get_ticket_rule(paid_unlocked: bool) -> TicketRule:
    if paid_unlocked:
        return TicketRule(
            interval_seconds=config.PAID_TICKET_INTERVAL_SECONDS,
            cap=config.PAID_TICKET_CAP,
        )
    return TicketRule(
        interval_seconds=config.FREE_TICKET_INTERVAL_SECONDS,
        cap=config.FREE_TICKET_CAP,
    )


def clamp_ticket_count(state: SaveData) -> None:
    rule = get_ticket_rule(state.paid_unlocked)
    state.ticket_count = max(0, min(state.ticket_count, rule.cap))


def replenish_tickets(state: SaveData, now: float | None = None) -> int:
    """
    Add tickets based on elapsed time and account mode.
    Returns how many tickets were actually added this call.
    """
    current = time.time() if now is None else now
    rule = get_ticket_rule(state.paid_unlocked)
    clamp_ticket_count(state)

    if state.last_ticket_ts <= 0:
        state.last_ticket_ts = current
        return 0

    if current < state.last_ticket_ts:
        state.last_ticket_ts = current
        return 0

    elapsed = current - state.last_ticket_ts
    generated = int(elapsed // rule.interval_seconds)
    if generated <= 0:
        return 0

    available = rule.cap - state.ticket_count
    if available <= 0:
        state.last_ticket_ts = current
        return 0

    added = min(generated, available)
    state.ticket_count += added

    if state.ticket_count >= rule.cap:
        state.last_ticket_ts = current
    else:
        state.last_ticket_ts += added * rule.interval_seconds
    return added


def can_spend_tickets(state: SaveData, cost: int) -> bool:
    return cost > 0 and state.ticket_count >= cost


def spend_tickets(state: SaveData, cost: int) -> bool:
    if not can_spend_tickets(state, cost):
        return False
    state.ticket_count -= cost
    return True

