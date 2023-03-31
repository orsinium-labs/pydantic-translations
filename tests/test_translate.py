from __future__ import annotations

import pydantic
import pytest

from pydantic_translations import Translator
from pydantic_translations._translator import _format


def test_format() -> None:
    actual = _format(
        eng_pattern='oh hi {user}',
        trans_pattern='о, привет, {user}',
        eng_message='oh hi mark',
    )
    assert actual == 'о, привет, mark'


@pytest.mark.parametrize('lang, given, expected', [
    ('ru', {'name': 'Aragorn', 'age': 88}, None),
    ('ru', {'name': '', 'age': 'hi'}, 'значение должно быть целым числом'),
    ('en', {'name': '', 'age': 'hi'}, 'value is not a valid integer'),
])
def test_translator(lang: str, given: object, expected: str | None) -> None:
    class User(pydantic.BaseModel):
        name: str
        age: int = 21

    tr = Translator(lang)
    try:
        User.parse_obj(given)
    except pydantic.ValidationError as exc:
        actual = tr.translate_exception(exc)
        assert actual.errors()[0]['msg'] == expected
    else:
        assert expected is None
