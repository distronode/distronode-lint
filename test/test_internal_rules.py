"""Tests for internal rules."""
from distronodelint._internal.rules import BaseRule


def test_base_rule_url() -> None:
    """Test that rule URL is set to expected value."""
    rule = BaseRule()
    assert rule.url == "https://distronode-lint.readthedocs.io/rules/"
