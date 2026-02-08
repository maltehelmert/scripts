#! /usr/bin/env python3

import sys


def report(infile, prefix):
    offending_lines = []
    for line_no, line in enumerate(infile):
        try:
            line.decode("ascii")
        except UnicodeDecodeError:
            offending_lines.append(line)
            print(f"{prefix}{line_no + 1:6d}: {line!r}")

    if offending_lines:
        print("-" * 72)
        print("offending lines found: checking if they work as UTF-8")
        all_ok = True
        offending_characters = set()
        for line in offending_lines:
            try:
                conv_line = line.decode("utf-8")
            except UnicodeDecodeError:
                print(f"failed: {line!r}")
                all_ok = False
            else:
                for char in conv_line:
                    if ord(char) >= 127:
                        offending_characters.add(char)
        if all_ok:
            print("OK.")
            print("-" * 72)
            print("non-ASCII characters found:")
            for char in sorted(offending_characters, key=ord):
                print(f"{char!r} = #{ord(char)} = {char}")


def main():
    args = sys.argv[1:]
    if args:
        for filename in args:
            with open(filename, "rb") as infile:
                report(infile, f"{filename}: ")
    else:
        report(sys.stdin.buffer, "")


if __name__ == "__main__":
    main()
