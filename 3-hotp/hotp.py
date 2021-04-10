from hashlib import sha1


def xor_bytes(bs1, bs2):
    return bytes(b1 ^ b2 for b1, b2 in zip(bs1, bs2))


def hmac_sha1(key, data):
    b = 64
    key_prime = key if len(key) <= b else sha1(key).digest()
    key_prime = key_prime + (b"\x00" * (b - len(key_prime)))
    assert len(key_prime) == b
    ipad = b"\x36" * b
    opad = b"\x5c" * b
    hs1 = sha1()
    hs1.update(xor_bytes(key_prime, ipad))
    hs1.update(data)
    hs2 = sha1()
    hs2.update(xor_bytes(key_prime, opad))
    hs2.update(hs1.digest())
    return hs2.digest()


def hotp(secret, counter):
    hs = hmac_sha1(secret, counter.to_bytes(8, byteorder="big"))
    offset = hs[-1] & 0xf
    p = bytes([hs[offset] & 0x7f]) + hs[offset+1:offset+4]
    dt = int.from_bytes(p, byteorder="big")
    return format(dt % (10**6), "06")


def test_xor():
    assert xor_bytes(b"\x00\xff", b"\x55\xaa") == b"\x55\x55"


def test_hmac_sha1_1():
    key = b"\x0b" * 20
    data = b"Hi There"
    digest = bytes.fromhex("b617318655057264e28bc0b6fb378c8ef146be00")
    assert hmac_sha1(key, data) == digest


def test_hmac_sha1_2():
    key = b"Jefe"
    data = b"what do ya want for nothing?"
    digest = bytes.fromhex("effcdf6ae5eb2fa2d27416d5f184df9c259a7c79")
    assert hmac_sha1(key, data) == digest


def test_hmac_sha1_3():
    key = b"\xaa" * 20
    data = b"\xdd" * 50
    digest = bytes.fromhex("125d7342b9ac11cd91a39af48aa17b4f63f175d3")
    assert hmac_sha1(key, data) == digest


def test_hmac_sha1_4():
    key = bytes.fromhex("0102030405060708090a0b0c0d0e0f10111213141516171819")
    data = b"\xcd" * 50
    digest = bytes.fromhex("4c9007f4026250c6bc8414f9bf50c86c2d7235da")
    assert hmac_sha1(key, data) == digest


def test_hmac_sha1_5():
    key = b"\x0c" * 20
    data = b"Test With Truncation"
    digest = bytes.fromhex("4c1a03424b55e07fe7f27be1d58bb9324a9a5a04")
    assert hmac_sha1(key, data) == digest


def test_hmac_sha1_6():
    key = b"\xaa" * 80
    data = b"Test Using Larger Than Block-Size Key - Hash Key First"
    digest = bytes.fromhex("aa4ae5e15272d00e95705637ce8a3b55ed402112")
    assert hmac_sha1(key, data) == digest


def test_hmac_sha1_7():
    key = b"\xaa" * 80
    data = b"Test Using Larger Than Block-Size Key and Larger Than One Block-Size Data"
    digest = bytes.fromhex("e8e99d0f45237d786d6bbaa7965c7808bbff1a91")
    assert hmac_sha1(key, data) == digest


def test_hotp():
    secret = b"12345678901234567890"
    otp_values = [
        "755224",
        "287082",
        "359152",
        "969429",
        "338314",
        "254676",
        "287922",
        "162583",
        "399871",
        "520489",
    ]
    assert [hotp(secret, counter) for counter, otp in enumerate(otp_values)] == otp_values


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        secret = bytes.fromhex(sys.argv[1])
    else:
        import os
        secret = os.urandom(20)
    print(f"secret: {secret.hex()}")
    for i in range(10):
        print(f"{i}: {hotp(secret, i)}")
