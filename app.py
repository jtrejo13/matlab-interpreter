"""
Filename:    app.py
Description: An interactive shell for the MATLAB Interpreter
Author:      Juan Trejo
Github:      https://github.com/jtrejo13
"""

# -------
# imports
# -------

import sys
import traceback
import Interpreter
import wx
import wx.py


sys.tracebacklimit = 1  # only display the last traceback error


welcome_txt = """
                    < M A T L A B  I N T E R P R E T E R (R) >
                            Copyright 2017 Juan Trejo
                               Version 1.0 (R2017a)
                                   Nov 26, 2017

For code information, visit www.github.com/jtrejo13/matlab-interpreter
"""


class MyInteractiveInterpreter(object):
    """
    This class deals with parsing and interpreter state (the user's
    namespace); it doesn't deal with input buffering or prompting or
    input file naming (the filename is always passed in explicitly).
    """

    def __init__(self, locals=locals):
        """Constructor.

        The optional 'locals' argument specifies the dictionary in
        which code will be executed; it defaults to a newly created
        dictionary with key "__name__" set to "__console__" and key
        "__doc__" set to None.
        """

        if locals is None:
            locals = {"__name__": "__console__", "__doc__": None}
        self.locals = locals

    def runsource(self, source, filename="<stdin>", symbol="single"):
        """Compile and run some source in the interpreter.

        One several things can happen:

        1) The input is incorrect; interp_read() raised an
        exception (SyntaxError).  A syntax traceback
        will be printed by calling the showsyntaxerror() method.

        2) TODO: The input is incomplete, and more input is required;
        interp_read() returned None.  Nothing happens.

        3) The input is complete; interp_read() returned a parser
        object.  The parser is executed by calling self.runcode() (which
        also handles run-time exceptions, except for SystemExit).

        The return value is True in case 2, False in the other cases (unless
        an exception is raised).  The return value can be used to
        decide whether to use sys.ps1 or sys.ps2 to prompt the next
        line.
        """
        try:
            parser = Interpreter.interp_read(source.strip())
        except (OverflowError, SyntaxError, ValueError):
            # Case 1
            self.showsyntaxerror(filename)
            return False

        if parser is None:
            # Case 2
            return True

        # Case 3
        self.runcode(parser)
        return False

    def runcode(self, parser):
        """Execute a parser object.

        When an exception occurs, self.showtraceback() is called to
        display a traceback.  All exceptions are caught except
        SystemExit, which is reraised.

        A note about KeyboardInterrupt: this exception may occur
        elsewhere in this code, and may not always be caught.  The
        caller should be prepared to deal with it.
        """
        try:
            result = Interpreter.interp_eval(parser)
            Interpreter.interp_print(sys.stdout, result)
        except SystemExit:
            print('SystemExit')
            raise
        except:
            self.showtraceback()

    def showsyntaxerror(self, filename=None):
        """
        Display the syntax error that just occurred.
        This doesn't display a stacktrace because there isn't one.

        If a filename is given, it is stuffed in the exception instead
        of what was there before.

        The output is written by self.write(), below.
        """
        type, value, sys.last_traceback = sys.exc_info()
        self.write(sys.exc_info())
        sys.last_type = type
        sys.last_value = value
        if filename and type is SyntaxError:
            # Work hard to stuff the correct filename in the exception
            try:
                msg, (dummy_filename, lineno, offset, line) = value
            except:
                # Not the format we expect; leave it alone
                pass
            else:
                # Stuff in the right filename
                value = SyntaxError(msg, (filename, lineno, offset, line))
                sys.last_value = value
        errlist = traceback.format_exception_only(type, value)
        for item in errlist:
            self.write(item)

    def showtraceback(self):
        """
        Display the exception that just occurred.
        The output is written by self.write(), below.
        """
        try:
            type, value, tb = sys.exc_info()
            sys.last_type = type
            sys.last_value = value
            sys.last_traceback = tb
            tblist = traceback.extract_tb(tb)
            del tblist[:1]
            list = traceback.format_list(tblist)
            if list:
                list.insert(0, "Traceback (most recent call last):\n")
            list[len(list):] = traceback.format_exception_only(type, value)
        finally:
            tblist = tb = None
            self.write('Traceback (most recent call last):\n\tFile "<stdin>", line 1, in <module>\n')
        for item in list:
            self.write(item)

    def write(self, data):
        """
        Write a string to sys.stderr.
        """
        sys.stderr.write(data)

    def interact(self, banner=None):
        """
        Closely emulate an interactive console/shell.
        The optional banner argument specify the banner to print
        before the first interaction; by default it prints a banner
        similar to the one printed by the real MATLAB interpreter
        """
        if banner is None:
            self.write(welcome_txt + '\n')
        else:
            self.write("{}".format(str(banner)))
        more = 0
        while 1:
            try:
                if more:
                    prompt = sys.ps2
                else:
                    prompt = sys.ps1
                try:
                    line = input(prompt)
                except EOFError:
                    self.write("\n")
                    break
                else:
                    more = self.push(line)
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                more = 0


