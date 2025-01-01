__all__ = ["escape", "interpret"]

import string

# NOTE: The backslash needs to be LAST in the string for
#       interpret_double_quoted to work properly.
double_quote_special_characters = "$`\"\\"

def interpret(word):
    """Return the string represented by <word>.
    Interprets single quotes, double quotes and backslashes.
    Some characters with special meaning for bash, such as dollar signs
    and backticks, are left intact. There is nothing useful we could
    do with them anyway, except maybe flag an error.
    Syntax errors (dangling single backslashes or missing closing quotes)
    are silently corrected, which is useful if this is an incomplete word
    as is typically the case for the current word in tab completion."""

    if word.startswith("\""):
        return interpret_double_quoted(word)
    elif word.startswith("'"):
        return interpret_single_quoted(word)
    else:
        return interpret_standard(word)

def interpret_double_quoted(word):
    for char in double_quote_special_characters:
        word = word.replace("\\" + char, char)
    if word.endswith("\""):
        return word[1:-1]
    else:
        return word[1:]

def interpret_single_quoted(word):
    if word.endswith("'"):
        return word[1:-1]
    else:
        return word[1:]

def interpret_standard(word):
    num_trailing_backslashes = len(word) - len(word.rstrip("\\"))
    if num_trailing_backslashes % 2 == 1:
        word += "\\"
    result = []
    chars = iter(word)
    for char in chars:
        if char == "\\":
            char = next(chars)
        result.append(char)
    return "".join(result)


def escape(word, quoting=None):
    """Return <word> quoted in a way that it is safe for a bash prompt.
    If the optional <quoting> argument is used, it must be either a single
    quote character or double quote character (or evaluate to False,
    leading to the default behaviour).

    In that case, the resulting string will be single or double-quoted.
    Otherwise, backslash escapes are used.

    Raises a ValueError if single or double quoting is requested and
    the resulting string cannot be represented in the desired way.
    Every string can be reprented as a backslash escaped string, so
    no errors will be raised if the optional argument is not specified."""

    if quoting == "\"":
        return escape_double_quoted(word)
    elif quoting == "'":
        return escape_single_quoted(word)
    elif not quoting:
        return escape_standard(word)
    else:
        assert "bad 'quoting' argument: %r" % quoting

def escape_double_quoted(word):
    # Double-quoted strings may not contain "!"; it causes problems
    # with readline, but cannot be escaped.
    if word.count("!") != word.count("\\!"):
        raise ValueError
    # Within double-quoted strings, we need to escape dollars,
    # backslashes, double quotes, and backticks.
    return backslash_escape(word, double_quote_special_characters)

def escape_single_quoted(word):
    # Single-quoted strings may not contain single quotes.
    if "'" in word:
        raise ValueError
    # Apart from single quotes, they may contain every character,
    # and nothing needs to be quoted.
    return word

def escape_standard(word):
    return backslash_escape(word, "|&;()<>#\\'\"`!=$" + string.whitespace)

def backslash_escape(word, special_characters):
    result = []
    for char in word:
        if char in special_characters:
            result.append("\\")
        result.append(char)
    return "".join(result)
