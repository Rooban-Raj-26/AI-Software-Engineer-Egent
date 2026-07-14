"""
Unit tests for the File Tool's safety guard.
Does not call any LLM — pure logic testing.
"""
import pytest
import tempfile
from app.tools.file_tool import write_file, FileToolError


def test_write_file_creates_file_in_base_dir():
    with tempfile.TemporaryDirectory() as tmp:
        path = write_file(tmp, "sub/hello.txt", "hello world")
        with open(path, encoding="utf-8") as f:
            assert f.read() == "hello world"


def test_write_file_rejects_path_traversal():
    with tempfile.TemporaryDirectory() as tmp:
        with pytest.raises(FileToolError):
            write_file(tmp, "../../etc/passwd", "malicious content")


def test_write_file_rejects_absolute_path_escape():
    with tempfile.TemporaryDirectory() as tmp:
        with pytest.raises(FileToolError):
            write_file(tmp, "../outside.txt", "escape attempt")