#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys


def report(infile, prefix):
    offending_lines = []
    for line_no, line in enumerate(infile):
        try:
            unicode(line)
        except UnicodeDecodeError:
            offending_lines.append(line)
            print "%s%6d: %r" % (prefix, line_no + 1, line)

    if offending_lines:
        print "-" * 72
        print "offending lines found: trying to convert to UTF-8"
        all_ok = True
        offending_characters = set()
        for line in offending_lines:
            try:
                conv_line = unicode(line, "utf-8")
            except UnicodeDecodeError:
                print "failed: %r" % line
                all_ok = False
            else:
                for char in conv_line:
                    if ord(char) >= 127:
                        offending_characters.add(char)
        if all_ok:
            print "OK."
            print "-" * 72
            print "non-ASCII characters found:"
            for char in sorted(offending_characters, key=ord):
                print "%r = #%d = %s" % (char, ord(char), char)


def main():
    args = sys.argv[1:]
    if args:
        for filename in args:
            with open(filename) as infile:
                report(infile, "%s: " % filename)
    else:
        report(sys.stdin, "")


if __name__ == "__main__":
    main()
