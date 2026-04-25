import json

from aeza_monitor.models import NotificationState, PromoData
from aeza_monitor.state import load_state, save_state


def test_state_roundtrip(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    monkeypatch.setenv("AEZA_STATE_FILE", str(state_file))

    import aeza_monitor.config as config
    import aeza_monitor.state as state_module

    config.STATE_FILE = state_file
    state_module.STATE_FILE = state_file

    state = NotificationState(
        last_notified=PromoData(
            found=True,
            location="Stockholm",
            plan_code="SWE-PROMO",
            price="1.99 €",
        )
    )

    save_state(state)
    loaded = load_state()

    assert loaded.last_notified is not None
    assert loaded.last_notified.location == "Stockholm"
    assert loaded.last_notified.plan_code == "SWE-PROMO"
    assert json.loads(state_file.read_text(encoding="utf-8"))["last_notified"]["price"] == "1.99 €"
