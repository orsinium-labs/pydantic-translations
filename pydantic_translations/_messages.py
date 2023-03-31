from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

from l10n import Locales

from ._constants import DEFAULT_LANGUAGE, LOCALES_PATH


locales = Locales(path=LOCALES_PATH)


def _get_without_codes() -> set[str]:
    loc = locales[DEFAULT_LANGUAGE]
    return {
        # type errors
        loc.get('byte type expected'),
        loc.get('str type expected'),
        loc.get('value could not be parsed to a boolean'),

        # value errors
        loc.get('could not parse value and unit from byte string'),
        loc.get('extra fields not permitted'),
        loc.get('invalid date format'),
        loc.get('invalid datetime format'),
        loc.get('invalid duration format'),
        loc.get('Invalid JSON'),
        loc.get('invalid time format'),
        loc.get('value is not a valid email address'),
        loc.get('value is not a valid IPv4 address'),
        loc.get('value is not a valid IPv4 interface'),
        loc.get('value is not a valid IPv4 network'),
        loc.get('value is not a valid IPv4 or IPv6 address'),
        loc.get('value is not a valid IPv4 or IPv6 interface'),
        loc.get('value is not a valid IPv4 or IPv6 network'),
        loc.get('value is not a valid IPv6 address'),
        loc.get('value is not a valid IPv6 interface'),
        loc.get('value is not a valid IPv6 network'),
    }


# In fact, these errors do have a code but it's not explicitly specified
# on the error class.
WITHOUT_CODES: frozenset[str] = frozenset(_get_without_codes())


