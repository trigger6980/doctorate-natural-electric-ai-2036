"""Tests for the 50-agent registry."""

from agent_registry import AGENTS, by_id, completeness, all_ids


def test_exactly_fifty():
    assert len(AGENTS) == 50
    assert completeness()["complete"] == 1
    assert all_ids() == list(range(1, 51))


def test_unique_ids_and_names():
    ids = [a.id for a in AGENTS]
    names = [a.name for a in AGENTS]
    assert len(set(ids)) == 50
    assert len(set(names)) == 50


def test_lookup():
    a = by_id(1)
    assert a is not None
    assert a.name == "Rail Floor Agent"
    assert by_id(50).name == "Enterprise Template Agent"
    assert by_id(0) is None
    assert by_id(51) is None


def test_every_card_named():
    for a in AGENTS:
        assert a.card.endswith(".md")
        assert a.card.startswith(f"{a.id:02d}-") or a.id >= 10


if __name__ == "__main__":
    test_exactly_fifty()
    test_unique_ids_and_names()
    test_lookup()
    test_every_card_named()
    print("All registry tests passed.")