class MyInterpreter(MyInteractiveInterpreter):
    """MyInterpreter based on MyInteractiveInterpreter."""

    def __init__(self, locals=None, rawin=None, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, showInterpIntro=True):

        """Create an interactive interpreter object."""
        MyInteractiveInterpreter.__init__(self, locals=locals)
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        if rawin:
            import builtins
            builtins.raw_input = rawin
            del builtins
        if showInterpIntro:
            self.introText = welcome_txt
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = '>>> '
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = '... '
        self.more = 0
        # List of lists to support recursive push().
        self.commandBuffer = []
        self.startupScript = None

    def push(self, command, astMod=None):
        """
        Send command to the interpreter to be executed.
        Because this may be called recursively, we append a new list
        onto the commandBuffer list and then append commands into
        that.  If the passed in command is part of a multi-line
        command we keep appending the pieces to the last list in
        commandBuffer until we have a complete command. If not, we
        delete that last list.
        """

        # If an ast code module is passed, pass it to runModule instead
        more = False
        if astMod is not None:
            self.runModule(astMod)
            self.more = False
        else:
            more = self.more = self.runsource(command)
        return more

    def runsource(self, source):
        """
        Compile and run source code in the interpreter.
        """
        stdin, stdout, stderr = sys.stdin, sys.stdout, sys.stderr
        sys.stdin, sys.stdout, sys.stderr = self.stdin, self.stdout, self.stderr
        more = MyInteractiveInterpreter.runsource(self, source)

        # If sys.std* is still what we set it to, then restore it.
        # But, if the executed source changed sys.std*, assume it was
        # meant to be changed and leave it. Power to the people.
        if sys.stdin == self.stdin:
            sys.stdin = stdin
        else:
            self.stdin = sys.stdin
        if sys.stdout == self.stdout:
            sys.stdout = stdout
        else:
            self.stdout = sys.stdout
        if sys.stderr == self.stderr:
            sys.stderr = stderr
        else:
            self.stderr = sys.stderr
        return more

    def runModule(self, mod):
        """
        Compile and run an ast module in the interpreter.
        """
        stdin, stdout, stderr = sys.stdin, sys.stdout, sys.stderr
        sys.stdin, sys.stdout, sys.stderr = self.stdin, self.stdout, self.stderr
        self.runcode(compile(mod, '', 'single'))
        # If sys.std* is still what we set it to, then restore it.
        # But, if the executed source changed sys.std*, assume it was
        # meant to be changed and leave it. Power to the people.
        if sys.stdin == self.stdin:
            sys.stdin = stdin
        else:
            self.stdin = sys.stdin
        if sys.stdout == self.stdout:
            sys.stdout = stdout
        else:
            self.stdout = sys.stdout
        if sys.stderr == self.stderr:
            sys.stderr = stderr
        else:
            self.stderr = sys.stderr
        return False

    def getAutoCompleteKeys(self):
        """
        Return list of auto-completion keycodes.
        """
        return [ord('.')]

    def getAutoCompleteList(self, command='', *args, **kwds):
        pass

    def getCallTip(self, command='', *args, **kwds):
        pass


class MyFrame(wx.py.shell.ShellFrame):
    """
    Customized version of shell.ShellFrame
    """
    def __init__(self):
        wx.py.shell.ShellFrame.__init__(self, title='MATLAB Interpreter')

        self.shell = wx.py.shell.Shell(parent=self, id=-1, introText=None, locals=None, InterpClass=MyInterpreter, startupScript=self.startupScript, execStartupScript=self.execStartupScript)

        self.shell.SetSize((750, 525))


# source: StackOverflow (http://bit.ly/2BoDY1F)
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def main(shouldDisplayGUI=True):
    """
    Main function

    shouldDisplayGUI indicates whether to display the MATLAB interpreter in
    a user interface or the console. shouldDisplayGUI is set to True by default
    """
    if shouldDisplayGUI:
        app = wx.App()
        frame = MyFrame()
        frame.Show()
        app.SetTopWindow(frame)
        app.MainLoop()
    else:
        shell = MyInterpreter()
        shell.interact()


if __name__ == '__main__':
    answer = query_yes_no("Would you like to launch a GUI?\n('n' launches the interpreter in the console)")
    main(answer)
