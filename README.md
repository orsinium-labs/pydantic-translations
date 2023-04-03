# pydantic-translations

Translations for pydantic errors.

## Languages

Currently, we have translated pydantic v1.10.2 errors to the following languages:

* `de`: German. 0/87.
* `es`: Spanish. 0/87.
* `fr`: French. 0/87.
* `it`: Italian. 0/87.
* `nl`: Dutch. 0/87.
* `ru`: Russian. 70/87.

Need more languages? Contributions are welcome!

## Installation

```bash
python3 -m pip install pydantic-translations
```

## Usage

Let's say you have a pydantic model `User`:

```python
from pydantic import BaseModel

class User(BaseModel):
    age: int
```

The translations are managed by the `Translator` class that is instantiated with the locale (language) you want the messages to be translated to:

```python
from pydantic_translations import Translator

tr = Translator('ru')
```

You can use translator as a context manager to translate pydantic exceptions raised from the context:

```python
with tr:
    User.parse_obj({'age': 'idk'})
# ValidationError: 1 validation error for User
# age
#   значение должно быть целым числом (type=type_error.integer)
```

Or use the `translate_exception` method to directly translate an exception instance:

```python
from pydantic import ValidationError

try:
    User.parse_obj({'age': 'idk'})
except ValidationError as exc:
    exc = tr.translate_exception(exc)
    raise exc
```

Or use the `translate_error` method to translate a specific error:

```python
try:
    User.parse_obj({'age': 'idk'})
except ValidationError as exc:
    err = exc.errors()[0]
    err = tr.translate_error(err)
    print(err)
# {'loc': ('age',), 'msg': 'значение должно быть целым числом', 'type': 'type_error.integer'}
```

## Custom translations

If you have translated the errors to a new language, the best you can do is contribute it back here. If, for some (legal?) reason, you can't, you may pass into the Translated as a locale a [l10n](https://github.com/orsinium-labs/l10n) locale with your translations:

```python
from l10n import Locales

locales = Locales()
locale = locales['ua']
tr = Translator(locale)
```

## Contributors

1. The original error messages provided by [@samuelcolvin](https://github.com/samuelcolvin) and [pydantic contributors](https://github.com/pydantic/pydantic/graphs/contributors).
1. The Russian translation is provided by [@orsinium](https://github.com/orsinium).
1. The German, Spanish, French, Italian, and Dutch translations are provided by [Andovar](https://andovar.com/) translation agency.

Minor corrections and improvements are provided by [the project contributors](https://github.com/orsinium-labs/pydantic-translations/graphs/contributors).
