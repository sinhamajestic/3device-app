import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .config import settings
import requests
from cachetools import TTLCache

# Cache for JWKS to avoid fetching it on every request
jwks_cache = TTLCache(maxsize=1, ttl=600)

class VerifyToken:
    def __init__(self):
        self.config = {
            "domain": settings.AUTH0_DOMAIN,
            "api_audience": settings.AUTH0_API_AUDIENCE,
            "algorithms": ["RS256"],
        }
        self.auth_bearer = HTTPBearer()

    def verify(self, token: str):
        jwks_url = f'https://{self.config["domain"]}/.well-known/jwks.json'
        
        if "jwks" not in jwks_cache:
            jwks = requests.get(jwks_url).json()
            jwks_cache["jwks"] = jwks
        else:
            jwks = jwks_cache["jwks"]
        
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.PyJWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token header: {e}")

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if not rsa_key:
            raise HTTPException(status_code=401, detail="Unable to find appropriate key")

        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=self.config["algorithms"],
                audience=self.config["api_audience"],
                issuer=f'https://{self.config["domain"]}/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token is expired")
        except jwt.JWTClaimsError:
            raise HTTPException(status_code=401, detail="Incorrect claims, please check the audience and issuer")
        except Exception:
            raise HTTPException(status_code=401, detail="Unable to parse authentication token.")

    async def __call__(self, creds: HTTPAuthorizationCredentials = Security(HTTPBearer())):
        return self.verify(creds.credentials)


verify_token = VerifyToken()

