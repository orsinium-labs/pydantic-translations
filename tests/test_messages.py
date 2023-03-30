from __future__ import annotations
from typing import Iterator

import pytest
from pydantic_translations._messages import WITH_CODES, WITHOUT_CODES
import pydantic
from itertools import chain


def iter_all_subclasses(root: type) -> Iterator[type]:
    for cls in root.__subclasses__():
        yield cls
        yield from iter_all_subclasses(cls)


def iter_all_messages() -> Iterator[str]:
    yield from WITHOUT_CODES
    for msg in WITH_CODES.values():
        if isinstance(msg, tuple):
            yield from msg
        else:
            yield msg


@pytest.mark.parametrize('cls', chain(
    iter_all_subclasses(pydantic.PydanticTypeError),
    iter_all_subclasses(pydantic.PydanticValueError),
))
def test_error_message_is_present(cls: type) -> None:
    msg_template = getattr(cls, 'msg_template', None)
    if msg_template is None:
        pytest.skip()
    assert msg_template in iter_all_messages()


@pytest.mark.parametrize('cls', iter_all_subclasses(pydantic.PydanticTypeError))
def test_type_error_code_is_present(cls: type) -> None:
    code = getattr(cls, 'code', None)
    msg_template = getattr(cls, 'msg_template', None)
    assert code is not None or msg_template is not None
    if code is not None:
        code = f'type_error.{code}'
        actual = WITH_CODES[code]
        if code == 'type_error.enum':
            assert msg_template is None
        else:
            assert actual == msg_template


@pytest.mark.parametrize('cls', iter_all_subclasses(pydantic.PydanticValueError))
def test_value_error_code_is_present(cls: type) -> None:
    code = getattr(cls, 'code', None)
    msg_template = getattr(cls, 'msg_template', None)
    if code is None and msg_template is None:
        pytest.skip()
    if code is not None:
        if code == 'url':
            pytest.skip()
        code = f'value_error.{code}'
        actual = WITH_CODES[code]
        if code == 'value_error.const':
            assert msg_template is None
        else:
            if isinstance(actual, tuple):
                assert msg_template in actual
            else:
                assert actual == msg_template
