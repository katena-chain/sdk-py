"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from nacl.exceptions import BadSignatureError
from katena_chain_sdk_py.crypto.base_key import BaseKey
from nacl.signing import VerifyKey


class PublicKey(BaseKey):
    # PublicKey is an Ed25519 public key wrapper (32 bytes).

    def __init__(self, key: bytes):
        super().__init__(key)

    def verify(self, message: bytes, signature: bytes) -> bool:
        # Indicates if a message and a signature match.
        try:
            VerifyKey(self.get_key()).verify(message, signature)
            return True
        except BadSignatureError:
            return False
