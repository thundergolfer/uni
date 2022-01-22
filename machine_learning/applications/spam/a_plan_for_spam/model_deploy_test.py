import io

import pytest

import model_deploy


def test_db_set():
    outfile = io.StringIO()

    model_deploy.db_set(
        db=outfile,
        key="foo",
        value="bar",
    )
    outfile.seek(0)
    content = outfile.read()
    assert content == "foo=bar\n"

    model_deploy.db_set(
        db=outfile,
        key="bee",
        value="biff",
    )
    outfile.seek(0)
    content = outfile.read()
    assert content == "foo=bar\nbee=biff\n"


def test_db_set_rejects_unprocessable_data():
    outfile = io.StringIO()
    key_msg = "'key' cannot contain"
    val_msg = "'value' cannot contain"
    with pytest.raises(ValueError, match=key_msg):
        model_deploy.db_set(
            db=outfile,
            key="bee=",
            value="biff",
        )
    with pytest.raises(ValueError, match=val_msg):
        model_deploy.db_set(
            db=outfile,
            key="bee",
            value="b=iff",
        )


def test_db_find():
    outfile = io.StringIO()
    pairs = [
        ("foo", "bar.biff"),
        ("bee", "biff"),
    ]
    for k, v in pairs:
        model_deploy.db_set(
            db=outfile,
            key=k,
            value=v,
        )
    for k, expected in pairs:
        outfile.seek(0)  # important to call so db_find can read all content.
        actual = model_deploy.db_find(
            db=outfile,
            key=k,
        )
        assert actual == expected


def test_db_find_on_missing_key():
    outfile = io.StringIO()
    model_deploy.db_set(
        db=outfile,
        key="foo",
        value="bar",
    )
    result = model_deploy.db_find(
        db=outfile,
        key="flim",
    )
    assert result is None
