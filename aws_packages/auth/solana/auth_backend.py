"""Authentication backends.

"""

from nacl.exceptions import BadSignatureError
from solathon.utils import verify_signature

from aws_packages.auth.auth_backend_abc import AuthBackendBase
from aws_packages.auth.models import User
from aws_packages.auth.tokens import AccessToken

from .models import SolanaAuthenticationRequest


class SolanaAuthBackend(AuthBackendBase):
    """Authentication backend with Solana Canister"""

    def __init__(self, url: str):
        self._url = url

    def authenticate(self, login_request_body: SolanaAuthenticationRequest) -> str:
        """Authenticate the request and returns an authenticated User"""

        # solana sdk call and authenticate or raise exception
        # TEMPFIX
        # if login_request_body.authcode != "1234":
        #     raise Exception("Invalid authcode")

        try:
            verify_signature(
                login_request_body.public_key,
                # login_request_body.get_signature_list()
                login_request_body.signature,
                login_request_body.message,
            )
            print("working")
        except BadSignatureError:
            print("unauthorized")

        return True

    def authenticate_with_token(self, token: str):
        """Authenticate user using jwt token and return status"""
        print("token : ", token)
        token = AccessToken(token_string=token)
        return token

    def get_access_token(self, user: User) -> str:
        """Get the access for the given user"""
        token = AccessToken()
        return token.get_access_token(user)

    def get_refresh_token(self, user: User, token: str) -> str:
        """Get the refresh token for the given user"""
        raise NotImplementedError("get_refresh_token is not implemented")


# check and remove the url
solana_auth_backend = SolanaAuthBackend(
    url="https://ic0.app",
)

if __name__ == "__main__":
    _auth_backend = SolanaAuthBackend(
        url="https://ic0.app",
    )

    request = SolanaAuthenticationRequest(
        user="4cay5-ew3bs-vr6yl-7iffu-67doc-l655v-dluy7-qplpx-7pkio-er5rt-uqe",
        authcode="",
    )
    user = solana_auth_backend.authenticate(request)
    print(user)
