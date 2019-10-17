"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from katena_chain_sdk_py.exceptions.api_exception import ApiException
from katena_chain_sdk_py.exceptions.client_exception import ClientException
from katena_chain_sdk_py.transactor import Transactor
from katena_chain_sdk_py.utils.crypto import create_private_key_ed25519_from_base64, create_private_key_x25519_from_base64, \
    create_public_key_x25519_from_base64


def main():
    # Alice wants to send a nacl box secret to Bob to encrypt an off-chain data

    # Common Katena network information
    api_url = "https://api.test.katena.transchain.io/api/v1"
    chain_id = "katena-chain-test"

    # Alice Katena network information
    alice_sign_private_key_base64 = "7C67DeoLnhI6jvsp3eMksU2Z6uzj8sqZbpgwZqfIyuCZbfoPcitCiCsSp2EzCfkY52Mx58xDOyQLb1OhC7cL5A== "
    alice_company_chain_id = "abcdef"
    alice_sign_private_key = create_private_key_ed25519_from_base64(alice_sign_private_key_base64)

    # Nacl box information
    alice_crypt_private_key_base64 = "nyCzhimWnTQifh6ucXLuJwOz3RgiBpo33LcX1NjMAsP1ZkQcdlDq64lTwxaDx0lq6LCQAUeYywyMUtfsvTUEeQ=="
    alice_crypt_private_key = create_private_key_x25519_from_base64(alice_crypt_private_key_base64)
    bob_crypt_public_key_base64 = "KiT9KIwaHOMELcqtPMsMVJLE5Hc9P60DZDrBGQcKlk8="
    bob_crypt_public_key = create_public_key_x25519_from_base64(bob_crypt_public_key_base64)

    # Create a Katena API helper
    transactor = Transactor(api_url, chain_id, alice_company_chain_id, alice_sign_private_key)

    # Off-chain information Alice wants to send
    secret_uuid = "2075c941-6876-405b-87d5-13791c0dc53a"
    content = "off_chain_secret_to_crypt_from_py"

    try:
        # Alice will use its private key and Bob's public key to encrypt a message
        encrypted_message, nonce = alice_crypt_private_key.seal(content.encode("utf-8"), bob_crypt_public_key)

        # Send a version 1 of a secret nacl box on Katena
        tx_status = transactor.send_secret_nacl_box_v1(secret_uuid, alice_crypt_private_key.get_public_key(), nonce,
                                                       encrypted_message)

        print("Transaction status")
        print("  Code    : {}".format(tx_status.get_code()))
        print("  Message : {}".format(tx_status.get_message()))
    except (ApiException, ClientException) as e:
        print(e)


main()
