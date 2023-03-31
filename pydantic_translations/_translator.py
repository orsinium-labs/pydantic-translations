from __future__ import annotations

import re
from dataclasses import dataclass
from functools import cached_property, lru_cache
from types import TracebackType
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
    """Set of functions to translate pydantic errors to the given locale.

    Supported locales:

    * `de`: German.
    * `en`: English (US).
    * `es`: Spanish.
    * `fr`: French.
    * `it`: Italian.
    * `nl`: Dutch.
    * `ru`: Russian.

    Example of using Translator as a context manager:

    ::

        translator = Translator('nl')
        with translator:
            User.parse_obj({'name': 'Aragorn'})

    """
    locale: str | Locale

    def __enter__(self) -> Translator:
        return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None,
    ) -> None:
        """Translate pydantic errors raised from the context.

        ::

            translator = Translator('nl')
            with translator:
                User.parse_obj({'name': 'Aragorn'})

        """
        if exc_value is None:
            return
        if not isinstance(exc_value, ValidationError):
            return
        exc_value = self.translate_exception(exc_value)
        raise exc_value from None

    def translate_exception(self, exc: ValidationError) -> ValidationError:
        """Translate errors in a pydantic exception.

        ::

            translator = Translator('nl')
            try:
                User.parse_obj({'name': 'Aragorn'})
            except pydantic.ValidationError as exc:
                exc = translator.translate_exception(exc)
                raise exc

        """
        errors = [self.translate_error(err) for err in exc.errors()]
        result = ValidationError(
            errors=exc.raw_errors,
            model=exc.model,
        )
        result._error_cache = errors
        return result

    def translate_error(self, err: ErrorDict) -> ErrorDict:
        """Translate the error dict.

        If for some reason it cannot be translated
        (unknown error code, unexpected error message, or unsupported locale),
        the error dict is returned unchanged.

        ::

            translator = Translator('nl')
            try:
                User.parse_obj({'name': 'Aragorn'})
            except pydantic.ValidationError as exc:
                err = exc.errors()[0]
                err = translator.translate_error(err)
                print(err)

        """
        result = self.maybe_translate_error(err)
        if result is None:
            return err
        return result

    def maybe_translate_error(self, err: ErrorDict) -> ErrorDict | None:
        """Translate the error dict if possible.
        """
        locale = self._locale
        if locale is None:
            return None
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

    @cached_property
    def _locale(self) -> Locale | None:
        if isinstance(self.locale, str):
            lang = self.locale.split('-')[0].split('_')[0]
            return locales.get(lang)
        return self.locale


def _format(eng_pattern: str, trans_pattern: str, eng_message: str) -> str | None:
    """
    Parse `eng_message` using `eng_pattern`
    and substitute extracted values into `trans_pattern`.
    """
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
