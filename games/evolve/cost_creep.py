#! /usr/bin/env python3


def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    assert minutes == int(minutes)
    minutes = int(minutes)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    parts = []
    unit = None
    if days:
        parts.append(f"{days} days")
        unit = "days"
    if unit or hours:
        if not unit:
            parts.append(f"{hours}")
        else:
            parts.append(f", {hours:02d}")
        unit = "hours"
    if unit or minutes:
        if not unit:
            unit = "minutes"
            parts.append(f"{minutes}")
        else:
            parts.append(f":{minutes:02d}")
    if seconds:
        if not unit:
            unit = "seconds"
            parts.append(f"{seconds:.2f}")
        else:
            parts.append(f":{seconds:05.2f}")
    return "".join(parts) + " " + unit


def print_statistics(what, starting_cost_in_seconds, creep, already_built, wanted):
    print(f"{wanted} {what}:")
    total = 0
    current = starting_cost_in_seconds * creep ** already_built
    for n in range(already_built + 1, wanted + 1):
        total += current
        total_duration = format_duration(total)
        current_duration = format_duration(current)
        print(f"build #{n}: {total_duration} total; {current_duration} for this one")
        current *= creep


def main():
    print_statistics(
        what="supercolliders",
        starting_cost_in_seconds=40000 / 1300,
        creep=1.045,
        already_built=98,
        wanted=99,
    )
    print()
    print_statistics(
        what="mana syphons",
        starting_cost_in_seconds=10000 / 40.48,
        creep=1.025,
        already_built=59,
        wanted=80,
        )


if __name__ == "__main__":
    main()
