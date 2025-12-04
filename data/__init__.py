"""data package for command modules"""

def register_all(tree):
    """Helper to register all commands from this package onto the given CommandTree."""
    # Individual modules expose a `register(tree)` function
    from . import ping, hi, clear, shutdown
    ping.register(tree)
    hi.register(tree)
    clear.register(tree)
    shutdown.register(tree)
