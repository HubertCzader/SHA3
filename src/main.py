import json
import string
import random

from tqdm import tqdm
from collections import defaultdict
from SHA3 import sha3_n
from profiling import profile, profile_results


def generate_random_message(length: int) -> str:
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


@profile(name='SHA3-224')
def sha3_224(m: str) -> str:
    return sha3_n(m, 224)


@profile(name='SHA3-256')
def sha3_256(m: str) -> str:
    return sha3_n(m, 256)


@profile(name='SHA3-384')
def sha3_384(m: str) -> str:
    return sha3_n(m, 384)


@profile(name='SHA3-512')
def sha3_512(m: str) -> str:
    return sha3_n(m, 512)


def main(max_power, iterations):
    time_measure = defaultdict(lambda: [])
    for i in range(max_power + 1):
        message_length = 10**i
        profile_results.clear()
        msg = generate_random_message(message_length)
        for _ in tqdm(range(iterations), desc=f"Message length: 10^{i}"):
            sha3_224(msg)
            sha3_256(msg)
            sha3_384(msg)
            sha3_512(msg)
        for key, value in profile_results.items():
            average_time = sum(value) / len(value)
            time_measure[key].append((message_length, average_time))
    time_measure_json = json.dumps(dict(time_measure))
    with open('./results/results.json', 'w') as f:
        f.write(time_measure_json)


if __name__ == "__main__":
    main(max_power=8, iterations=10)
