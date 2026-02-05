from __future__ import annotations

import unittest

import config
from save import SaveData
from ticket import get_ticket_rule, replenish_tickets


class TicketRuleTests(unittest.TestCase):
    def test_rule_values(self) -> None:
        free_rule = get_ticket_rule(False)
        paid_rule = get_ticket_rule(True)
        self.assertEqual(free_rule.interval_seconds, config.FREE_TICKET_INTERVAL_SECONDS)
        self.assertEqual(free_rule.cap, config.FREE_TICKET_CAP)
        self.assertEqual(paid_rule.interval_seconds, config.PAID_TICKET_INTERVAL_SECONDS)
        self.assertEqual(paid_rule.cap, config.PAID_TICKET_CAP)


class TicketReplenishTests(unittest.TestCase):
    def test_free_replenish_every_60_seconds(self) -> None:
        state = SaveData(paid_unlocked=False, ticket_count=0, last_ticket_ts=100.0)
        added = replenish_tickets(state, now=280.0)
        self.assertEqual(added, 3)
        self.assertEqual(state.ticket_count, 3)

    def test_paid_replenish_every_second(self) -> None:
        state = SaveData(paid_unlocked=True, ticket_count=0, last_ticket_ts=100.0)
        added = replenish_tickets(state, now=150.0)
        self.assertEqual(added, 50)
        self.assertEqual(state.ticket_count, 50)

    def test_replenish_clamped_by_cap(self) -> None:
        state = SaveData(
            paid_unlocked=False,
            ticket_count=config.FREE_TICKET_CAP - 1,
            last_ticket_ts=100.0,
        )
        added = replenish_tickets(state, now=100.0 + config.FREE_TICKET_INTERVAL_SECONDS * 100)
        self.assertEqual(added, 1)
        self.assertEqual(state.ticket_count, config.FREE_TICKET_CAP)


if __name__ == "__main__":
    unittest.main()

