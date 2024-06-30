import dataclasses
import json
import pathlib
import platform
import sys
import timeit

import benches

benchmarks = [
    "bench_loop",
    "bench_dict_mutation",
    "bench_parse_http_request",
    "bench_download_webpage",
    "bench_run_python",
    "bench_create_files",
    "bench_write_to_disk",
    "bench_write_to_memory",
    "bench_json_parse",
    "bench_sha256_digest",
    "bench_fill_array",
    "bench_fill_array_out_of_order",
]

# The possible guesses proceed through 10 orders of magnitude.
choices = [10 ** i for i in range(10)]

@dataclasses.dataclass
class BenchResult:
    name: str
    platform: str
    lang_version: str
    # TODO: cpu info, mem info, ssd info
    # TODO: mount info for /tmp/
    answer: int
    # How many milliseconds benchmark took on answer.
    answer_duration_ms: float
    # Estimation/extrapolation of what N would be for bench
    # to take exactly one second.
    estimated_n: int
    bench_source: str
    bench_doc: str
    hints: list[str] | None = None
    language: str = "python"

def snake_number_format(z: int):
    if z < 0:
        return '-' + snake_number_format(-z)
    s = []
    while z:
        if len(s) % 4 == 3:
            s.append("_")
        s.append(str(z % 10))
        z //= 10
    return ''.join(reversed(s))

def extract_clean_bench_source(bench_fn: callable) -> tuple[str, str]:
    """
    Grab the source code of the bench function without the docstring.
    """
    import inspect
    import textwrap
    src = inspect.getsource(bench_fn)   
    src = textwrap.dedent(src) 
    seen_start_of_docstring = False
    lines = [ln.replace("    ", "\t") for ln in src.splitlines()]
    for i, line in enumerate(lines):
        if not seen_start_of_docstring and line.strip().startswith('"""'):
            seen_start_of_docstring = True
            continue
        elif line.strip().endswith('"""'):
            if seen_start_of_docstring:
                break
            else:
                RuntimeError("unexpected end of docstring")
    return inspect.getdoc(bench_fn), textwrap.dedent("\n".join(lines[i+1:]))


def run_benchmark(name: str, validate: bool = True) -> BenchResult:
    """
    Exercises a benchmark by first gathering hardware and OS information
    about the host and then running the bench function against each 'guess'
    option until it reaches the correct answer.

    This function is slow because it runs 5 iterations to confirm the
    correct answer.
    """
    print(f"running benchmark {name} on {platform.platform()} {sys.version}")

    bench_fn = getattr(benches, name)
    for n in choices:
        stmt = lambda: bench_fn(n)  # noqa: E731
        duration_s = timeit.timeit(stmt, number=1)
        print(f"N {snake_number_format(n):10}: {duration_s * 1000:.3f}ms")
        # Found answer. 
        # If we ran next answer we'd exceed one second.
        # NB: we're assuming that all benchmarks have linear scaling. 
        if 0.1 < duration_s <= 1.0:
            estimated_n = int(n / duration_s)
            print(
                f"benchmark {name} answer: {snake_number_format(n)} (est. exact N={snake_number_format(estimated_n)})"
            )
            break
    else:
        estimated_n = int(n / duration_s)

    # Confirm by measure on estimated_n for more iterations.
    if validate:
        cofirm_stmt = lambda: bench_fn(estimated_n)  # noqa: E731
        if name in {"bench_write_to_disk", "bench_write_to_memory", "bench_download_webpage"}:
            delta_tolerance = 0.5
        elif n < 10_000:
            delta_tolerance = 0.25
        else:
            delta_tolerance = 0.2
        iterations = 5
        duration_total_s = timeit.timeit(cofirm_stmt, number=iterations)
        duration_s = duration_total_s / 5
        delta = abs(duration_s - 1.0)
        assert delta < delta_tolerance, f"inaccurate benchmark on {name}: {delta=} (took {duration_s}s on N={estimated_n})"
        print(f"accurate benchmark on {name}: {delta=} (took {duration_s}s on N={estimated_n})")

    doc, source = extract_clean_bench_source(bench_fn)
    return BenchResult(
        name=name,
        platform=platform.platform(),
        lang_version=sys.version,
        answer=n,
        answer_duration_ms=duration_s * 1000,
        estimated_n=estimated_n,
        bench_doc=doc,
        bench_source=source,
        hints=benches.hints.get(name, []),
    )


def main():
    skip = {
        # Uncomment if running without internet connectivity.
        # "bench_download_webpage"
    }
    results = [
        run_benchmark(b)
        for b in benchmarks
        if b not in skip
    ] 
    out = pathlib.Path("out.json")
    out.write_text(json.dumps([dataclasses.asdict(d) for d in results]))
    


if __name__ == "__main__":
    main()
