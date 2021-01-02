from kurby.decrypt import decrypt


class TestDecrypt:
    def test_decrypt(self):
        key = b"LXgIVP&PorO68Rq7dTx8N^lP!Fa5sGJ^*XK"
        ciphertext = b"U2FsdGVkX1+UQFYDO21ygRddtiHnkwWi9c+8b6v7d57JXGRBMlCx/zY7ezFpbfa/"
        text = decrypt(ciphertext, key)
        assert text.decode("utf-8") == "/anime/narutoold/naruto-001.mp4"
