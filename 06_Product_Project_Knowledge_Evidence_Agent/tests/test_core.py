import json
import tempfile
import unittest
from pathlib import Path

from pkea.core import analyze_workspace, ingest_path, write_report


class TestPKEA(unittest.TestCase):
    def test_ingest_analyze_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "project"
            source.mkdir()
            (source / "a.md").write_text(
                "# Project\nDecision: Use controlled change.\nRisk: stale source.\n",
                encoding="utf-8",
            )
            (source / "b.md").write_text(
                "Decision: Do not use controlled change.\n", encoding="utf-8"
            )
            workspace = root / "workspace"

            registry = ingest_path(source, workspace)
            self.assertEqual(len(registry["documents"]), 2)

            result = analyze_workspace(workspace, source)
            self.assertEqual(len(result["claims"]), 3)
            self.assertEqual(len(result["conflicts"]), 1)
            self.assertTrue(all(c["validation_status"] == "CANDIDATE" for c in result["claims"]))

            report = write_report(workspace)
            self.assertTrue(report.exists())
            parsed = json.loads((workspace / "analysis.json").read_text(encoding="utf-8"))
            self.assertTrue(parsed["controls"]["human_gate_required"])


if __name__ == "__main__":
    unittest.main()
