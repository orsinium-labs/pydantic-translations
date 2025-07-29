from __future__ import annotations

import pydantic
import pytest
from typing import List

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


def test_translator__context_manager() -> None:
    class User(pydantic.BaseModel):
        name: str
        age: int = 21

    tr = Translator('ru')
    with pytest.raises(pydantic.ValidationError) as exc:
        with tr:
            User.parse_obj({'name': '', 'age': 'hi'})
    assert exc.value.errors()[0]['msg'] == 'значение должно быть целым числом'


class MinOneMaxTen(pydantic.BaseModel):
    items: List[str] = pydantic.Field(..., min_items=1, max_items=10)

class MinTwo(pydantic.BaseModel):
    items: List[str] = pydantic.Field(..., min_items=2)

class MinFive(pydantic.BaseModel):
    items: List[str] = pydantic.Field(..., min_items=5)

class MinTwentyOne(pydantic.BaseModel):
    items: List[str] = pydantic.Field(..., min_items=21)

@pytest.mark.parametrize(
    "model_class, test_data, expected_substring",
    [
        (MinOneMaxTen, {"items": []}, "как минимум 1 элемент"),
        (MinOneMaxTen, {"items": ["a"]*11}, "максимум 10 элементов"),
        (MinTwo, {"items": ["a"]}, "как минимум 2 элемента"),
        (MinFive, {"items": ["a", "b", "c"]}, "как минимум 5 элементов"),
        (MinTwentyOne, {"items": ["a", "b", "c"]}, "как минимум 21 элемент"),
    ]
)
def test_russian_list_pluralization(
    model_class, test_data, expected_substring
):
    tr = Translator('ru')
    with pytest.raises(pydantic.ValidationError) as exc:
        with tr:
            model_class.parse_obj(test_data)

    error_msg = exc.value.errors()[0]['msg']
    assert expected_substring in error_msg
