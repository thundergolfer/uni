import dataclasses

import serde


def test_from_dict():
    @dataclasses.dataclass
    class FooBar:
        a: str
        b: int
        c: bool

    dict_input = {
        "a": "John",
        "b": 30,
        "c": True,
    }

    actual = serde.from_dict(dataklass=FooBar, data=dict_input)
    assert actual
    assert actual.a == "John"
    assert actual.b == 30
    assert actual.c is True


def test_from_dict_w_nested_dataclasses():
    @dataclasses.dataclass
    class Bar:
        c: bool

    @dataclasses.dataclass
    class Foo:
        a: str
        b: Bar

    dict_input = {
        "a": "Jerry",
        "b": {
            "c": False,
        },
    }

    actual = serde.from_dict(dataklass=Foo, data=dict_input)
    assert actual
    assert actual.a == "Jerry"
    assert actual.b.c is False
