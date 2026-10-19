"""Report environment variable usage."""
import json


def report(used: dict, documented: set, fmt: str = "text") -> None:
    used_set = set(used)
    undocumented = sorted(used_set - documented) if documented else []
    unused = sorted(documented - used_set) if documented else []

    if fmt == "json":
        out = {
            "used": sorted(used_set),
            "used_locations": used,
            "documented": sorted(documented),
            "undocumented": undocumented,
            "unused": unused,
        }
        print(json.dumps(out, indent=2))
        return

    print(f"Environment variables referenced in code: {len(used_set)}")
    for v in sorted(used_set):
        locs = used[v]
        noun = "file" if len(locs) == 1 else "files"
        print(f"  {v}  ({len(locs)} {noun})")

    if documented:
        print()
        if undocumented:
            print(f"Undocumented (used in code, not in env file): {len(undocumented)}")
            for v in undocumented:
                print(f"  - {v}")
        else:
            print("No undocumented variables.")
        if unused:
            print(f"Unused (in env file, not referenced in code): {len(unused)}")
            for v in unused:
                print(f"  - {v}")
        else:
            print("No unused variables.")