def _get_with_codes() -> dict[str, str | tuple[str, ...]]:
    loc = locales[DEFAULT_LANGUAGE]
    return {
        'type_error.arbitrary_type':            loc.get('instance of {expected_arbitrary_type} expected'),
        'type_error.bool':                      loc.get('value is not a valid boolean'),
        'type_error.callable':                  loc.get('{value} is not callable'),
        'type_error.class':                     loc.get('a class is expected'),
        'type_error.dataclass':                 loc.get('instance of {class_name}, tuple or dict expected'),
        'type_error.decimal':                   loc.get('value is not a valid decimal'),
        'type_error.deque':                     loc.get('value is not a valid deque'),
        'type_error.dict':                      loc.get('value is not a valid dict'),
        'type_error.enum_instance':             loc.get('{value} is not a valid Enum instance'),
        'type_error.enum':                      loc.get('value is not a valid enumeration member; permitted: {permitted}'),
        'type_error.float':                     loc.get('value is not a valid float'),
        'type_error.frozenset':                 loc.get('value is not a valid frozenset'),
        'type_error.hashable':                  loc.get('value is not a valid hashable'),
        'type_error.int_enum_instance':         loc.get('{value} is not a valid IntEnum instance'),
        'type_error.integer':                   loc.get('value is not a valid integer'),
        'type_error.iterable':                  loc.get('value is not a valid iterable'),
        'type_error.json':                      loc.get('JSON object must be str, bytes or bytearray'),
        'type_error.list':                      loc.get('value is not a valid list'),
        'type_error.none.allowed':              loc.get('value is not none'),
        'type_error.none.not_allowed':          loc.get('none is not an allowed value'),
        'type_error.not_none':                  loc.get('value is not None'),
        'type_error.path':                      loc.get('value is not a valid path'),
        'type_error.pyobject':                  loc.get('ensure this value contains valid import path or valid callable: {error_message}'),
        'type_error.sequence':                  loc.get('value is not a valid sequence'),
        'type_error.set':                       loc.get('value is not a valid set'),
        'type_error.subclass':                  loc.get('subclass of {expected_class} expected'),
        'type_error.tuple':                     loc.get('value is not a valid tuple'),
        'type_error.uuid':                      loc.get('value is not a valid uuid'),
        'value_error.any_str.max_length':       loc.get('ensure this value has at most {limit_value} characters'),
        'value_error.any_str.min_length':       loc.get('ensure this value has at least {limit_value} characters'),
        'value_error.color':                    loc.get('value is not a valid color: {reason}'),
        'value_error.const':                    loc.get('unexpected value; permitted: {permitted}'),
        'value_error.date.not_in_the_future':   loc.get('date is not in the future'),
        'value_error.date.not_in_the_past':     loc.get('date is not in the past'),
        'value_error.decimal.max_digits':       loc.get('ensure that there are no more than {max_digits} digits in total'),
        'value_error.decimal.max_places':       loc.get('ensure that there are no more than {decimal_places} decimal places'),
        'value_error.decimal.not_finite':       loc.get('value is not a valid decimal'),
        'value_error.decimal.whole_digits':     loc.get('ensure that there are no more than {whole_digits} digits before the decimal point'),
        'value_error.discriminated_union.invalid_discriminator': loc.get('No match for discriminator {discriminator_key!r} and value {discriminator_value!r} (allowed values: {allowed_values})'),
        'value_error.discriminated_union.missing_discriminator': loc.get('Discriminator {discriminator_key!r} is missing in value'),
        'value_error.frozenset.max_items':      loc.get('ensure this value has at most {limit_value} items'),
        'value_error.frozenset.min_items':      loc.get('ensure this value has at least {limit_value} items'),
        'value_error.invalidbytesizeunit':      loc.get('could not interpret byte unit: {unit}'),
        'value_error.list.max_items':           loc.get('ensure this value has at most {limit_value} items'),
        'value_error.list.min_items':           loc.get('ensure this value has at least {limit_value} items'),
        'value_error.list.unique_items':        loc.get('the list has duplicated items'),
        'value_error.missing':                  loc.get('field required'),
        'value_error.number.not_finite_number': loc.get('ensure this value is a finite number'),
        'value_error.number.not_ge':            loc.get('ensure this value is greater than or equal to {limit_value}'),
        'value_error.number.not_gt':            loc.get('ensure this value is greater than {limit_value}'),
        'value_error.number.not_le':            loc.get('ensure this value is less than or equal to {limit_value}'),
        'value_error.number.not_lt':            loc.get('ensure this value is less than {limit_value}'),
        'value_error.number.not_multiple':      loc.get('ensure this value is a multiple of {multiple_of}'),
        'value_error.path.not_a_directory':     loc.get('path "{path}" does not point to a directory'),
        'value_error.path.not_a_file':          loc.get('path "{path}" does not point to a file'),
        'value_error.path.not_exists':          loc.get('file or directory at path "{path}" does not exist'),
        'value_error.payment_card_number.digits': loc.get('card number is not all digits'),
        'value_error.payment_card_number.invalid_length_for_brand': loc.get('Length for a {brand} card must be {required_length}'),
        'value_error.payment_card_number.luhn_check': loc.get('card number is not luhn valid'),
        'value_error.regex_pattern':            loc.get('Invalid regular expression'),
        'value_error.set.max_items':            loc.get('ensure this value has at most {limit_value} items'),
        'value_error.set.min_items':            loc.get('ensure this value has at least {limit_value} items'),
        'value_error.str.regex':                loc.get('string does not match regex "{pattern}"'),
        'value_error.tuple.length':             loc.get('wrong tuple length {actual_length}, expected {expected_length}'),
        'value_error.url.extra':                loc.get('URL invalid, extra characters found after valid URL: {extra!r}'),
        'value_error.url.host':                 (loc.get('URL host invalid'), loc.get('URL host invalid, top level domain required')),
        'value_error.url.port':                 loc.get('URL port invalid, port cannot exceed 65535'),
        'value_error.url.scheme':               (loc.get('invalid or missing URL scheme'), loc.get('URL scheme not permitted')),
        'value_error.url.userinfo':             loc.get('userinfo required in URL but missing'),
        'value_error.uuid.version':             loc.get('uuid version {required_version} expected'),
    }


WITH_CODES: Mapping[str, str | tuple[str, ...]] = MappingProxyType(_get_with_codes())
