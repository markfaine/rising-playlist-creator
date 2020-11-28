import os
import pickle
import logging
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from google.auth.transport.requests import Request
from pyfields import field
from autoclass import autoclass

__author__ = "Mark Faine"
__email__ = "mark.faine@gmail.com"
__maintainer__ = "Mark Faine"

logger = logging.getLogger(__name__)

@autoclass()
class GoogleService:
    client_secret_file: str = field(check_type=True, doc="The secrets file")
    scopes: list = field(check_type=True, doc="The API version")
    api_name: str = field(check_type=True, default="youtube", doc="The API name")
    api_version: str = field(check_type=True, default="3", doc="The API version")


    def authenticate(self) :
        cred = None
        logger.debug(f"Secret File: {self.client_secret_file}")
        logger.debug(f"API Name: {self.api_name}")
        logger.debug(f"API Version: {self.api_version}")
        logger.debug(f"Scopes: {','.join(self.scopes)}")

    # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        pickle_file = f'token_{self.api_name}_{self.api_version}.pickle'
        logger.debug(f"Pickle File: {pickle_file}")

        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                # Get credentials and create an API client
                flow = InstalledAppFlow.from_client_secrets_file(self.client_secret_file, self.scopes)
                cred = flow.run_local_server()
                with open(pickle_file, 'wb') as token:
                    pickle.dump(cred, token)
        try:
            service = googleapiclient.discovery.build(self.api_name, self.api_version, credentials=cred)
            logger.debug(f"{self.api_name} service created successfully")
            return service
        except ImportError:
            pass
        except ModuleNotFoundError:
            pass
        except Exception as e:
            print(e)
            logger.debug(f'Failed to create service instance for {self.api_name}')
            os.remove(pickle_file)
            return None
