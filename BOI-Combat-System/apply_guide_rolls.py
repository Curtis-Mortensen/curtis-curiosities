#!/usr/bin/env python3
"""Apply optimal single-die rolls (all D&D dice) to combat-balance-guide.html."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from combat_balance_audit import (
    DIE_SIDES,
    LIFESTEAL_HEAL_PER_HIT,
    LIFESTEAL_ROUNDS,
    TARGETS,
    actual_dmg_per_round,
    all_rolls,
    closest_roll,
    fmt_dpr,
    fmt_hp_each,
    fmt_hp_value,
    lifesteal_four_round_budget,
    lifesteal_listed_hp,
    target_dmg_per_round,
    unique_hit_table,
)

GUIDE_PATH = Path(__file__).parent / "combat-balance-guide.html"

ARCHETYPE_CODES: dict[str, int] = {
    "standard": 11,
    "heavy": 12,
    "acid": 13,
    "group": 14,
    "lifesteal": 15,
    "splitter": 16,
}


@dataclass(frozen=True)
class RollData:
    roll: str
    hit_str: str
    hit_class: str
    target_dpr: str
    actual_dpr: str
    hit_f: float = 0.0
    listed_hp: str = ""
    heal_per_hit: str = ""


def encounter_id(party: int, level: int, archetype: str) -> str:
    return f"{party:03d}{level}{ARCHETYPE_CODES[archetype]:02d}"


def parse_encounter_id(eid: str) -> tuple[int, int]:
    return int(eid[:3]), int(eid[3])


def hit_class(archetype: str, hit: float) -> str:
    p = hit * 100
    if archetype == "heavy":
        return "hit-ok" if 43 <= p <= 57 else "hit-warn"
    if archetype in ("acid", "group"):
        if p >= 70:
            return "hit-ok"
        if p >= 65:
            return "hit-warn"
        return "hit-low"
    if p >= 70:
        return "hit-ok"
    if p >= 65:
        return "hit-warn"
    return "hit-low"


def fmt_hit(hit: float) -> str:
    return f"{hit * 100:.2f}%"


def ideal_hit(
    target: float,
    base: float,
    monsters: int,
    rounds: int,
    party: int,
    group_dpp: bool = False,
) -> float:
    if group_dpp:
        return target / (rounds * base * party)
    return target / (rounds * base * monsters)


def build_lookup() -> dict[tuple[str, str, float], RollData]:
    """(archetype, encounter_id, base) -> roll assignment with per-round damage."""
    lookup: dict[tuple[str, str, float], RollData] = {}

    def add(
        arch: str,
        party: int,
        lvl: int,
        monsters: int,
        base: float,
        rounds: int,
        class_arch: str | None = None,
        group: bool = False,
    ) -> None:
        eid = encounter_id(party, lvl, arch)
        target = TARGETS[(party, lvl)]
        ideal = ideal_hit(target, base, monsters, rounds, party, group)
        roll = closest_roll(ideal)
        hit_f = roll.hit_chance()
        ha = class_arch or arch
        fight_rounds = LIFESTEAL_ROUNDS if arch == "lifesteal" else 3
        hp_total = lifesteal_listed_hp(party, monsters, hit_f) if arch == "lifesteal" else 0.0
        lookup[(arch, eid, base)] = RollData(
            roll=roll.label,
            hit_str=fmt_hit(hit_f),
            hit_class=hit_class(ha, hit_f),
            target_dpr=fmt_dpr(target_dmg_per_round(target, fight_rounds)),
            actual_dpr=fmt_dpr(
                actual_dmg_per_round(
                    base, hit_f, monsters, party=party, archetype=arch
                )
            ),
            hit_f=hit_f,
            listed_hp=fmt_hp_each(hp_total, monsters) if arch == "lifesteal" else "",
            heal_per_hit=fmt_hp_value(LIFESTEAL_HEAL_PER_HIT) if arch == "lifesteal" else "",
        )

    for party in (2, 3):
        std = (
            [(1, 1, 1.5), (2, 1, 2.0), (3, 1, 3.0), (4, 2, 2.0), (5, 2, 2.5)]
            if party == 2
            else [(1, 1, 2.0), (2, 1, 3.0), (3, 1, 4.5), (4, 2, 3.0), (5, 2, 3.5)]
        )
        hvy = (
            [(1, 1, 2.0), (2, 1, 3.5), (3, 1, 5.0), (4, 2, 3.0), (5, 2, 3.5)]
            if party == 2
            else [(1, 1, 3.0), (2, 1, 5.0), (3, 1, 7.0), (4, 2, 4.5), (5, 2, 5.5)]
        )
        acd = (
            [(1, 1, 1.0), (2, 1, 1.5), (3, 1, 2.0), (4, 2, 1.0), (5, 2, 1.5)]
            if party == 2
            else [(1, 1, 1.0), (2, 1, 2.0), (3, 1, 3.0), (4, 2, 1.5), (5, 2, 2.0)]
        )
        grp = [(1, 1, 1.0), (2, 1, 1.0), (3, 1, 1.5), (4, 2, 2.0), (5, 2, 2.5)]
        lst = (
            [(1, 1, 1.5), (2, 1, 2.0), (3, 1, 3.5), (4, 2, 4.0), (5, 2, 4.5)]
            if party == 2
            else [(1, 1, 2.0), (2, 1, 3.0), (3, 1, 4.0), (4, 2, 4.0), (5, 2, 4.5)]
        )
        for lvl, mon, base in std:
            add("standard", party, lvl, mon, base, 3)
            add("splitter", party, lvl, mon, base, 3)
        for lvl, mon, base in hvy:
            add("heavy", party, lvl, mon, base, 3)
        for lvl, mon, base in acd:
            add("acid", party, lvl, mon, base, 5, "acid")
        for lvl, mon, base in grp:
            add("group", party, lvl, mon, base, 3, "group", group=True)
        for lvl, mon, base in lst:
            add("lifesteal", party, lvl, mon, base, 4)

    return lookup


def hit_table_html() -> str:
    lines = []
    for hit, roll in unique_hit_table(all_rolls(DIE_SIDES)):
        lines.append(
            f'          <tr><td class="num">{hit:.2f}%</td>'
            f'<td><code>{roll.label}</code></td>'
            f"<td>Die + modifier ≥ 4</td></tr>"
        )
    return "\n".join(lines)


def update_dice_section(html: str) -> str:
    start = html.index("    <!-- DICE & HIT CHANCE -->")
    end = html.index("    <!-- ASSUMPTIONS -->")
    new_section = f"""    <!-- DICE & HIT CHANCE -->
    <section id="dice">
      <h2>Dice &amp; Hit Chance</h2>
      <p>
        Monster attacks are not free-floating percentages — they come from <strong>actual dice rolls</strong>.
        Each attack rolls <strong>one die</strong> (any standard D&amp;D die: d4, d6, d8, d10, d12, or d20)
        with a <strong>+/− modifier</strong>, then checks whether the result meets or beats the player's
        <strong>AC of 4</strong>.
      </p>

      <div class="formula-box">
        <div class="label">Attack roll (meets or beats)</div>
        Roll 1dX with modifier (+/− X), where X is 4, 6, 8, 10, 12, or 20.<br>
        <strong>(die result + modifier) ≥ 4</strong> → hit.<br><br>
        Equivalent: the die must show ≥ (4 − modifier) on its face.
      </div>

      <div class="callout blue">
        <strong>Example: 1d10 vs AC 4</strong>
        No modifier means the die needs to show ≥ 4. Faces 4–10 succeed (7 of 10).
        Probability = 7/10 = <strong>70.00%</strong>.
      </div>

      <h3>All Achievable Hit Percentages</h3>
      <p class="muted">
        Using one die (d4–d20) and modifiers from −5 to +5 against AC 4, these are the distinct hit rates.
        Stat blocks pick the roll whose percentage is <strong>closest to the mathematical target</strong>
        (ties broken by fewer sides on the die, then smaller modifier). Run <code>combat_balance_audit.py</code>
        to verify any assignment.
      </p>

      <table>
        <thead>
          <tr><th>Hit %</th><th>Attack Roll</th><th>Rule</th></tr>
        </thead>
        <tbody>
{hit_table_html()}
        </tbody>
      </table>
      <p class="muted">
        <strong>Note:</strong> Larger dice (d10, d12, d20) give finer steps than d6 alone — e.g. 70% via
        <code>1d10</code> vs d6's nearest options of 66.67% or 83.33%. Prefer the die type that lands
        closest to the target hit chance.
      </p>
    </section>


