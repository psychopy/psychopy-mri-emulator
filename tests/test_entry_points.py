import importlib.metadata
from psychopy.plugins import activatePlugins
from psychopy.tools.pkgtools import PluginStub


def test_entry_points():
    """
    Check that entry points from this module are importable once activated, and that the imported 
    object isn't a PluginStub
    """
    # activate all plugins
    activatePlugins()
    # iterate through entry points
    for ep in importlib.metadata.distribution("psychopy-mri-emulator").entry_points:
        # get module
        mod = importlib.import_module(ep.group)
        # get target from module
        cls = getattr(mod, ep.name)
        # make sure target isn't a PluginStub
        if isinstance(cls, type):
            assert not issubclass(cls, PluginStub)
