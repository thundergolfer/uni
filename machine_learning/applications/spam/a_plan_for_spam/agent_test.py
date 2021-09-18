import agent


def test_main(capsys):
    status = agent.main(["cleanup"])

    out, err = capsys.readouterr()
    assert "Done" in out
    assert err == ""
    assert status == 0
