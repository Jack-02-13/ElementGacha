from __future__ import annotations

import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Sequence

import config
from data.elements import Element
from save import SaveData
from ticket import replenish_tickets, spend_tickets


@dataclass(frozen=True)
class DrawEntry:
    element: Element
    count: int


@dataclass(frozen=True)
class DrawBatchResult:
    success: bool
    message: str
    newly_obtained: list[DrawEntry]
    already_owned: list[DrawEntry]


class GachaEngine:
    def __init__(self, elements: Sequence[Element], rng: random.Random | None = None) -> None:
        self.rng = rng or random.Random()
        self.elements_by_rarity: dict[int, list[Element]] = defaultdict(list)
        self.elements_by_atomic_number: dict[int, Element] = {}

        for element in elements:
            self.elements_by_rarity[element.rarity_level].append(element)
            self.elements_by_atomic_number[element.atomic_number] = element

        for rarity in config.RARITY_WEIGHTS:
            if not self.elements_by_rarity.get(rarity):
                raise ValueError(f"Rarity bucket {rarity} is empty.")

    def roll_rarity(self) -> int:
        roll = self.rng.random()
        cumulative = 0.0
        for rarity, weight in config.RARITY_WEIGHTS.items():
            cumulative += weight
            if roll < cumulative:
                return rarity
        return max(config.RARITY_WEIGHTS)

    def pull_with_rarity(self) -> tuple[int, Element]:
        rarity = self.roll_rarity()
        element = self.rng.choice(self.elements_by_rarity[rarity])
        return rarity, element

    def pull(self) -> Element:
        _, element = self.pull_with_rarity()
        return element


def collected_count(state: SaveData, elements: Sequence[Element]) -> int:
    return sum(1 for element in elements if state.owned.get(element.atomic_number, 0) > 0)


def _sort_draw_entries(entries: list[DrawEntry]) -> list[DrawEntry]:
    return sorted(
        entries,
        key=lambda entry: (-entry.element.rarity_level, entry.element.atomic_number),
    )


def draw_batch(
    state: SaveData,
    engine: GachaEngine,
    draw_count: int,
    now: float | None = None,
) -> DrawBatchResult:
    if draw_count <= 0:
        return DrawBatchResult(False, "抽卡次數必須大於 0。", [], [])

    replenish_tickets(state, now=now)

    if state.ticket_count < draw_count:
        return DrawBatchResult(
            False,
            f"抽卡券不足 ({state.ticket_count} / {draw_count})",
            [],
            [],
        )

    owned_before = {atomic_number for atomic_number, count in state.owned.items() if count > 0}
    spend_tickets(state, draw_count)

    rolled_counts: Counter[int] = Counter()
    for _ in range(draw_count):
        element = engine.pull()
        rolled_counts[element.atomic_number] += 1

    for atomic_number, count in rolled_counts.items():
        state.owned[atomic_number] = state.owned.get(atomic_number, 0) + count
    state.total_draws += draw_count

    newly_obtained: list[DrawEntry] = []
    already_owned: list[DrawEntry] = []
    for atomic_number, count in rolled_counts.items():
        element = engine.elements_by_atomic_number[atomic_number]
        entry = DrawEntry(element=element, count=count)
        if atomic_number in owned_before:
            already_owned.append(entry)
        else:
            newly_obtained.append(entry)

    return DrawBatchResult(
        success=True,
        message="",
        newly_obtained=_sort_draw_entries(newly_obtained),
        already_owned=_sort_draw_entries(already_owned),
    )

