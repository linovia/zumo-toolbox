from __future__ import unicode_literals
from demo import Zumo


def test_led(monkeypatch):
    zumo = Zumo()
    monkeypatch.setattr("os.getcwd", lambda: None)
    result = zumo.led(True)
    assert result == b"\x02\x01\x00\x00"
    result = zumo.led(False)
    assert result == b"\x02\x00\x00\x00"
