import os
import pkgutil
import importlib
import sys

package_dir = os.path.dirname(__file__)
__all__ = []

# Get the 'pages' package namespace
package = sys.modules[__name__]

# Import all modules from the package
for _, module_name, _ in pkgutil.iter_modules(path=[package_dir]):
    full_module_name = f"pages.{module_name}"
    module = importlib.import_module(full_module_name)

    # Add the module classes to the package namespace
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, type):  # Check that it's a class
            setattr(package, attr_name, attr)
            __all__.append(attr_name)
