import notes


def test_add_then_list(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(notes, "NOTES", tmp_path / "notes.txt")
    assert notes.main(["add", "buy", "milk"]) == 0
    assert notes.main(["list"]) == 0
    assert "1. buy milk" in capsys.readouterr().out


def test_count_starts_empty(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(notes, "NOTES", tmp_path / "notes.txt")
    assert notes.main(["count"]) == 0
    assert capsys.readouterr().out.strip() == "0"


def test_unknown_command(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(notes, "NOTES", tmp_path / "notes.txt")
    assert notes.main(["frobnicate"]) == 1
    assert "unknown command" in capsys.readouterr().out


def test_add_with_nothing_to_add(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(notes, "NOTES", tmp_path / "notes.txt")
    assert notes.main(["add"]) == 1
    assert "nothing to add" in capsys.readouterr().out
