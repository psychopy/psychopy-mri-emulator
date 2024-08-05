"""
Use data from the imported library to automatically generate pages. This approach is very much limited, so we recommend using it as a starting point and then writing manually from there. Use with caution if you already have docs written as this may overwrite them!
"""


from importlib import metadata, import_module
from pathlib import Path
from psychopy.experiment import Experiment


# specify path to docs source folder
docsFolder = Path(__file__).parent
# specify path to root folder (containing the pyproject.toml)
rootFolder = docsFolder.parent
# create a dummy experiment so we can initialize comps/routines to inspect their params
exp = Experiment()
# get path for the module folder (will be the first folder found which contains an __init__.py)
modFolder = None
for candidate in rootFolder.glob("*/__init__.py"):
    if candidate.parent.stem not in ("tests", "docs", "docs_src"):
        modFolder = candidate.parent
if modFolder is None:
    raise ModuleNotFoundError("Could not find module.")
# find all entry point groups
for group, points in metadata.entry_points().items():
    # make sure it's pointing to psychopy
    if not group.startswith("psychopy"):
        continue
    # find all entry points for this group
    for ep in points:
        # make sure it's come from a module from this plugin
        if not ep.value.split(".")[0] == modFolder.stem:
            continue
        # load object
        try:
            obj = ep.load()
        except:
            print("Failed to write docs for " + ep.value)
            continue
        # get name and mro
        mro, name = ep.value.split(":")
        # write docs
        if group.startswith("psychopy.experiment.components"):
            content = obj(exp, "").getFullDocumentation()
            file = docsFolder / "builder" / "components" / (name + ".rst")
            file.write_text(content)
        else:
            # anything else, write for Coder
            content = (
                f"===============================\n"
                f"{name}\n"
                f"===============================\n"
                f"\n"
                f"To import {name}, you can either use::\n"
                f"\n"
                f"    from {mro} import {name}\n"
                f"\n"
                f"or, any time after `psychopy.plugins.activatePlugins` has been called::\n"
                f"\n"
                f"    from {group} import {name}\n"
                f"\n"
                f".. autoclass:: {mro}.{name}\n"
                f"    :members:\n"
                f"    :undoc-members:\n"
                f"    :inherited-members:\n"
            )
            file = docsFolder / "coder" / (name + ".rst")
            file.write_text(content)
