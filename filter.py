import argparse
import json
import os


def save_file(text, filename):
    print(f"> file: {filename}, text: {text}")
    with open(filename, "w") as f:
        f.write(text)


def filter(env: dict, prefix, sep='_'):
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
    print("> filter res:", result)
    return result


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('prefix', type=str)
    parser.add_argument('sep', type=str)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    env_list = [os.environ.get("SECRETS"),
                os.environ.get("VAR")]
    print("> env_list: ", env_list)
    result = ""
    for env in env_list:
        print("> env:", env)
        if not env:
            continue

        _env = json.loads(env)
        print("> env 2:", _env)
        _filtered = filter(_env, args.prefix, args.sep)
        result += _filtered

    save_file(result, args.file)
    print(f"{'*'*20} SAVED {'*'*20}")


if __name__ == "__main__":
    main()
