from __future__ import annotations

import random
import unittest

import config
from data.elements import ELEMENTS
from gacha import GachaEngine, draw_batch
from save import SaveData


class ProbabilityTests(unittest.TestCase):
    def test_rarity_weight_sum_is_one(self) -> None:
        self.assertAlmostEqual(sum(config.RARITY_WEIGHTS.values()), 1.0, places=9)


class BucketTests(unittest.TestCase):
    def test_drawn_element_matches_rolled_rarity(self) -> None:
        engine = GachaEngine(ELEMENTS, rng=random.Random(2026))
        for _ in range(2000):
            rolled_rarity, element = engine.pull_with_rarity()
            self.assertEqual(rolled_rarity, element.rarity_level)


class DrawBatchTests(unittest.TestCase):
    def test_insufficient_ticket_message(self) -> None:
        state = SaveData(ticket_count=3, last_ticket_ts=100.0)
        engine = GachaEngine(ELEMENTS, rng=random.Random(1))
        result = draw_batch(state, engine, draw_count=5, now=100.0)
        self.assertFalse(result.success)
        self.assertEqual(result.message, "抽卡券不足 (3 / 5)")


if __name__ == "__main__":
    unittest.main()

