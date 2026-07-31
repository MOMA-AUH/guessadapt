import argparse
import gzip

import pytest

from guessadapt.client import _open_fastq, _parse_adapters, main


FASTQ = "@read-1\nACGT\n+\nIIII\n"


def test_parse_adapters_strips_whitespace():
    assert _parse_adapters(" ACG , TTT ") == ["ACG", "TTT"]


def test_parse_adapters_rejects_empty_and_duplicate_entries():
    with pytest.raises(argparse.ArgumentTypeError, match="non-empty"):
        _parse_adapters("ACG,")
    with pytest.raises(argparse.ArgumentTypeError, match="duplicates"):
        _parse_adapters("ACG,ACG")


def test_open_fastq_supports_plain_and_gzip_files(tmp_path):
    plain_path = tmp_path / "reads.fastq"
    gzip_path = tmp_path / "reads.data"
    plain_path.write_text(FASTQ, encoding="utf-8")
    with gzip.open(gzip_path, "wt", encoding="utf-8") as handle:
        handle.write(FASTQ)

    with _open_fastq(plain_path) as handle:
        assert handle.read() == FASTQ
    with _open_fastq(gzip_path) as handle:
        assert handle.read() == FASTQ


def test_main_prints_a_deterministic_complete_result(tmp_path, monkeypatch, capsys):
    path = tmp_path / "reads.fastq"
    path.write_text(FASTQ, encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["guessadapt", "-a", "TTT,CGT,ACG", str(path)])

    main()

    assert capsys.readouterr().out == "ACG\t1\nCGT\t1\nTTT\t0\n"
