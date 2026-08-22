import json
import tempfile
import unittest
from pathlib import Path

from pkea.core import analyze_workspace, ingest_path, write_report
from pkea.review import append_review, latest_reviews


class TestReviewLedger(unittest.TestCase):
    def test_review_is_append_only_and_visible_in_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "project"
            source.mkdir()
            (source / "a.md").write_text("Requirement: Every claim needs evidence.\n", encoding="utf-8")
            workspace = root / "workspace"
            ingest_path(source, workspace)
            result = analyze_workspace(workspace, source)
            claim_id = result["claims"][0]["claim_id"]

            first = append_review(workspace, claim_id=claim_id, decision="NEEDS_REVIEW", reviewer="alice")
            second = append_review(workspace, claim_id=claim_id, decision="VALIDATED", reviewer="bob", note="Source checked")

            self.assertNotEqual(first["event_id"], second["event_id"])
            reviews = latest_reviews(workspace)
            self.assertEqual(reviews[claim_id]["decision"], "VALIDATED")
            ledger_lines = (workspace / "validation_ledger.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(ledger_lines), 2)

            report = write_report(workspace).read_text(encoding="utf-8")
            self.assertIn("VALIDATED", report)
            self.assertIn("bob", report)
            json.loads(ledger_lines[0])


if __name__ == "__main__":
    unittest.main()
