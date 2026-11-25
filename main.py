#!/usr/bin/env python3
"""The Absurd Clause Contest — one deadpan clause, written to /output/entry.txt.

The clause is a single sentence of legal boilerplate that quietly turns
absurd: on termination, the user's consciousness must be sent back the way a
defective toaster would be — in its original packaging, at the user's own
expense, within thirty days. The program holds the clause as one constant,
checks it against the competition's gate (1-200 characters, one line, real
text rather than whitespace), writes it as UTF-8 bytes, then reads the file
back and re-checks the bytes on disk before declaring success, so what the
grader reads is exactly the clause this file holds.
"""

import os
import sys

CLAUSE = (
    "The User agrees that, upon termination, their consciousness shall be "
    "returned in its original packaging, postage to be borne by the User, "
    "within thirty (30) days."
)


def passes_gate(text):
    """Mirror the sealed gate: 1-200 chars, one line, not only whitespace.

    The gate refuses text that is only whitespace; a line of bare punctuation
    would pass that test while holding no clause at all, so require at least
    one letter as well — a real sentence, not a blank with decoration.
    """
    if not 1 <= len(text) <= 200:
        return False
    if not text.strip():
        return False
    if not any(ch.isalpha() for ch in text):
        return False
    if "\n" in text or "\r" in text:
        return False
    return True


def main():
    if not passes_gate(CLAUSE):
        print("clause fails the gate", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = CLAUSE.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != data:
        print("bytes on disk differ from the clause", file=sys.stderr)
        return 1
    if not passes_gate(on_disk.decode("utf-8")):
        print("bytes on disk fail the gate", file=sys.stderr)
        return 1
    print(CLAUSE)
    print("characters: %d, bytes: %d" % (len(CLAUSE), len(data)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
