from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING

from l10n import Locale, Locales
from pydantic import ValidationError

from ._constants import DEFAULT_LANGUAGE, LOCALES_PATH
from ._messages import WITH_CODES


if TYPE_CHECKING:
    from pydantic.error_wrappers import ErrorDict

locales = Locales(path=LOCALES_PATH)
REX_TRANSFORM = re.compile(r'\{([a-z_]+?)(\!r)?\}')


@dataclass(frozen=True)
class Translator:
    locale: str | Locale

    def __enter__(self) -> None:
        return None

    def __exit__(self, *exc_info) -> None:
        ...

    def translate_exception(self, exc: ValidationError) -> ValidationError:
        errors = [self.translate_error(err) for err in exc.errors()]
        result = ValidationError(
            errors=exc.raw_errors,
            model=exc.model,
        )
        result._error_cache = errors
        return result

    def translate_error(self, err: ErrorDict) -> ErrorDict:
        result = self.maybe_translate_error(err)
        if result is None:
            return err
        return result

    def maybe_translate_error(self, err: ErrorDict) -> ErrorDict | None:
        if isinstance(self.locale, str):
            locale = locales[self.locale]
        else:
            locale = self.locale
        if locale.language == DEFAULT_LANGUAGE:
            return err

        eng_message = err['msg']
        eng_patterns = WITH_CODES.get(err['type'], eng_message)
        if isinstance(eng_patterns, tuple):
            if eng_message not in eng_patterns:
                return None
            eng_pattern = eng_message
        else:
            eng_pattern = eng_patterns

        new_msg = _format(
            eng_pattern=eng_pattern,
            trans_pattern=locale.get(eng_pattern),
            eng_message=eng_message,
        )
        if new_msg is None:
            return None
        result = err.copy()
        result['msg'] = new_msg
        return result


def _format(eng_pattern: str, trans_pattern: str, eng_message: str) -> str | None:
    if '{' not in eng_pattern:
        return trans_pattern
    rex = _compile_pattern(eng_pattern)
    match = rex.match(eng_message)
    if match is None:
        return None
    return trans_pattern.format(**match.groupdict())


@lru_cache(maxsize=128)
def _compile_pattern(pattern: str) -> re.Pattern:
    """Convert python str.format-style string into a regular expression.
    """
    assert REX_TRANSFORM.findall(pattern)
    regex = REX_TRANSFORM.sub(r'(?P<\1>.+)', pattern)
    return re.compile(regex)
