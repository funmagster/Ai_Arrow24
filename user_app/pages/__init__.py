import os
import pkgutil
import importlib
import sys

package_dir = os.path.dirname(__file__)
__all__ = []

# Получаем пространство имен пакета 'pages'
package = sys.modules[__name__]

# Импортируем все модули из пакета
for _, module_name, _ in pkgutil.iter_modules(path=[package_dir]):
    full_module_name = f"pages.{module_name}"
    module = importlib.import_module(full_module_name)

    # Добавляем классы модуля в пространство имен пакета
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, type):  # Проверяем, что это класс
            setattr(package, attr_name, attr)
            __all__.append(attr_name)
