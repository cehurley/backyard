from .user import User
from .garbage import Garbage
from .truck import Truck
'''

from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

cnames = []
# iterate through the modules in the current package
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([package_dir]):

    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute):
            # Add the class to this package's variables
            globals()[attribute_name] = attribute
            cnames.append(attribute)


for c in cnames:  # [Workflow, User]:
    if hasattr(c, 'belongs_to'):
        for b in c.belongs_to:
            c.belongs_to[b]['class'] = eval(c.belongs_to[b]['class'])
    if hasattr(c, 'hbtm'):
        for h in c.hbtm:
            c.hbtm[h]['class'] = eval(c.hbtm[h]['class'])
    if hasattr(c, 'has_many'):
        for h in c.has_many:
            c.has_many[h]['class'] = eval(c.has_many[h]['class'])
'''
