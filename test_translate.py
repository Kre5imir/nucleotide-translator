"""Tests for the six-frame ORF finder in translate.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "translate.py"


class TranslateScriptTests(unittest.TestCase):
    def test_script_reads_a_sequence_file_and_reports_frames(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            seq_file = Path(tmpdir) / "seq.fa"
            seq_file.write_text(
                textwrap.dedent(
                    """>example
                    ATGAAATAG
                    """
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT)],
                input=f"{seq_file}\n\n",
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Frame 1", result.stdout)
            self.assertIn("ORF 1", result.stdout)
            self.assertIn("MK", result.stdout)

    def test_missing_file_exits_with_error(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input="missing_file.txt\n\n",
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("error unable to read file or file does not exist!!!", result.stdout)

    def test_script_handles_a_fasta_header_and_sequence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            seq_file = Path(tmpdir) / "gene.fa"
            seq_file.write_text(
                textwrap.dedent(
                    """>gene1
                    ATGGCTTCAAAATAG
                    """
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT)],
                input=f"{seq_file}\n\n",
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn(">gene1", result.stdout)
            self.assertIn("Frame 1", result.stdout)
            self.assertIn("MASK", result.stdout)


if __name__ == "__main__":
    unittest.main()
