"""FASTQ parsing and adapter counting primitives."""

from collections import Counter
from collections.abc import Iterable, Iterator, Sequence
from itertools import islice


class FastqFormatError(ValueError):
    """Raised when an input stream does not contain complete FASTQ records."""


def parse_fastq(stream: Iterable[str]) -> Iterator[str]:
    """Yield sequences from a four-line-per-record FASTQ stream.

    This deliberately supports the conventional, single-line sequence and quality
    representation.  Malformed and truncated records raise :class:`FastqFormatError`
    rather than being silently ignored.
    """

    lines = iter(stream)
    record_number = 0
    while True:
        header = next(lines, None)
        if header is None:
            return

        record_number += 1
        record = [header, *(next(lines, None) for _ in range(3))]
        if any(line is None for line in record):
            raise FastqFormatError(f"Record {record_number} is incomplete")

        header, sequence, separator, quality = (
            line.rstrip("\r\n") for line in record
        )
        if not header.startswith("@"):
            raise FastqFormatError(
                f"Record {record_number} header must start with '@'"
            )
        if not separator.startswith("+"):
            raise FastqFormatError(
                f"Record {record_number} separator must start with '+'"
            )
        if len(sequence) != len(quality):
            raise FastqFormatError(
                f"Record {record_number} sequence and quality lengths differ"
            )
        yield sequence


def count_adapters(
    stream: Iterable[str], adapters: Sequence[str], limit: int | None = None
) -> Counter[str]:
    """Count reads that contain each adapter sequence.

    ``limit`` is the maximum number of reads to inspect.  A limit of zero is
    valid and produces no counts; negative limits are rejected.
    """

    if limit is not None and limit < 0:
        raise ValueError("limit must be non-negative")

    records = parse_fastq(stream)
    if limit is not None:
        records = islice(records, limit)

    counts: Counter[str] = Counter()
    for sequence in records:
        for adapter in adapters:
            if adapter in sequence:
                counts[adapter] += 1
    return counts
