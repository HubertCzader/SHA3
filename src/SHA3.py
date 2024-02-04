import struct


def pad(msg: str, r: int) -> bytearray:
    assert isinstance(msg, str)
    msg = msg.encode('utf-8')
    q = r - (len(msg) % r)
    if q == 1:
        msg += bytes([0x86])
    elif q == 2:
        msg += bytes([0x06]) + bytes([0x80])
    else:
        msg += bytes([0x06]) + (q - 2) * bytes([0x00]) + bytes([0x80])
    return bytearray(msg)


def convertToInts(state: bytearray) -> list:
    state_ints = [[0 for _ in range(5)] for _ in range(5)]
    for y in range(5):
        for x in range(5):
            start_index = 8 * (5 * y + x)
            state_ints[x][y] = struct.unpack("<Q", state[start_index:start_index + 8])[0]
    return state_ints


def convertToBytes(state: list) -> bytearray:
    state_bytes = bytearray()
    for y in range(5):
        for x in range(5):
            state_bytes.extend(struct.pack("<Q", state[x][y]))
    return state_bytes


def rot(a: int, b: int) -> int:
    return ((a << b) | (a >> (64 - b))) & ((1 << 64) - 1)


def oneRound(state: list, RC: int, rotations: list) -> list:
    C = [state[i][0] ^ state[i][1] ^ state[i][2] ^ state[i][3] ^ state[i][4] for i in range(5)]
    D = [C[(i - 1) % 5] ^ rot(C[(i + 1) % 5], 1) for i in range(5)]
    for i in range(5):
        for j in range(5):
            state[i][j] ^= D[i]

    B = [[0 for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            B[j][(2 * i + 3 * j) % 5] = rot(state[i][j], rotations[i][j])

    for i in range(5):
        for j in range(5):
            state[i][j] = B[i][j] ^ ((~B[(i + 1) % 5][j]) & B[(i + 2) % 5][j])

    state[0][0] ^= RC
    return state


def compute(state: bytearray, n: int, RC: list, rotations: list) -> bytearray:
    state = convertToInts(state)
    for i in range(n):
        state = oneRound(state, RC[i], rotations)
    return convertToBytes(state)


def sha3_n(m: str, d: int) -> str:

    if d not in [224, 256, 384, 512]:
        raise ValueError(f'Invalid SHA3 instance: SHA3-{d}.\
        Only SHA3-224, SHA3-256, SHA3-384 and SHA3-512 are supported.')

    n = 24
    c = d * 2
    r = (1600 - c) // 8
    RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
          0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
          0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
          0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
          0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
          0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008]

    rotations = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
    padded_message = pad(m, r)
    state = bytearray(200)

    for i in range(0, len(padded_message), r):
        for j in range(r):
            if i + j < len(padded_message):
                state[j] ^= padded_message[i + j]
        state = compute(state, n, RC, rotations)
    msg = bytes(state[:d//8])
    return msg.hex()





