import sys
import traceback

import bashtools

## Bash completion.
##
## To set this up, source the following code with bash:
##
##     _my_py_complete()
##     {
##         local IFS=$'\n'
##         COMPREPLY=( $( "$1" --bashcomplete \
##                        "$2" "$3" $COMP_POINT "$COMP_LINE" \
##                        $COMP_CWORD "${COMP_WORDS[@]}" ) )
##     }
##     complete -o default -F _my_py_complete program_name
##
## where program_name is the name fo the program to complete for
## (using the basename is sufficient).
##
## The program should call handle_completion with a callback function
## that receives a Completer object and calls complete_list,
## complete_file, complete_none or raises an exception to program the
## completion.
##
## Usually, the callback should only need to look at word_no and words
## to decide what to do. The input words are properly unescaped and
## the output words (passed to complete_list) are properly escaped, so
## that the calling program should not need to worry about bash escaping.

debug_filename = None

def handle_completion(callback):
    if len(sys.argv) >= 2 and sys.argv[1] == "--bashcomplete":
        try:
            completer = Completer(sys.argv[2:])
        except ValueError as e:
            raise SystemExit(str(e))
        completer.log()
        try:
            callback(completer)
        except Exception as e:
            completer._complete_error(e)
        raise SystemExit

def debug(line):
    if debug_filename:
        print(line, file=open(debug_filename, "a"))

class Completer(object):
    def __init__(self, args):
        try:
            prefix = args[0]
            previous_word = args[1]
            position = int(args[2])
            line = args[3]
            word_no = int(args[4])
            words = args[5:]
            if not 0 <= position <= len(line):
                raise ValueError
            if not 1 <= word_no < len(words):
                raise ValueError
            if previous_word != words[word_no - 1]:
                raise ValueError
        except (ValueError, IndexError):
            raise ValueError("bad arguments for completion: %r" % args)

        self._quoting_mode = self._get_quoting_mode(words[word_no])
        self.prefix = bashtools.interpret(self._quoting_mode + prefix)
        self._line = line
        self._position = position
        self.words = [bashtools.interpret(word) for word in words]
        self.word_no = word_no

    def log(self):
        debug("-----------------------------------------------")
        debug("prefix:   %r" % self.prefix)
        debug("line:     %r" % self._line)
        debug("position: %d" % self._position)
        debug("words:    %r" % self.words)
        debug("word no:  %d" % self.word_no)

    def complete_list(self, candidates):
        matches = [candidate for candidate in candidates
                   if candidate.startswith(self.prefix)]
        if not matches:
            self.complete_none()
        else:
            try:
                escaped_words = [self._escape_match(word) for word in matches]
            except ValueError:
                # If there is any word that cannot be escaped (which can
                # only be the case if single or double quoting is requested
                # and unusual characters are used), we give no matches.
                # Otherwise, we would give the false impression that only the
                # printed completions were possible matches.
                self.complete_none()
            else:
                for word in escaped_words:
                    print(word)

    def complete_file(self):
        # Don't print anything. Bash will handle this with file
        # completion if this is set up properly.
        pass

    def complete_none(self):
        # If there are no matches, print something to keep bash
        # from using filename completion.
        print(" ")
        print("[no completions]")

    def _complete_error(self, error):
        print(" ")
        print("[error: %s]" % error)
        debug(traceback.format_exc())

    def _escape_match(self, word):
        # Note: We need to match the quoting mode of the input to work
        # around Bash's behaviour of preserving that quoting.
        # For example, if we hit TAB on the word {"Fo} and return
        # {Foo\ Bar}, then bash will preserve the double-quote, resulting
        # in {"Foo\ Bar"}, which is not what we want, because the backslash
        # will be interpreted as part of the word!
        return bashtools.escape(word, self._quoting_mode)

    def _get_quoting_mode(self, word):
        if word and word[0] in "'\"":
            return word[0]
        else:
            return ""
