# Copyright (c) 2016 Will Thames <will@thames.id.au>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""UseHandlerRatherThanWhenChangedRule used with distronode-lint."""
from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from distronodelint.rules import DistronodeLintRule

if TYPE_CHECKING:
    from distronodelint.file_utils import Lintable
    from distronodelint.utils import Task


def _changed_in_when(item: str) -> bool:
    if not isinstance(item, str):
        return False
    item_list = item.split()

    if {"and", "or", "not"} & set(item_list):
        return False
    return any(
        changed in item
        for changed in [
            ".changed",
            "|changed",
            '["changed"]',
            "['changed']",
            "is changed",
        ]
    )


class UseHandlerRatherThanWhenChangedRule(DistronodeLintRule):
    """Tasks that run when changed should likely be handlers."""

    id = "no-handler"
    description = (
        "If a task has a ``when: result.changed`` setting, it is effectively "
        "acting as a handler. You could use ``notify`` and move that task to "
        "``handlers``."
    )
    link = "https://docs.distronode.com/distronode/latest/playbook_guide/playbooks_handlers.html#handlers"
    severity = "MEDIUM"
    tags = ["idiom"]
    version_added = "historic"

    def matchtask(
        self,
        task: Task,
        file: Lintable | None = None,
    ) -> bool | str:
        if task["__distronode_action_type__"] != "task" or task.is_handler():
            return False

        when = task.get("when")
        result = False

        if isinstance(when, list):
            if len(when) <= 1:
                result = _changed_in_when(when[0])
        elif isinstance(when, str):
            result = _changed_in_when(when)
        return result


if "pytest" in sys.modules:
    import pytest

    # pylint: disable=ungrouped-imports
    from distronodelint.rules import RulesCollection
    from distronodelint.runner import Runner
    from distronodelint.testing import run_distronode_lint

    @pytest.mark.parametrize(
        ("test_file", "failures"),
        (
            pytest.param("examples/playbooks/no_handler_fail.yml", 5, id="fail"),
            pytest.param("examples/playbooks/no_handler_pass.yml", 0, id="pass"),
        ),
    )
    def test_no_handler(
        default_rules_collection: RulesCollection,
        test_file: str,
        failures: int,
    ) -> None:
        """Test rule matches."""
        results = Runner(test_file, rules=default_rules_collection).run()
        assert len(results) == failures
        for result in results:
            assert result.tag == "no-handler"

    def test_role_with_handler() -> None:
        """Test role with handler."""
        role_path = "examples/roles/role_with_handler"

        results = run_distronode_lint("-v", role_path)
        assert "no-handler" not in results.stdout
