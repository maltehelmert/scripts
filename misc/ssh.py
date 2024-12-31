#! /usr/bin/env python2

"""Transparent ssh proxy that replaces certain host names with others
if certain ports are open. Meant to be used together with the thor
script and suitable entries in .ssh/config to allow using the same ssh
hostnames whether or not we're using the VPN. This is especially
useful in conjunction with svn+ssh.

Limitation: the heuristics we use to decide where the ssh options end
(and hence where the hostname is located on the command line) are
pretty simplisistic and definitely not generally sufficient. They have
been chosen to be good enough for our main purpose, which is to enable
use of svn+ssh."""


import errno
import os.path
import socket
import sys


VERBOSITY = 1  # Set to 0 (silent), 1 (normal) or 2 (verbose)

SUBSTITUTIONS = [
    (34318, "kibo", "kibo-tunnel"),
    (34319, "maia", "maia-tunnel"),
    ]


def is_port_open(port):
    sock = socket.socket()
    try:
        sock.connect(("localhost", port))
    except socket.error, e:
        if e.errno == errno.ECONNREFUSED:
            return False
        else:
            raise
    else:
        sock.close()
        return True


def identify_host_arg_no(args):
    skip_next = False
    for pos, arg in enumerate(args):
        if skip_next:
            skip_next = False
        else:
            if arg == "-o":
                skip_next = True
            elif arg.startswith("-"):
                pass
            else:
                return pos
    return None


def main():
    args = sys.argv[1:]
    host_arg_no = identify_host_arg_no(args)
    if host_arg_no is not None:
        for (port, host, subst_host) in SUBSTITUTIONS:
            if args[host_arg_no] == host and is_port_open(port):
                if VERBOSITY >= 1:
                    print >> sys.stderr, "[%s] substituting %s for %s" % (
                        os.path.basename(sys.argv[0]), subst_host, host)
                args[host_arg_no] = subst_host
                break
    if VERBOSITY >= 2:
        print >> sys.stderr, "[args = %r]" % (args,)
    os.execl("/usr/bin/ssh", "ssh", *args)


if __name__ == "__main__":
    main()
