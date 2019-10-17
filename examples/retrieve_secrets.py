"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from katena_chain_sdk_py.entity.certify.common import get_type_secret_nacl_box_v1
from katena_chain_sdk_py.exceptions.api_exception import ApiException
from katena_chain_sdk_py.exceptions.client_exception import ClientException
from katena_chain_sdk_py.transactor import Transactor
from base64 import b64encode

from katena_chain_sdk_py.utils.crypto import create_private_key_x25519_from_base64


def main():
    # Bob wants to read a nacl box secret from Alice to decrypt an off-chain data

    # Common Katena network information
    api_url = "https://api.test.katena.transchain.io/api/v1"

    # Alice Katena network information
    alice_company_chain_id = "abcdef"

    # Create a Katena API helper
    transactor = Transactor(api_url)

    # Nacl box information
    bob_crypt_private_key_base64 = "quGBP8awD/J3hjSvwGD/sZRcMDks8DPz9Vw0HD4+zecqJP0ojBoc4wQtyq08ywxUksTkdz0/rQNkOsEZBwqWTw=="
    bob_crypt_private_key = create_private_key_x25519_from_base64(bob_crypt_private_key_base64)

    # Certificate uuid Alice wants to retrieve
    secret_uuid = "2075c941-6876-405b-87d5-13791c0dc53a"

    try:
        # Retrieve a version 1 of a certificate from Katena
        tx_wrappers = transactor.retrieve_secrets(alice_company_chain_id, secret_uuid)

        for tx_wrapper in tx_wrappers.get_txs():
            tx_data = tx_wrapper.get_tx().get_data()

            print("Transaction status")
            print("  Code    : {}".format(tx_wrapper.get_status().get_code()))
            print("  Message : {}".format(tx_wrapper.get_status().get_message()))

            if tx_data.get_type() == get_type_secret_nacl_box_v1():
                print("SecretNaclBoxV1")
                print("  Id                : {}".format(tx_data.get_id()))
                print("  Data sender       : {}".format(b64encode(tx_data.get_sender().get_key()).decode("utf-8")))
                print("  Data nonce        : {}".format(b64encode(tx_data.get_nonce()).decode("utf-8")))
                print("  Data content      : {}".format(b64encode(tx_data.get_content()).decode("utf-8")))

            decrypted_content = bob_crypt_private_key.open(tx_data.get_content(), tx_data.get_sender(),
                                                           tx_data.get_nonce()).decode("utf-8")
            if decrypted_content == "":
                decrypted_content = "Unable to decrypt"

            print("  Decrypted content : {}".format(decrypted_content))
            print()
    except (ApiException, ClientException) as e:
        print(e)


main()
