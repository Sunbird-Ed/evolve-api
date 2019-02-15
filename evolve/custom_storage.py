from storages.backends.azure_storage import AzureStorage
from evolve import settings
class MediaStorage(AzureStorage):
    # location = 'media'
    # file_overwrite = True
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = settings.AZURE_CONTAINER
    expiration_secs = None

# class FileStorage(S3Boto3Storage):
#     location = 'files'
#     file_overwrite = True