"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from katena_chain_sdk_py.exceptions.api_exception import ApiException
from katena_chain_sdk_py.exceptions.client_exception import ClientException
from katena_chain_sdk_py.transactor import Transactor
from katena_chain_sdk_py.utils.crypto import create_private_key_ed25519_from_base64


def main():
    # Alice wants to certify an ed25519 signature of an off-chain data

    # Common Katena network information
    api_url = "https://api.test.katena.transchain.io/api/v1"
    chain_id = "katena-chain-test"

    # Alice Katena network information
    alice_sign_private_key_base64 = "7C67DeoLnhI6jvsp3eMksU2Z6uzj8sqZbpgwZqfIyuCZbfoPcitCiCsSp2EzCfkY52Mx58xDOyQLb1OhC7cL5A== "
    alice_company_chain_id = "abcdef"
    alice_sign_private_key = create_private_key_ed25519_from_base64(alice_sign_private_key_base64)

    # Create a Katena API helper
    transactor = Transactor(api_url, chain_id, alice_company_chain_id, alice_sign_private_key)

    try:
        # Off-chain information Alice wants to send
        certificate_uuid = "2075c941-6876-405b-87d5-13791c0dc53a"
        data_signature = alice_sign_private_key.sign("off_chain_data_to_sign_from_py".encode("utf-8"))

        # Send a version 1 of a certificate d25519 on Katena
        tx_status = transactor.send_certificate_ed25519_v1(certificate_uuid, alice_sign_private_key.get_public_key(),
                                                           data_signature)

        print("Transaction status")
        print("  Code    : {}".format(tx_status.get_code()))
        print("  Message : {}".format(tx_status.get_message()))
    except (ApiException, ClientException) as e:
        print(e)


main()
