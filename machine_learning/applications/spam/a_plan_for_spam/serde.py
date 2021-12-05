"""
Minimal library to support deserializing events from JSON.

Don't use this for serious applications. Use https://github.com/konradhalas/dacite, instead.

As this code contains substantial portions of the https://github.com/konradhalas/dacite codebase,
the MIT license is copied in:

MIT License

Copyright (c) 2018 Konrad Hałas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import copy
import dataclasses
import itertools

# Init-only fields have this type. Init-only fields are accessible in __init__
# and (notably) __post_init__, but are not otherwise accessible, for ex. in .fields().
# https://docs.python.org/3/library/dataclasses.html#init-only-variables
from dataclasses import InitVar  # type: ignore

# Main object type of dataclasses, describing their fields.
from dataclasses import Field

# A sentinel value signifying a missing default or default_factory.
from dataclasses import MISSING

# Undocumented accessor of field objects
# https://github.com/python/cpython/blob/3.9/Lib/dataclasses.py#L188
from dataclasses import _FIELDS  # type: ignore

# Marker for Field
from dataclasses import _FIELD  # type: ignore

# Marker for InitVar type Field
from dataclasses import _FIELD_INITVAR  # type: ignore
from typing import (
    Any,
    Collection,
    Dict,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

Input = Dict[str, Any]
T = TypeVar("T")


class SerdeError(Exception):
    pass


class DefaultValueNotFoundError(SerdeError):
    pass


class SerdeFieldError(SerdeError):
    def __init__(self, field_path: Optional[str] = None):
        super().__init__()
        self.field_path = field_path

    def update_path(self, parent_field_path: str) -> None:
        if self.field_path:
            self.field_path = f"{parent_field_path}.{self.field_path}"
        else:
            self.field_path = parent_field_path


class MissingValueError(SerdeFieldError):
    def __init__(self, field_path: Optional[str] = None):
        super().__init__(field_path=field_path)

    def __str__(self) -> str:
        return f'missing value for field "{self.field_path}"'


def from_dict(dataklass: Type[T], data: Input) -> T:
    """
    Conveniently convert from a (likely JSON-deserialized) dict into a specified dataclass
    object.

    For simplicity, this does not do proper type-checking on the values assigned to fields.
    """
    init_values: Input = {}
    post_init_values: Input = {}
    dataklass_fields = _get_fields(dataklass)
    for field in dataklass_fields:
        field_copy = copy.copy(field)
        if field_copy.name in data:
            try:
                field_data = data[field_copy.name]
                transformed_value = transform_value(
                    target_type=field.type,
                    value=field_data,
                )
                value = _build_value(type_=field.type, data=transformed_value)
            except Exception:
                raise
        else:
            try:
                value = get_default_value_for_field(field_copy)
            except DefaultValueNotFoundError:
                if not field_copy.init:
                    continue
                raise MissingValueError(field_copy.name)
        if field_copy.init:
            init_values[field_copy.name] = value
        else:
            post_init_values[field_copy.name] = value
    return _create_instance(
        dataklass=dataklass,
        init_values=init_values,
        post_init_values=post_init_values,
    )


def get_default_value_for_field(field: Field) -> Any:
    if field.default != MISSING:
        return field.default
    elif field.default_factory != MISSING:  # type: ignore
        return field.default_factory()  # type: ignore
    elif _is_optional(field.type):
        return None
    raise DefaultValueNotFoundError()


def _build_value(type_: Type, data: Any) -> Any:
    if _is_init_var(type_):
        try:
            type_ = type_.type
        except AttributeError:
            type_ = Any  # type: ignore
    if _is_union(type_):
        return _build_value_for_union(union=type_, data=data)
    elif _is_generic_collection(type_) and is_instance(
        data, _extract_origin_collection(type_)
    ):
        return _build_value_for_collection(collection=type_, data=data)
    elif dataclasses.is_dataclass(type_) and is_instance(data, Input):
        return from_dict(dataklass=type_, data=data)
    return data


def _build_value_for_union(union: Type, data: Any) -> Any:
    types = _extract_generic(union)
    if _is_optional(union) and len(types) == 2:
        return _build_value(type_=types[0], data=data)
    union_matches: Dict[Any, Any] = {}
    for inner_type in types:
        try:
            try:
                data = transform_value(
                    target_type=inner_type,
                    value=data,
                )
            except Exception:
                continue
            value = _build_value(type_=inner_type, data=data)
            if is_instance(value, inner_type):
                union_matches[inner_type] = value
        except SerdeError:
            pass
    if len(union_matches) > 1:
        raise SerdeError(
            f"Strict union match error. Cannot choose b/w possible matches: {union_matches}"
        )
    return union_matches.popitem()[1]


def transform_value(
    target_type: Type,
    value: Any,
) -> Any:
    if _is_optional(target_type):
        if value is None:
            return None
        target_type = _extract_optional(target_type)
        return transform_value(target_type, value)
    if _is_generic_collection(target_type) and isinstance(
        value, _extract_origin_collection(target_type)
    ):
        collection_cls = value.__class__
        if issubclass(collection_cls, dict):
            key_cls, item_cls = _extract_generic(target_type, defaults=(Any, Any))
            return collection_cls(
                {
                    transform_value(key_cls, key): transform_value(item_cls, item)
                    for key, item in value.items()
                }
            )
        item_cls = _extract_generic(target_type, defaults=(Any,))[0]
        return collection_cls(transform_value(item_cls, item) for item in value)
    return value


def _create_instance(
    *, dataklass: Type[T], init_values: Input, post_init_values: Input
) -> T:
    instance = dataklass(**init_values)  # type: ignore
    for key, value in post_init_values.items():
        setattr(instance, key, value)
    return instance


def _get_fields(dataklass: Type[T]) -> List[Field]:
    fields: Dict[str, dataclasses.Field] = getattr(dataklass, _FIELDS)
    return [
        f
        for f in fields.values()
        if f._field_type is _FIELD or f._field_type is _FIELD_INITVAR  # type: ignore
    ]


def _extract_origin_collection(collection: Type) -> Type:
    """
    Takes a type like List[Foo], where `Foo` may be something like:

        class Foo(NamedTuple):
            a: int

    and extracts the 'origin' collection type, which will be one of the
    stdlib collection types: list, dict, tuple, etc.
    """
    try:
        return collection.__extra__
    except AttributeError:
        return collection.__origin__


def _is_optional(type_: Type) -> bool:
    return _is_union(type_) and type(None) in _extract_generic(type_)


def _extract_optional(optional: Type[Optional[T]]) -> T:
    for type_ in _extract_generic(optional):
        if type_ is not type(None):
            return type_
    raise ValueError("can not find not-none value")


def _is_literal(type_: Type) -> bool:
    try:
        from typing import Literal  # type: ignore

        return _is_generic(type_) and type_.__origin__ == Literal
    except ImportError:
        # typing.Literal is new in 3.8
        # https://docs.python.org/3/library/typing.html#typing.Literal
        return False


def _is_generic(type_: Type) -> bool:
    """
    Check if type is of typing.Generic.

    Ref: https://stackoverflow.com/a/50080269/4885590
    """
    return hasattr(type_, "__origin__")


def _is_generic_collection(type_: Type) -> bool:
    if not _is_generic(type_):
        return False
    origin = _extract_origin_collection(type_)
    try:
        return bool(origin and issubclass(origin, Collection))
    except (TypeError, AttributeError):
        return False


def _is_union(type_: Type) -> bool:
    return _is_generic(type_) and type_.__origin__ == Union


def _extract_generic(type_: Type, defaults: Tuple = ()) -> tuple:
    try:
        if hasattr(type_, "_special") and type_._special:
            return defaults
        return type_.__args__ or defaults  # type: ignore
    except AttributeError:
        return defaults


def _is_init_var(type_: Type) -> bool:
    return isinstance(type_, InitVar) or type_ is InitVar


def _extract_init_var(type_: Type) -> Union[Type, Any]:
    try:
        return type_.type
    except AttributeError:
        return Any


def _is_new_type(type_: Type) -> bool:
    return hasattr(type_, "__supertype__")


def _extract_new_type(type_: Type) -> Type:
    return type_.__supertype__


def is_instance(value: Any, type_: Type) -> bool:
    if type_ == Any:
        return True
    elif _is_union(type_):
        return any(is_instance(value, t) for t in _extract_generic(type_))
    elif _is_generic_collection(type_):
        origin = _extract_origin_collection(type_)
        if not isinstance(value, origin):
            return False
        if not _extract_generic(type_):
            return True
        if isinstance(value, tuple):
            tuple_types = _extract_generic(type_)
            if len(tuple_types) == 1 and tuple_types[0] == ():
                return len(value) == 0
            elif len(tuple_types) == 2 and tuple_types[1] is ...:
                return all(is_instance(item, tuple_types[0]) for item in value)
            else:
                if len(tuple_types) != len(value):
                    return False
                return all(
                    is_instance(item, item_type)
                    for item, item_type in zip(value, tuple_types)
                )
        if isinstance(value, Mapping):
            key_type, val_type = _extract_generic(type_, defaults=(Any, Any))
            for key, val in value.items():
                if not is_instance(key, key_type) or not is_instance(val, val_type):
                    return False
            return True
        return all(
            is_instance(item, _extract_generic(type_, defaults=(Any,))[0])
            for item in value
        )
    elif _is_new_type(type_):
        return is_instance(value, _extract_new_type(type_))
    elif _is_literal(type_):
        return value in _extract_generic(type_)
    elif _is_init_var(type_):
        return is_instance(value, _extract_init_var(type_))
    elif _is_type_generic(type_):
        return _is_subclass(value, _extract_generic(type_)[0])
    else:
        try:
            # As described in PEP 484 - section: "The numeric tower"
            if isinstance(value, (int, float)) and type_ in [float, complex]:
                return True
            return isinstance(value, type_)
        except TypeError:
            return False


def _is_subclass(sub_type: Type, base_type: Type) -> bool:
    if _is_generic_collection(sub_type):
        sub_type = _extract_origin_collection(sub_type)
    try:
        return issubclass(sub_type, base_type)
    except TypeError:
        return False


# https://docs.python.org/3/library/typing.html#typing.Type
def _is_type_generic(type_: Type) -> bool:
    try:
        return type_.__origin__ in (type, Type)
    except AttributeError:
        return False


def _build_value_for_collection(collection: Type, data: Any) -> Any:
    data_type = data.__class__
    if is_instance(data, Mapping):
        item_type = _extract_generic(collection, defaults=(Any, Any))[1]
        return data_type(
            (key, _build_value(type_=item_type, data=value))
            for key, value in data.items()
        )
    elif is_instance(data, tuple):
        types = _extract_generic(collection)
        # See https://stackoverflow.com/a/50661182/4885590 for info on 'Ellipsis'
        if len(types) == 2 and types[1] == Ellipsis:
            return data_type(_build_value(type_=types[0], data=item) for item in data)
        return data_type(
            _build_value(type_=type_, data=item)
            for item, type_ in itertools.zip_longest(data, types)
        )
    item_type = _extract_generic(collection, defaults=(Any,))[0]
    return data_type(_build_value(type_=item_type, data=item) for item in data)
