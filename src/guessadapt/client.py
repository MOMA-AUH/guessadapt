import argparse
import gzip
from collections.abc import Iterator
from pathlib import Path

from guessadapt import __version__
from guessadapt.core import count_adapters


DEFAULT_ADAPTERS = ("AGATCGGAAGAGC", "TGGAATTCTCGG", "CTGTCTCTTATA")


def _parse_adapters(value: str) -> list[str]:
    adapters = [adapter.strip() for adapter in value.split(",")]
    if not all(adapters):
        raise argparse.ArgumentTypeError("adapters must be non-empty sequences")
    if len(set(adapters)) != len(adapters):
        raise argparse.ArgumentTypeError("adapters must not contain duplicates")
    return adapters


def _open_fastq(path: Path) -> Iterator[str]:
    """Open a plain-text or gzip-compressed FASTQ file as text."""

    with path.open("rb") as raw_handle:
        is_gzip = raw_handle.read(2) == b"\x1f\x8b"
    opener = gzip.open if is_gzip else open
    return opener(path, "rt", encoding="utf-8")


def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    parser.add_argument('fastq', help='path to input FASTQ file')
    parser.add_argument('--limit', '-n', type=int, help='maximal number of reads to consider')
    parser.add_argument(
        '--adapters',
        '-a',
        type=_parse_adapters,
        default=','.join(DEFAULT_ADAPTERS),
        metavar='SEQUENCES',
        help='comma-separated list of adapters (default: %(default)s)',
    )

    args = parser.parse_args()

    try:
        with _open_fastq(Path(args.fastq)) as handle:
            adapter_counts = count_adapters(
                stream=handle, limit=args.limit, adapters=args.adapters
            )
    except (OSError, ValueError) as error:
        parser.error(str(error))

    for adapter in sorted(args.adapters, key=lambda adapter: (-adapter_counts[adapter], adapter)):
        print(adapter, adapter_counts[adapter], sep='\t')
