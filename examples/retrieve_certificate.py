"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from katena_chain_sdk_py.entity.certify.common import get_type_certificate_raw_v1, get_type_certificate_ed25519_v1
from katena_chain_sdk_py.exceptions.api_exception import ApiException
from katena_chain_sdk_py.exceptions.client_exception import ClientException
from katena_chain_sdk_py.transactor import Transactor
from base64 import b64encode


def main():
    # Alice wants to retrieve a certificate

    # Common Katena network information
    api_url = "https://api.test.katena.transchain.io/api/v1"

    # Alice Katena network information
    alice_company_chain_id = "abcdef"

    # Create a Katena API helper
    transactor = Transactor(api_url)

    # Certificate uuid Alice wants to retrieve
    certificate_uuid = "2075c941-6876-405b-87d5-13791c0dc53a"

    try:
        # Retrieve a version 1 of a certificate from Katena
        tx_wrapper = transactor.retrieve_certificate(alice_company_chain_id, certificate_uuid)
        tx_data = tx_wrapper.get_tx().get_data()

        print("Transaction status")
        print("  Code    : {}".format(tx_wrapper.get_status().get_code()))
        print("  Message : {}".format(tx_wrapper.get_status().get_message()))

        if tx_data.get_type() == get_type_certificate_raw_v1():
            print("CertificateRawV1")
            print("  Id    : {}".format(tx_data.get_id()))
            print("  Value : {}".format(tx_data.get_value().decode("utf-8")))

        if tx_data.get_type() == get_type_certificate_ed25519_v1():
            print("CertificateEd25519V1")
            print("  Id             : {}".format(tx_data.get_id()))
            print("  Data signer    : {}".format(b64encode(tx_data.get_signer().get_key()).decode("utf-8")))
            print("  Data signature : {}".format(b64encode(tx_data.get_signature()).decode("utf-8")))
    except (ApiException, ClientException) as e:
        print(e)


main()
