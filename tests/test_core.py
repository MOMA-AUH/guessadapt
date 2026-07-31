import pytest

from guessadapt.core import FastqFormatError, count_adapters, parse_fastq


@pytest.fixture
def stream():
    return iter(
        [
            "@SequenceA",
            "ACGT",
            "+",
            "IIII",
            "@SequenceB",
            "CGTT",
            "+",
            "IIII",
            "@SequenceC",
            "GACG",
            "+",
            "IIII",
            "@SequenceD",
            "TTTC",
            "+",
            "IIII",
            "@SequenceE",
            "TCGT",
            "+",
            "IIII",
        ]
    )


@pytest.fixture
def adapters():
    return ["ACG", "CGT", "TTT"]


def test_parser():
    records = list(
        parse_fastq(iter(["@SequenceA", "ACGT", "+", "IIII", "@SequenceB", "TCGA", "+", "IIII"]))
    )
    assert records == ["ACGT", "TCGA"]


def test_parser_rejects_incomplete_record():
    with pytest.raises(FastqFormatError, match="incomplete"):
        list(parse_fastq(iter(["@SequenceA", "ACGT", "+"])))


def test_parser_rejects_invalid_fastq_structure():
    with pytest.raises(FastqFormatError, match="header must start"):
        list(parse_fastq(iter(["SequenceA", "ACGT", "+", "IIII"])))

    with pytest.raises(FastqFormatError, match="lengths differ"):
        list(parse_fastq(iter(["@SequenceA", "ACGT", "+", "III"])))


def test_count_adapters(stream, adapters):
    counts = count_adapters(stream=stream, adapters=adapters)
    assert counts == {"ACG": 2, "CGT": 3, "TTT": 1}


def test_count_adapters_with_limit(stream, adapters):
    counts = count_adapters(stream=stream, adapters=adapters, limit=3)
    assert counts == {"ACG": 2, "CGT": 2}


def test_count_adapters_with_zero_limit(stream, adapters):
    assert count_adapters(stream=stream, adapters=adapters, limit=0) == {}


def test_count_adapters_does_not_read_past_limit(adapters):
    stream = iter(["@SequenceA", "ACGT", "+", "IIII", "@Incomplete"])
    assert count_adapters(stream=stream, adapters=adapters, limit=1) == {
        "ACG": 1,
        "CGT": 1,
    }


def test_count_adapters_rejects_negative_limit(stream, adapters):
    with pytest.raises(ValueError, match="non-negative"):
        count_adapters(stream=stream, adapters=adapters, limit=-1)
