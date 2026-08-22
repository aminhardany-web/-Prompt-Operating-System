import tempfile
import unittest
from pathlib import Path

from pkea.core import analyze_workspace, ingest_path


class FakeAdapter:
    def __init__(self, claims):
        self.claims = claims

    def extract_claims(self, **kwargs):
        return self.claims


class TestLLMValidation(unittest.TestCase):
    def test_valid_llm_claim_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "project"
            source.mkdir()
            (source / "a.md").write_text("# Project\nThe system must retain evidence.\n", encoding="utf-8")
            workspace = root / "workspace"
            ingest_path(source, workspace)
            adapter = FakeAdapter([{
                "type": "requirement",
                "text": "The system must retain evidence.",
                "line_start": 2,
                "line_end": 2,
                "quote": "The system must retain evidence.",
            }])
            result = analyze_workspace(workspace, source_root=source, adapter=adapter)
            self.assertEqual(len(result["claims"]), 1)
            self.assertEqual(result["controls"]["extraction_mode"], "llm_with_deterministic_evidence_validation")
            self.assertEqual(result["controls"]["llm_claims_rejected_by_evidence_validation"], 0)

    def test_fabricated_quote_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "project"
            source.mkdir()
            (source / "a.md").write_text("# Project\nThe system must retain evidence.\n", encoding="utf-8")
            workspace = root / "workspace"
            ingest_path(source, workspace)
            adapter = FakeAdapter([{
                "type": "requirement",
                "text": "The system must delete evidence.",
                "line_start": 2,
                "line_end": 2,
                "quote": "The system must delete evidence.",
            }])
            result = analyze_workspace(workspace, source_root=source, adapter=adapter)
            self.assertEqual(len(result["claims"]), 0)
            self.assertEqual(result["controls"]["llm_claims_rejected_by_evidence_validation"], 1)

    def test_valid_quote_with_unsupported_claim_text_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "project"
            source.mkdir()
            (source / "a.md").write_text("# Project\nDecision: Retain all project evidence.\n", encoding="utf-8")
            workspace = root / "workspace"
            ingest_path(source, workspace)
            adapter = FakeAdapter([{
                "type": "decision",
                "text": "Delete all project evidence.",
                "line_start": 2,
                "line_end": 2,
                "quote": "Decision: Retain all project evidence.",
            }])
            result = analyze_workspace(workspace, source_root=source, adapter=adapter)
            self.assertEqual(len(result["claims"]), 0)
            self.assertEqual(result["controls"]["llm_claims_rejected_by_evidence_validation"], 1)


if __name__ == "__main__":
    unittest.main()
