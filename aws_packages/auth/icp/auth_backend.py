"""Authentication backends.

"""

import os

from ic.agent import Agent
from ic.candid import Types, encode
from ic.client import Client
from ic.identity import Identity

from aws_packages.auth.auth_backend_abc import AuthBackendBase
from aws_packages.auth.models import AuthenticationRequest, User
from aws_packages.auth.tokens import AccessToken


class ICPAuthBackend(AuthBackendBase):
    """Authentication backend with ICP Canister"""

    def __init__(self, url: str, auth_canister: str, auth_function: str):
        self._url = url
        self._identity = Identity()
        self._client = Client(url=self._url)
        self._icp_agent = Agent(self._identity, self._client)
        self._auth_canister = auth_canister
        self._canister_auth_func = auth_function

    def authenticate(self, login_request: AuthenticationRequest) -> User:
        """Authenticate the request and returns an authenticated User"""
        encoded_args = encode(
            [
                {
                    "type": Types.Principal,
                    "value": login_request.user,
                }
            ]
        )

        self._icp_agent.update_raw(
            self._auth_canister, self._canister_auth_func, encoded_args
        )

        return User(principal=login_request.user)

    def authenticate_with_token(self, token: str):
        """Authenticate user using jwt token and return status"""
        print("token : ", token)
        AccessToken(token_string=token)

    def get_access_token(self, user: User) -> str:
        """Get the access for the given user"""
        token = AccessToken()
        return token.get_access_token(user)

    def get_refresh_token(self, user: User, token: str) -> str:
        """Get the refresh token for the given user"""
        raise NotImplementedError("get_refresh_token is not implemented")


icp_auth_backend = ICPAuthBackend(
    url="https://ic0.app",
    auth_canister=os.environ.get("CANISTER_ID"),
    auth_function="getUserToken",
)


if __name__ == "__main__":
    icp_auth_backend = ICPAuthBackend(
        url="https://ic0.app",
        auth_canister="6qy4q-5aaaa-aaaah-adwma-cai",
        auth_function="getUserToken",
    )

    request = AuthenticationRequest(
        user="4cay5-ew3bs-vr6yl-7iffu-67doc-l655v-dluy7-qplpx-7pkio-er5rt-uqe",
        authcode="",
    )
    user = icp_auth_backend.authenticate(request)
    print(user)
