import argparse
import json
import os

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_file(text, filename):
    logger.info(f"Saving file: {filename}")
    with open(filename, "w") as f:
        f.write(text)


def _filter(env: dict, prefix, sep='_'):
    result = ""
    for k, v in env.items():
        if k == prefix:
            result += v
        elif k.startswith(prefix):
            _key: str = k.removeprefix(prefix).removeprefix(sep)
            result += f"{_key}={v}"
        else:
            continue
        result += '\n'
    return result


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('prefix', type=str)
    parser.add_argument('sep', type=str)

    args = parser.parse_args()
    return args


def main():
    logger.info(f"{'*'*20} START {'*'*20}")
    args = parse_args()
    prefix = args.prefix.upper()
    env_list = [
        os.environ.get("SECRETS"),
        os.environ.get("VAR")
    ]
    logger.info(f"VAR list input: {env_list[0]}")
    result = ""
    for env in env_list:
        logger.info(f"ENV: {env}")
        if not env:
            continue

        _env = json.loads(env)
        _filtered = _filter(_env, prefix, args.sep)
        result += _filtered

    save_file(result, args.file)
    logger.info(f"{'*'*20} SAVED {'*'*20}")


if __name__ == "__main__":
    main()
