from storages.backends.azure_storage import AzureStorage

class MediaStorage(AzureStorage):
    # location = 'media'
    # file_overwrite = True
    expiration_secs = None

# class FileStorage(S3Boto3Storage):
#     location = 'files'
#     file_overwrite = True