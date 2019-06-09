"""
The binlink module allows callables to register themselves in the binlink
registry. If a symlink is created to the main executable, the registered
callable is called when the symlink is executed. For example, given a function:

    @binlink.register("sec-gather-unixusers")
    def unixusers(version):
        print("Gathering unix user information")

And given a symlink created like so:

    $ ln -s ln -s ./sec-tool ./sec-gather-unixusers

You can now call `sec-gather-unixusers` from the commandline:

    $ ./sec-gather-unixusers
    Gathering unix user information

This construction is used so that we can generate a single self-contained
binary using pyinstaller. Otherwise, if each tool was a separate binary, they
would each contain the entire Python VM.
"""

binlinks = {}


class BinLinkError(Exception):
    """
    Base class for exceptions in this module.
    """
    pass


def register(binname):
    """
    Register a callable under a binary name
    """
    def wrapper(func):
        binlinks[binname] = func
    return wrapper


def run(binname, *args, **kwargs):
    """
    Execute the registered callable for binname, passing args and kwargs to the
    callable. Raises a BinLinkError if the binname wasn't registered.
    """
    try:
        bin = binlinks[binname]
    except KeyError:
        raise BinLinkError("No binlink registered for '{}'.".format(binname))

    bin(*args, **kwargs)
