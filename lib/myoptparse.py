import optparse
import sys
import textwrap

class OptionParser(optparse.OptionParser):
    """Extends and modifies optparse.OptionParser in three ways:

    1. On error, we print a message to inform the user how they can
        get help in addition to the normal usage message. Use the
        'help' keyword argument to the constructor to customize the
        message or just use the default.
    2. If the command description contains several paragraphs, separated
        by blank lines, we wrap them separately and print them properly.
    3. The description string is dedented in such a way that triple-quoted
        strings like this one are aligned properly."""

    help_msg = 'Try "%prog --help" for more information.'

    def __init__(self, *args, **kwargs):
        if "help" in kwargs:
            self.help_msg = kwargs["help"]
            del kwargs[help]

        if "description" in kwargs:
            description = kwargs["description"]
            lines = description.splitlines()
            if len(lines) >= 2:
                leading_spaces = " " * (len(lines[1]) - len(lines[1].lstrip(" ")))
                description = textwrap.dedent(leading_spaces + description)
                kwargs["description"] = description

        optparse.OptionParser.__init__(self, *args, **kwargs)

    def error(self, msg):
        self.print_usage(sys.stderr)
        error_msg = "%s: error: %s" % (self.get_prog_name(), msg)
        help_msg = self.help_msg.replace("%prog", self.get_prog_name())
        self.exit(2, "%s\n\n%s\n" % (error_msg, help_msg))

    def format_description(self, formatter):
        return "\n".join(self.formatter.format_description(paragraph)
                         for paragraph in self.get_description().split("\n\n"))
