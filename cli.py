"""A comfortable netcat for the CyberGame JSONL wire.

The CLI deliberately knows no game verbs. It sends one opaque JSON value to
an explicit host/port and prints the opaque JSON response.
"""
import argparse
import json
import sys

from netutil import call


def exchange(host, port, raw, timeout):
    request = json.loads(raw)
    response = call(host, port, request, timeout=timeout)
    return json.dumps(response, ensure_ascii=False)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="send opaque JSONL requests to one CyberGame endpoint")
    parser.add_argument("host")
    parser.add_argument("port", type=int)
    parser.add_argument("request", nargs="?",
                        help="one JSON value; omit for line-oriented stdin")
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args(argv)

    if args.request is not None:
        try:
            print(exchange(args.host, args.port, args.request, args.timeout))
        except (json.JSONDecodeError, OSError, ValueError) as exc:
            parser.error(str(exc))
        return 0

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            print(exchange(args.host, args.port, line, args.timeout), flush=True)
        except (json.JSONDecodeError, OSError, ValueError) as exc:
            print(json.dumps({"cli_error": str(exc)}, ensure_ascii=False),
                  file=sys.stderr, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
