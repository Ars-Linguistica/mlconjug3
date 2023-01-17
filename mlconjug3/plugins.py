import stevedore

def discover_plugins():
    """
    Discover and load all plugins in the 'mlconjug3.plugins' namespace.
    """
    manager = stevedore.ExtensionManager(
        namespace='mlconjug3.plugins',
        invoke_on_load=True,
        propagate_map_exceptions=True
    )
    return manager

def load_plugin(name):
    """
    Load and return a specific plugin by name.
    """
    manager = discover_plugins()
    return manager[name].obj

def register_plugin(name, plugin):
    """
    Register a new plugin.
    """
    manager = discover_plugins()
    manager.register(name, plugin)
