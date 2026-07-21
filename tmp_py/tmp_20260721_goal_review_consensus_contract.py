"""Contract tests for consensus-based snap-goal-review live evaluations."""

from __future__ import annotations

import unittest

from tmp_20260715_run_goal_review_evals import resolve_repeat, summarize_consensus


class GoalReviewConsensusContract(unittest.TestCase):
    """Verify stable defaults and majority verdict aggregation."""

    def test_fixture_evals_default_to_three_runs(self) -> None:
        """Full fixture evaluations should collect three independent verdicts."""
        self.assertEqual(resolve_repeat(fixtures=True, requested=None), 3)
        self.assertEqual(resolve_repeat(fixtures=False, requested=None), 1)
        self.assertEqual(resolve_repeat(fixtures=True, requested=2), 2)

    def test_two_of_three_runs_pass_consensus(self) -> None:
        """A fixture should pass when at least two of three runs pass."""
        summary = summarize_consensus(
            [
                {"id": "stable-case", "passed": True},
                {"id": "stable-case", "passed": False},
                {"id": "stable-case", "passed": True},
            ]
        )

        self.assertEqual(
            summary["stable-case"],
            {
                "passed_runs": 2,
                "total_runs": 3,
                "required_passes": 2,
                "passed": True,
            },
        )

    def test_one_of_three_runs_fails_consensus(self) -> None:
        """A fixture should fail when fewer than two of three runs pass."""
        summary = summarize_consensus(
            [
                {"id": "unstable-case", "passed": False},
                {"id": "unstable-case", "passed": True},
                {"id": "unstable-case", "passed": False},
            ]
        )

        self.assertFalse(summary["unstable-case"]["passed"])
        self.assertEqual(summary["unstable-case"]["required_passes"], 2)


if __name__ == "__main__":
    unittest.main()
