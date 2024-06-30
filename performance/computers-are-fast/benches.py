import hashlib
import json
import pathlib
import os
import subprocess
import urllib.request
from http.server import BaseHTTPRequestHandler
BaseHTTPRequestHandler
from io import BytesIO, StringIO


hints: dict[str, list] = {}
notes: dict[str, list] = {}

def bench_loop(n: int):
    """
    Number to guess: How many iterations of an empty loop can we go through in a second?
    """
    for _ in range(n):
        pass

hints[bench_loop.__name__] = [
    "A CPU can execute around a few billion instructions per second."
]

def bench_parse_http_request(n: int):
    """
    Number to guess: How many HTTP GET requests can we parse in a second?
    """
    class HTTPRequest(BaseHTTPRequestHandler):
        def __init__(self, request_text):
            self.rfile = BytesIO(request_text)
            self.raw_requestline = self.rfile.readline()
            self.error_code = self.error_message = None
            self.parse_request()

        def send_error(self, code, message):
            self.error_code = code
            self.error_message = message

    request_text = b"""GET / HTTP/1.1
    Host: localhost:8001
    Connection: keep-alive
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
    Accept-Encoding: gzip, deflate, sdch
    Accept-Language: en-GB,en-US;q=0.8,en;q=0.6
    """
    for _ in range(n):
        _ = HTTPRequest(request_text)


def bench_dict_mutation(n: int):
    """
    Number to guess: How many entries can we add to a dictionary in a second?
    """
    d = {}
    max_entries = 1000
    for i in range(n):
        d[i % max_entries] = i


def bench_download_webpage(n: int):
    """
    Number to guess: How many times can we download google.com in a second?
    """
    for _ in range(n):
        response = urllib.request.urlopen("http://google.com")
        response.read()

def bench_run_python(n: int):
    """
    Number to guess: How many times can we start the Python interpreter in a second?
    """
    for _ in range(n):
        subprocess.run("python3 -c ''", shell=True, check=True)

hints[bench_run_python.__name__] = [
    "This is much less than 100 million :)"
]

def bench_write_to_disk(n: int):
    """
    Number to guess: How many bytes can we write to an output file in a second?
    """
    def cleanup(f, name):
        f.flush()
        os.fsync(f.fileno())
        f.close()
        try:
            os.remove(name)
        except OSError:
            pass

    chunk_size = 1_000_000  # 1 megabyte
    data_chunk = b"a" * chunk_size
    name = "/tmp/bench-write-to-disk"
    bytes_written = 0
    with open(name, 'wb') as f:
        while bytes_written < n:
            written = f.write(data_chunk)
            bytes_written += chunk_size
            assert written == chunk_size, "incomplete disk write"
        cleanup(f, name)


hints[bench_write_to_disk.__name__] = [
    "we make sure everything is sync'd to disk before exiting"
]

def bench_write_to_memory(n: int):
    """
    Number to guess: How many bytes can we write to a string in memory in a second?
    """
    chunk_size = 1_000_000  # 1 megabyte
    data_chunk = "a" * chunk_size
    output = StringIO()
    bytes_written = 0
    while bytes_written < n:
        _ = output.write(data_chunk)
        bytes_written += chunk_size
    output.getvalue()


def bench_json_parse(n: int):
    """
    Number to guess: parse iterations possible within one second.
    """
    data = pathlib.Path("message.json").read_text()
    for _ in range(n):
        json.loads(data)


def bench_sha256_digest(n: int):
    """
    Number to guess: bytes hashed in one second.
    """
    CHUNK_SIZE = 10_000
    s = b'a' * CHUNK_SIZE
    h = hashlib.md5()
    bytes_hashed = 0
    while bytes_hashed < n:
        h.update(s)
        bytes_hashed += CHUNK_SIZE
    h.digest()

hints[bench_sha256_digest.__name__] = [
    "sha256 is cryptographically secure and slower than md5, siphash, CRC32."
]


def bench_fill_array(n: int):
    """
    Number to guess: bytes written to array in one second.
    """
    array = bytearray(n)
    j = 1
    for i in range(n):
        j *= 2
        if j > n:
            j -= n
        array[i] = j % 256  # Ensure value fits in a byte
    print(array[n // 7], end='')


def bench_fill_array_out_of_order(n: int):
    """
    Number to guess: bytes written to array in one second.
    """
    array = bytearray(n)
    jmp_around = 1
    for _ in range(n):
        jmp_around = jmp_around * 2
        if jmp_around > n:
            jmp_around -= n
        array[jmp_around % n] = jmp_around % 256  # Ensure index and value fit in range

    print(array[n // 7])
