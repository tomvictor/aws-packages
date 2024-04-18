from typing import List

from pydantic import BaseModel


class SolanaAuthenticationRequest(BaseModel):
    """Authentication request model"""

    public_key: str
    signature: List[int]
    message: str

    def get_signature_list(self):
        # TODO: mohit fix to bytes
        return bytes(self.signature["data"])
