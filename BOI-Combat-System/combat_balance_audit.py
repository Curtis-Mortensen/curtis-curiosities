#!/usr/bin/env python3
"""
Audit tool for combat-balance-guide.html monster tuning.

Models standard 3-round fights: expected damage = rounds × base_dmg × monsters × hit%.

Hit chance comes from a single die roll vs player AC (default 4):
    (die_result + modifier) >= AC  → hit

Run:
    python combat_balance_audit.py              # audit guide stat blocks
    python combat_balance_audit.py --table      # all achievable single-die hit rates
    python combat_balance_audit.py --solve      # best roll per target (any die type)
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

AC = 4
ROUNDS = 3
LIFESTEAL_ROUNDS = 4
LIFESTEAL_HEAL_PER_HIT = 0.5
PARTY_DMG_PER_PLAYER = 0.75
DIE_SIDES = (4, 6, 8, 10, 12, 20)
MODIFIER_RANGE = range(-5, 6)  # inclusive -5 .. +5


@dataclass(frozen=True)
class Roll:
    sides: int
    modifier: int

    @property
    def label(self) -> str:
        if self.modifier == 0:
            return f"1d{self.sides}"
        sign = "+" if self.modifier > 0 else ""
        return f"1d{self.sides}{sign}{self.modifier}"

    def hit_chance(self, ac: int = AC) -> float:
        threshold = ac - self.modifier
        if threshold <= 1:
            return 1.0
        if threshold > self.sides:
            return 0.0
        successes = self.sides - threshold + 1
        return successes / self.sides


@dataclass
class GuideEntry:
    archetype: str
    party: int
    level: int
    monsters: int
    base_dmg: float
    roll: str
    hit_pct: float
    target_dmg: float

    @property
    def rounds(self) -> int:
        return fight_rounds(self.archetype)

    @property
    def target_dpr(self) -> float:
        return target_dmg_per_round(self.target_dmg, self.rounds)

    def actual_dpr(self, hit: float | None = None) -> float:
        h = hit if hit is not None else self.hit_pct / 100
        return actual_dmg_per_round(
            self.base_dmg,
            h,
            self.monsters,
            party=self.party,
            archetype=self.archetype,
        )


@dataclass
class SolveResult:
    base_dmg: float
    roll: Roll
    ideal_hit: float
    actual_hit: float
    expected_dmg: float
    target_dmg: float
    dmg_error: float
    hit_error: float

    @property
    def label(self) -> str:
        return self.roll.label


def all_rolls(
    sides: tuple[int, ...] = DIE_SIDES,
    modifiers: range = MODIFIER_RANGE,
) -> list[Roll]:
    rolls: list[Roll] = []
    for s in sides:
        for m in modifiers:
            rolls.append(Roll(s, m))
    return rolls


def unique_hit_table(rolls: list[Roll] | None = None) -> list[tuple[float, Roll]]:
    rolls = rolls or all_rolls()
    best: dict[float, Roll] = {}
    for r in rolls:
        p = round(r.hit_chance() * 100, 4)
        if p not in best or (r.sides, abs(r.modifier)) < (best[p].sides, abs(best[p].modifier)):
            best[p] = r
    return sorted(((p, best[p]) for p in best), key=lambda x: x[0])


def parse_roll(text: str) -> Roll | None:
    m = re.match(r"1d(\d+)([+-]\d+)?", text.strip())
    if not m:
        return None
    sides = int(m.group(1))
    mod = int(m.group(2)) if m.group(2) else 0
    return Roll(sides, mod)


def closest_roll(target_hit: float, rolls: list[Roll] | None = None) -> Roll:
    rolls = rolls or all_rolls()
    return min(rolls, key=lambda r: (abs(r.hit_chance() - target_hit), r.sides, abs(r.modifier)))


def expected_damage(base: float, hit: float, monsters: int = 1, rounds: int = ROUNDS) -> float:
    return rounds * base * monsters * hit


def ideal_hit(target_dmg: float, base: float, monsters: int = 1, rounds: int = ROUNDS) -> float:
    return target_dmg / (rounds * base * monsters)


def target_dmg_per_round(target_dmg: float, rounds: int = ROUNDS) -> float:
    """Average damage per round needed to land exactly on the HP target."""
    return target_dmg / rounds


def actual_dmg_per_round(
    base: float,
    hit: float,
    monsters: int = 1,
    *,
    party: int = 2,
    archetype: str = "standard",
) -> float:
    """Expected damage to the party per round from the assigned roll."""
    if archetype == "group":
        return base * party * monsters * hit
    if archetype == "acid":
        return (5 * base * monsters * hit) / ROUNDS
    rounds = 4 if archetype == "lifesteal" else ROUNDS
    return base * monsters * hit


def fmt_dpr(value: float) -> str:
    return f"{value:.4f}"


def fight_rounds(archetype: str) -> int:
    return LIFESTEAL_ROUNDS if archetype == "lifesteal" else ROUNDS


def standard_monster_hp(party: int) -> float:
    """Total HP for a standard 3-round monster (rounded to nearest 0.5)."""
    raw = party * PARTY_DMG_PER_PLAYER * ROUNDS
    return round(raw * 2) / 2


def lifesteal_listed_hp(party: int, monsters: int, hit: float) -> float:
    """Total listed HP for a lifesteal encounter.

    Heals 0.5 HP per hit (fixed, regardless of damage). HP is derived from
    standard monster HP + one extra round of party damage − expected healing,
    with a small difficulty bump (0.5 at 75% hit, scaling up above 75%).
    """
    party_dmg = party * PARTY_DMG_PER_PLAYER
    expected_healing = LIFESTEAL_ROUNDS * monsters * hit * LIFESTEAL_HEAL_PER_HIT
    difficulty = 0.5 + 3.0 * max(0.0, hit - 0.75)
    total = standard_monster_hp(party) + party_dmg - expected_healing - difficulty
    return round(total * 2) / 2


def fmt_hp_value(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return f"{value:.1f}"


def split_monster_hp(total: float, monsters: int) -> list[float]:
    """Split total HP across monsters in 0.5 steps."""
    if monsters == 1:
        return [total]
    each = round((total / monsters) * 2) / 2
    parts = [each] * (monsters - 1)
    parts.append(round((total - each * (monsters - 1)) * 2) / 2)
    return parts


def lifesteal_four_round_budget(party: int) -> float:
    """Total damage budget for a 4-round lifesteal fight."""
    return round(party * PARTY_DMG_PER_PLAYER * LIFESTEAL_ROUNDS * 2) / 2


def fmt_hp_each(total: float, monsters: int) -> str:
    parts = split_monster_hp(total, monsters)
    if monsters == 1:
        return fmt_hp_value(parts[0])
    return " / ".join(fmt_hp_value(p) for p in parts)


def damage_multiplier(archetype: str) -> float:
    if archetype == "acid":
        return 5.0
    return float(fight_rounds(archetype))


def solve_standard(
    target_dmg: float,
    monsters: int = 1,
    rounds: int = ROUNDS,
    min_base: float = 0.5,
    max_base: float = 20.0,
    die_sides: tuple[int, ...] = DIE_SIDES,
    hit_floor: float | None = None,
    hit_ceiling: float | None = None,
    require_hit_band: bool = False,
    anchor_base: float | None = None,
) -> SolveResult:
    """Find base damage (0.5 steps) + single die roll closest to target damage.

    When anchor_base is set, search only that base (guide-style: pick base, then roll).
    Otherwise search all bases but prefer staying near target_dmg / rounds (raw per-hit dmg).
    """
    rolls = all_rolls(die_sides)
    best: SolveResult | None = None
    best_any: SolveResult | None = None
    raw_anchor = target_dmg / (rounds * monsters)

    if anchor_base is not None:
        bases = [anchor_base]
    else:
        bases = []
        b = min_base
        while b <= max_base + 1e-9:
            bases.append(b)
            b += 0.5

    for base in bases:
        ideal = ideal_hit(target_dmg, base, monsters, rounds)
        if ideal <= 0 or ideal > 1:
            continue

        roll = closest_roll(ideal, rolls)
        actual_hit = roll.hit_chance()
        exp = expected_damage(base, actual_hit, monsters, rounds)
        dmg_err = abs(exp - target_dmg)
        hit_err = abs(actual_hit - ideal)
        base_penalty = abs(base - raw_anchor) * 0.01 if anchor_base is None else 0.0

        candidate = SolveResult(
            base_dmg=base,
            roll=roll,
            ideal_hit=ideal,
            actual_hit=actual_hit,
            expected_dmg=exp,
            target_dmg=target_dmg,
            dmg_error=dmg_err + base_penalty,
            hit_error=hit_err,
        )

        in_band = True
        if hit_floor is not None and actual_hit < hit_floor:
            in_band = False
        if hit_ceiling is not None and actual_hit > hit_ceiling:
            in_band = False

        if best_any is None or (candidate.dmg_error, candidate.hit_error, candidate.base_dmg) < (
            best_any.dmg_error,
            best_any.hit_error,
            best_any.base_dmg,
        ):
            best_any = candidate

        if in_band and (
            best is None
            or (candidate.dmg_error, candidate.hit_error, candidate.base_dmg)
            < (best.dmg_error, best.hit_error, best.base_dmg)
        ):
            best = candidate

    if require_hit_band and best is not None:
        return best
    if best is not None:
        return best
    if best_any is None:
        raise ValueError(f"No valid solution for target_dmg={target_dmg}")
    return best_any


def solve_with_fixed_base(
    target_dmg: float,
    base: float,
    monsters: int = 1,
    die_sides: tuple[int, ...] = DIE_SIDES,
) -> SolveResult:
    ideal = ideal_hit(target_dmg, base, monsters)
    roll = closest_roll(ideal, all_rolls(die_sides))
    actual = roll.hit_chance()
    return SolveResult(
        base_dmg=base,
        roll=roll,
        ideal_hit=ideal,
        actual_hit=actual,
        expected_dmg=expected_damage(base, actual, monsters),
        target_dmg=target_dmg,
        dmg_error=abs(expected_damage(base, actual, monsters) - target_dmg),
        hit_error=abs(actual - ideal),
    )


# Stat blocks copied from combat-balance-guide.html (standard archetype tables)
GUIDE_STANDARD: list[GuideEntry] = [
    GuideEntry("standard", 2, 1, 1, 1.5, "1d10", 70.00, 3.2),
    GuideEntry("standard", 2, 2, 1, 2.0, "1d8+2", 87.50, 5.2),
    GuideEntry("standard", 2, 3, 1, 3.0, "1d10+1", 80.00, 7.2),
    GuideEntry("standard", 2, 4, 2, 2.0, "1d4+2", 75.00, 9.2),
    GuideEntry("standard", 2, 5, 2, 2.5, "1d4+2", 75.00, 11.2),
    GuideEntry("standard", 3, 1, 1, 2.0, "1d10+1", 80.00, 4.8),
    GuideEntry("standard", 3, 2, 1, 3.0, "1d8+2", 87.50, 7.8),
    GuideEntry("standard", 3, 3, 1, 4.5, "1d10+1", 80.00, 10.8),
    GuideEntry("standard", 3, 4, 2, 3.0, "1d4+2", 75.00, 13.8),
    GuideEntry("standard", 3, 5, 2, 3.5, "1d10+1", 80.00, 16.8),
]

GUIDE_HEAVY: list[GuideEntry] = [
    GuideEntry("heavy", 2, 1, 1, 2.0, "1d4+1", 50.00, 3.2),
    GuideEntry("heavy", 2, 2, 1, 3.5, "1d4+1", 50.00, 5.2),
    GuideEntry("heavy", 2, 3, 1, 5.0, "1d4+1", 50.00, 7.2),
    GuideEntry("heavy", 2, 4, 2, 3.0, "1d4+1", 50.00, 9.2),
    GuideEntry("heavy", 2, 5, 2, 3.5, "1d4+1", 50.00, 11.2),
    GuideEntry("heavy", 3, 1, 1, 3.0, "1d4+1", 50.00, 4.8),
    GuideEntry("heavy", 3, 2, 1, 5.0, "1d4+1", 50.00, 7.8),
    GuideEntry("heavy", 3, 3, 1, 7.0, "1d4+1", 50.00, 10.8),
    GuideEntry("heavy", 3, 4, 2, 4.5, "1d4+1", 50.00, 13.8),
    GuideEntry("heavy", 3, 5, 2, 5.5, "1d4+1", 50.00, 16.8),
]

TARGETS = {
    (2, 1): 3.2,
    (2, 2): 5.2,
    (2, 3): 7.2,
    (2, 4): 9.2,
    (2, 5): 11.2,
    (3, 1): 4.8,
    (3, 2): 7.8,
    (3, 3): 10.8,
    (3, 4): 13.8,
    (3, 5): 16.8,
}


def pct(x: float) -> str:
    return f"{x * 100:.2f}%"


def print_hit_table(die_sides: tuple[int, ...] = DIE_SIDES) -> None:
    print("Achievable hit rates (single die vs AC 4, modifiers -5..+5)\n")
    print(f"{'Hit %':>8}  {'Roll':<10}  {'Die'}")
    print("-" * 32)
    for hit, roll in unique_hit_table(all_rolls(die_sides)):
        print(f"{hit:>7.2f}%  {roll.label:<10}  d{roll.sides}")

    d6_only = unique_hit_table(all_rolls((6,)))
    all_rates = unique_hit_table(all_rolls(die_sides))
    print(f"\nDistinct rates: {len(all_rates)} with {list(die_sides)}  vs  {len(d6_only)} with d6 only")


def audit_entries(
    entries: list[GuideEntry],
    die_sides: tuple[int, ...] = DIE_SIDES,
    label: str = "Guide audit",
) -> None:
    print(f"\n{label}")
    print("=" * 140)
    hdr = (
        f"{'P':>1} L {'M':>1}  {'Base':>4}  {'Guide roll':<10} {'Hit%':>7}  "
        f"{'Tgt/Rd':>8}  {'Act/Rd':>8}  {'Δ/Rd':>8}  "
        f"{'Ideal%':>7}  {'Best roll':<10} {'Best%':>7}  "
        f"{'Target':>6}  {'Actual':>7}  {'Δ tot':>6}"
    )
    print(hdr)
    print("-" * 140)

    mult = damage_multiplier(entries[0].archetype) if entries else float(ROUNDS)
    rounds = fight_rounds(entries[0].archetype) if entries else ROUNDS

    for e in entries:
        guide_roll = parse_roll(e.roll)
        guide_hit = guide_roll.hit_chance() if guide_roll else e.hit_pct / 100
        tgt_dpr = e.target_dpr
        act_dpr = e.actual_dpr(guide_hit)
        guide_out = act_dpr * rounds if e.archetype == "acid" else expected_damage(
            e.base_dmg, guide_hit, e.monsters, rounds
        )
        if e.archetype == "group":
            guide_out = act_dpr * rounds
        ideal = ideal_hit(e.target_dmg, e.base_dmg, e.monsters, int(mult))
        best = closest_roll(ideal, all_rolls(die_sides))
        best_hit = best.hit_chance()
        best_act_dpr = e.actual_dpr(best_hit)
        best_out = best_act_dpr * rounds

        flag = "  "
        if abs(best_hit - guide_hit) > 1e-6:
            flag = "⚠"
        print(
            f"{e.party} {e.level} {e.monsters}  {e.base_dmg:>4.1f}  {e.roll:<10} {pct(guide_hit):>7}  "
            f"{fmt_dpr(tgt_dpr):>8}  {fmt_dpr(act_dpr):>8}  {act_dpr - tgt_dpr:>+8.4f}  "
            f"{pct(ideal):>7}  {best.label:<10} {pct(best_hit):>7}  "
            f"{e.target_dmg:>6.1f}  {guide_out:>7.2f}  {guide_out - e.target_dmg:>+6.2f}{flag}"
        )


def print_solve_table(die_sides: tuple[int, ...] = DIE_SIDES) -> None:
    print("\nBest roll at each guide base (standard, 3 rounds)")
    print("=" * 128)
    print(
        f"{'P':>1} L {'M':>1}  {'Tgt/Rd':>8}  {'Base':>4}  {'Roll':<10} {'Hit%':>7}  "
        f"{'Act/Rd':>8}  {'Δ/Rd':>8}  {'Total':>7}  {'Δ tot':>6}  "
        f"{'d6 roll':<10} {'d6 Act/Rd':>9}  {'d6 Δ/Rd':>8}"
    )
    print("-" * 128)

    for e in GUIDE_STANDARD:
        tgt_dpr = e.target_dpr
        all_sol = solve_with_fixed_base(e.target_dmg, e.base_dmg, e.monsters, die_sides)
        act_dpr = actual_dmg_per_round(e.base_dmg, all_sol.actual_hit, e.monsters)
        d6_sol = solve_with_fixed_base(e.target_dmg, e.base_dmg, e.monsters, (6,))
        d6_act = actual_dmg_per_round(e.base_dmg, d6_sol.actual_hit, e.monsters)
        print(
            f"{e.party} {e.level} {e.monsters}  {fmt_dpr(tgt_dpr):>8}  {e.base_dmg:>4.1f}  "
            f"{all_sol.label:<10} {pct(all_sol.actual_hit):>7}  "
            f"{fmt_dpr(act_dpr):>8}  {act_dpr - tgt_dpr:>+8.4f}  "
            f"{all_sol.expected_dmg:>7.2f}  {all_sol.expected_dmg - e.target_dmg:>+6.2f}  "
            f"{d6_sol.label:<10} {fmt_dpr(d6_act):>9}  {d6_act - tgt_dpr:>+8.4f}"
        )


def compare_die_granularity() -> None:
    print("\nExample: P2 L1 standard — target 3.2 dmg, base 1.5 → ideal hit 71.11%\n")
    ideal = ideal_hit(3.2, 1.5)
    print(f"{'Die set':<20}  {'Closest roll':<12}  {'Hit %':>7}  {'Expected dmg':>12}  {'Δ from target':>14}")
    print("-" * 72)
    for sides in [(6,), (8,), (10,), (12,), (20,), DIE_SIDES]:
        roll = closest_roll(ideal, all_rolls(sides))
        out = expected_damage(1.5, roll.hit_chance())
        name = f"d{sides[0]} only" if len(sides) == 1 else "all dice"
        print(
            f"{name:<20}  {roll.label:<12}  {pct(roll.hit_chance()):>7}  {out:>12.2f}  {out - 3.2:>+14.2f}"
        )


def print_dice_reuse_summary() -> None:
    """Show how often each attack roll appears across all archetype tables."""
    from apply_guide_rolls import build_lookup

    lookup = build_lookup()
    counts: dict[str, list[str]] = {}
    for (arch, eid, _base), data in sorted(lookup.items()):
        counts.setdefault(data.roll, []).append(f"{arch} {eid}")

    print("\nDice roll reuse across all guide stat blocks")
    print("=" * 72)
    print(f"{'Roll':<12} {'Count':>5}  Used by")
    print("-" * 72)
    for roll, uses in sorted(counts.items(), key=lambda x: (-len(x[1]), x[0])):
        preview = ", ".join(uses[:4])
        if len(uses) > 4:
            preview += f", … (+{len(uses) - 4} more)"
        print(f"{roll:<12} {len(uses):>5}  {preview}")
    print(
        f"\n{len(counts)} distinct rolls across {len(lookup)} stat-block entries "
        f"({len(lookup) - len(counts)} reuse slots)"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit combat balance dice math")
    parser.add_argument("--table", action="store_true", help="Print achievable hit rate table")
    parser.add_argument("--solve", action="store_true", help="Solve optimal rolls for all targets")
    parser.add_argument("--d6-only", action="store_true", help="Restrict to d6 when solving")
    args = parser.parse_args()

    sides: tuple[int, ...] = (6,) if args.d6_only else DIE_SIDES

    if args.table:
        print_hit_table(sides)
        return

    if args.solve:
        print_solve_table(sides)
        return

    print("Combat balance audit — single die vs AC 4, 3-round standard fights")
    compare_die_granularity()
    print_hit_table(sides)
    audit_entries(GUIDE_STANDARD, sides, "Standard monsters (guide base dmg held fixed)")
    audit_entries(GUIDE_HEAVY, sides, "Heavy hitters (guide base dmg held fixed)")
    print_solve_table(sides)
    print_dice_reuse_summary()

    print(
        "\nNotes:"
        "\n  • Tgt/Rd = target damage per round (dmg_dealt ÷ rounds) — the rate needed to hit the HP target"
        "\n  • Act/Rd = base × monsters × hit% per round (acid uses ×5 total ÷ 3; group uses dmg/player × party)"
        "\n  • Ideal hit % = Tgt/Rd ÷ (base × monsters), then pick the closest single-die roll"
        "\n  • ⚠ = guide roll differs from best roll for that base + die set"
        "\n  • d6 only gives 7 distinct hit rates; d8/d10/d12/d20 add much finer steps"
    )


if __name__ == "__main__":
    main()