"""
    return html[:start] + new_section + html[end:]


def update_formula_section(html: str) -> str:
    old = """      <h3>Standard monster: damage per turn</h3>
      <div class="formula-box">
        <div class="label">Standard archetype</div>
        Raw Monster Dmg = Dmg Dealt ÷ 3<br>
        Hit Chance = Dmg Dealt ÷ (3 × Base Damage)
      </div>
      <p>
        Pick a <strong>Base Damage</strong> (rounded to the nearest 0.5 step), then solve for the
        hit chance that makes average output match the target. Standard monsters aim for
        <strong>70% or higher</strong> hit chance.
      </p>"""

    new = """      <h3>Standard monster: damage per turn</h3>
      <div class="formula-box">
        <div class="label">Standard archetype</div>
        Target Dmg/Round = Dmg Dealt ÷ 3<br>
        Actual Dmg/Round = Base Damage × Monsters × Hit%<br>
        Hit Chance = Target Dmg/Round ÷ (Base Damage × Monsters)<br><br>
        Example: need 1.7333 dmg/round with Base 2.0 → ideal hit 86.67% → <code>1d8+2</code> at 87.50%
        gives Actual/Rd = 1.7500 (exact over 3 rounds).
      </div>
      <p>
        Pick a <strong>Base Damage</strong> (rounded to the nearest 0.5 step), then solve for the
        hit chance that makes <strong>Actual Dmg/Round</strong> closest to the target. Standard monsters aim for
        <strong>70% or higher</strong> hit chance.
      </p>"""

    if old in html:
        return html.replace(old, new)
    return html


def parse_base_from_row(row: str) -> float | None:
    m = re.search(r'class="num">([\d.]+)(?:\s+ea\.)?</td>\s*<td><code>', row)
    if m:
        return float(m.group(1))
    m = re.search(
        r'class="num">([\d.]+)(?:\s+ea\.)?</td>\s*<td class="num">[\d.]+</td>\s*<td><code>',
        row,
    )
    if m:
        return float(m.group(1))
    return None


def dpr_cells(target_dpr: str, actual_dpr: str) -> str:
    return f'<td class="num">{target_dpr}</td><td class="num">{actual_dpr}</td>'


def inject_dpr_after_hit(row: str, target_dpr: str, actual_dpr: str) -> str:
    cells = dpr_cells(target_dpr, actual_dpr)
    hit_m = re.search(r'class="num hit-[^"]+">[^<]+</td>', row)
    if not hit_m:
        return row
    pos = hit_m.end()
    rest = row[pos:]
    existing = re.match(
        r"\s*<td class=\"num\">\d+\.\d{4}</td>\s*<td class=\"num\">\d+\.\d{4}</td>",
        rest,
    )
    if existing:
        rest = rest[existing.end() :]
        return row[:pos] + cells + rest
    return row[:pos] + cells + rest


def ensure_table_headers(section: str) -> str:
    replacements = [
        (
            "<th>Hit %</th><th>Dmg Dealt</th>",
            "<th>Hit %</th><th>Target/Rd</th><th>Actual/Rd</th><th>Dmg Dealt</th>",
        ),
        (
            "<th>Hit %</th><th>Acid/turn</th><th>Dmg Dealt</th>",
            "<th>Hit %</th><th>Target/Rd</th><th>Actual/Rd</th><th>Acid/turn</th><th>Dmg Dealt</th>",
        ),
        (
            "<th>Hit %</th><th>Steal %</th><th>Dmg Dealt</th>",
            "<th>Hit %</th><th>Target/Rd</th><th>Actual/Rd</th><th>Heal/Hit</th><th>Dmg Dealt</th>",
        ),
        (
            "<th>Hit %</th><th>Target/Rd</th><th>Actual/Rd</th><th>Steal %</th><th>Dmg Dealt</th>",
            "<th>Hit %</th><th>Target/Rd</th><th>Actual/Rd</th><th>Heal/Hit</th><th>Dmg Dealt</th>",
        ),
    ]
    for old, new in replacements:
        section = section.replace(old, new)
    return section


def update_lifesteal_row(row: str, data: RollData) -> str:
    """Update HP ea. and heal/hit columns in a lifesteal table row."""
    row = re.sub(
        r'(<td class="center">\d+</td>\s*<td class="center"><code>\d{6}</code></td>'
        r'\s*<td class="center">\d+</td>\s*<td class="num">)[^<]+',
        lambda m: f"{m.group(1)}{data.listed_hp}",
        row,
        count=1,
    )
    row = re.sub(
        r'(<td class="num">\d+\.\d{4}</td>\s*<td class="num">)[^<]+'
        r'(</td>\s*<td class="num">[\d.]+</td></tr>)',
        lambda m: f"{m.group(1)}{data.heal_per_hit}{m.group(2)}",
        row,
        count=1,
    )
    return row


def update_lifesteal_stat_block(section: str, data: RollData, eid: str, party: int) -> str:
    """Refresh HP and heal-on-hit fields in lifesteal stat blocks."""
    hp_key = "HP each" if " / " in data.listed_hp else "HP"
    hp_display = data.listed_hp.replace(" / ", " & ")
    budget = fmt_hp_value(lifesteal_four_round_budget(party))

    section = re.sub(
        rf"(ID {eid} · Party of {party}[\s\S]*?"
        rf'<div class="stat-row"><span class="key">{hp_key}</span><span class="val">)[^<]+',
        lambda m: f"{m.group(1)}{hp_display}",
        section,
        count=1,
    )
    section = re.sub(
        rf"(ID {eid} · Party of {party}[\s\S]*?"
        rf'<div class="stat-row"><span class="key">)(?:Lifesteal|Heal on Hit)(</span><span class="val">)[^<]+',
        lambda m: f"{m.group(1)}Heal on Hit{m.group(2)}{data.heal_per_hit}",
        section,
        count=1,
    )
    section = re.sub(
        rf"(ID {eid} · Party of {party}[\s\S]*?"
        rf'<div class="stat-row"><span class="key">4-Round Budget</span><span class="val">)[^<]+',
        lambda m: f"{m.group(1)}{budget}",
        section,
        count=1,
    )
    return section


def update_stat_blocks(section: str, archetype: str, lookup: dict) -> str:
    for key, data in lookup.items():
        arch_k, eid, base = key
        if arch_k != archetype:
            continue
        party, _level = parse_encounter_id(eid)
        marker = f'Target/Rd</span><span class="val">{data.target_dpr}</span>'
        id_block = re.search(
            rf"ID {eid} · Party of {party}[\s\S]*?Target Dmg</span>", section
        )
        if not (id_block and marker in id_block.group(0)):
            dpr_rows = (
                f'<div class="stat-row"><span class="key">Target/Rd</span>'
                f'<span class="val">{data.target_dpr}</span></div>\n            '
                f'<div class="stat-row"><span class="key">Actual/Rd</span>'
                f'<span class="val">{data.actual_dpr}</span></div>\n            '
            )
            pat = (
                rf"(<div class=\"stat-header\">[\s\S]*?ID {eid} · Party of {party}"
                rf"[\s\S]*?<div class=\"stat-body\">[\s\S]*?"
                rf")(<div class=\"stat-row\"><span class=\"key\">Target Dmg</span>)"
            )
            section, _ = re.subn(pat, rf"\1{dpr_rows}\2", section, count=1)

        base_strs = {str(base), f"{base:.1f}"}
        if base == int(base):
            base_strs.add(str(int(base)))
        for bstr in base_strs:
            pat2 = (
                rf"(ID {eid} · Party of {party}[\s\S]*?"
                rf"(?:Base Dmg each|Base Dmg|Dmg / Player)</span><span class=\"val\">){re.escape(bstr)}"
                rf"([\s\S]*?Attack Roll</span><span class=\"val\"><code>)[^<]*"
                rf"(</code></span>[\s\S]*?Hit Chance</span><span class=\"val )hit-[^\"]+(\"[^>]*>)[^<]*"
                rf"(</span>)"
            )

            def repl2(m: re.Match, _data=data) -> str:
                return (
                    f"{m.group(1)}{bstr}{m.group(2)}{_data.roll}{m.group(3)}"
                    f"{_data.hit_class}{m.group(4)}{_data.hit_str}{m.group(5)}"
                )

            section, n = re.subn(pat2, repl2, section, count=1)
            if n:
                break
        if archetype == "lifesteal":
            section = update_lifesteal_stat_block(section, data, eid, party)
    return section


def update_section_tables(html: str, section_id: str, archetype: str) -> str:
    lookup = build_lookup()
    section_re = re.compile(
        rf'(<section id="{section_id}">.*?)(</section>)',
        re.DOTALL,
    )
    m = section_re.search(html)
    if not m:
        return html
    section = m.group(1)
    section = ensure_table_headers(section)

    def replace_row(row_m: re.Match) -> str:
        row = row_m.group(0)
        id_m = re.search(r"<code>(\d{6})</code>", row)
        if not id_m:
            return row
        eid = id_m.group(1)
        base = parse_base_from_row(row)
        if base is None:
            return row
        key = (archetype, eid, base)
        if key not in lookup:
            return row
        data = lookup[key]
        row = re.sub(
            r"<td><code>[^<]+</code>",
            f"<td><code>{data.roll}</code>",
            row,
            count=1,
        )
        row = re.sub(
            r'class="num hit-[^"]+">[^<]+</td>',
            f'class="num {data.hit_class}">{data.hit_str}</td>',
            row,
            count=1,
        )
        row = inject_dpr_after_hit(row, data.target_dpr, data.actual_dpr)
        if archetype == "lifesteal":
            row = update_lifesteal_row(row, data)
        return row

    section = re.sub(r"<tr>.*?</tr>", replace_row, section, flags=re.DOTALL)
    section = update_stat_blocks(section, archetype, lookup)
    return html[: m.start(1)] + section + html[m.end(1) :]


def update_misc(html: str) -> str:
    html = html.replace(
        "<li><strong>Assign a dice roll</strong> — choose the 1d6±X roll whose hit % is closest to the target.</li>",
        "<li><strong>Assign a dice roll</strong> — choose the single 1dX±M roll whose hit % is closest to the target.</li>",
    )
    html = re.sub(
        r"66\.67% \(<code>1d6\+1</code>\)",
        "70.00% (<code>1d10</code>)",
        html,
    )
    html = re.sub(
        r"83\.33% \(<code>1d6\+2</code>\)",
        "80.00% (<code>1d10+1</code>)",
        html,
    )
    html = re.sub(
        r"<strong>Chosen: Base 1\.0 @ <code>1d6\+1</code> \(66\.67%\)\.</strong>",
        "<strong>Chosen: Base 1.0 @ <code>1d20-4</code> (65.00%).</strong>",
        html,
    )
    html = re.sub(
        r"<strong>Alternative:</strong> <code>1d6</code> at 50%",
        "<strong>Alternative:</strong> <code>1d4+1</code> at 50%",
        html,
    )
    html = re.sub(
        r"Ideal hit 64% — closest single die: <code>1d6\+1</code> \(66\.67%\)",
        "Ideal hit 64% — closest single die: <code>1d20-4</code> (65.00%)",
        html,
    )
    return html


def main() -> None:
    html = GUIDE_PATH.read_text()
    html = update_dice_section(html)
    html = update_formula_section(html)
    for sid, arch in [
        ("standard", "standard"),
        ("heavy", "heavy"),
        ("acid", "acid"),
        ("group", "group"),
        ("lifesteal", "lifesteal"),
        ("splitter", "splitter"),
    ]:
        html = update_section_tables(html, sid, arch)
    html = update_misc(html)
    GUIDE_PATH.write_text(html)
    print(f"Updated {GUIDE_PATH}")


if __name__ == "__main__":
    main()
