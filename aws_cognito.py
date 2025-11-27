# This class is responsible for communicating with AWS Cognito, however I chose to utilize the OAuth method to
# communicate with Cognito for simplicity end efficiency.
import boto3
import hmac
import hashlib
import base64
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class CognitoService:
    def __init__(self, user_pool_id, client_id, client_secret):
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.cognito_idp_client = boto3.client("cognito-idp", region_name="eu-north-1")

    def _secret_hash(self, username):
        message = username + self.client_id
        digest = hmac.new(
            self.client_secret.encode("utf-8"),
            msg=message.encode("utf-8"),
            digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(digest).decode()

    def sign_up_user(self, user_name, password, user_email, first_name, last_name):
        try:
            kwargs = {
                "ClientId": self.client_id,
                "Username": user_name,
                "Password": password,
                "UserAttributes": [{"Name": "email", "Value": user_email},
                                   {"Name": "given_name", "Value": first_name},
                                   {"Name": "family_name", "Value": last_name}],
            }
            if self.client_secret:
                kwargs["SecretHash"] = self._secret_hash(user_name)
            response = self.cognito_idp_client.sign_up(**kwargs)
            confirmed = response["UserConfirmed"]
        except ClientError as err:
            if err.response["Error"]["Code"] == "UsernameExistsException":
                resp = self.cognito_idp_client.admin_get_user(
                    UserPoolId=self.user_pool_id,
                    Username=user_name
                )
                confirmed = resp["UserStatus"] == "CONFIRMED"
            else:
                raise
        return confirmed

    def confirm_user_sign_up(self, user_name, confirmation_code):
        try:
            kwargs = {
                "ClientId": self.client_id,
                "Username": user_name,
                "ConfirmationCode": confirmation_code,
            }

            if self.client_secret:
                kwargs["SecretHash"] = self._secret_hash(user_name)

            self.cognito_idp_client.confirm_sign_up(**kwargs)
        except ClientError as err:
            raise
        return True
