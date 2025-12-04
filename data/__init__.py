"""data package for command modules"""

def register_all(tree, client=None):
    """Helper to register all commands from this package onto the given CommandTree.

    If `client` is provided, modules that need the client (event listeners)
    will be initialized via their `setup(client)` coroutine.
    """
    # Individual modules expose a `register(tree)` function
    from . import ping, hi, clear, shutdown
    ping.register(tree)
    hi.register(tree)
    clear.register(tree)
    shutdown.register(tree)

    # Optional event listeners
    if client is not None:
        try:
            from . import ai_responder
            # schedule setup to run soon
            import asyncio
            asyncio.create_task(ai_responder.setup(client))
        except Exception:
            # don't fail if ai_responder can't be loaded
            pass
