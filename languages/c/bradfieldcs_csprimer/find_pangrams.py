import sys


def is_pangram(phrase):
    return len(set(ch for ch in phrase.lower() if ch.isalpha())) == 26


if __name__ == '__main__':
    for line in sys.stdin:
        if is_pangram(line):
            sys.stdout.write(line)
