from pydantic_translations._translate import _format


def test_format():
    actual = _format(
        eng_pattern='oh hi {user}',
        trans_pattern='о, привет, {user}',
        eng_message='oh hi mark',
    )
    assert actual == 'о, привет, mark'