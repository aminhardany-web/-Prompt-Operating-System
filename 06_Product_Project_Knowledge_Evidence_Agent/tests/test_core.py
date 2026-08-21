import json
import tempfile
import unittest
import zipfile
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

    def test_docx_ingestion_preserves_paragraph_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "project"
            source.mkdir()
            docx = source / "evidence.docx"
            document_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p><w:r><w:t>Decision: Use controlled change.</w:t></w:r></w:p>
    <w:p><w:r><w:t>Risk: stale source.</w:t></w:r></w:p>
  </w:body>
</w:document>"""
            with zipfile.ZipFile(docx, "w") as archive:
                archive.writestr("word/document.xml", document_xml)

            workspace = root / "workspace"
            registry = ingest_path(source, workspace)
            self.assertEqual(len(registry["documents"]), 1)
            self.assertEqual(registry["documents"][0]["format"], "docx")

            result = analyze_workspace(workspace, source)
            self.assertEqual(len(result["claims"]), 2)
            self.assertEqual(result["claims"][0]["evidence"]["line_start"], 1)
            self.assertEqual(result["claims"][1]["evidence"]["line_start"], 2)


if __name__ == "__main__":
    unittest.main()
