Title: Versioned Static Assets in Django with Docker
Date: 2024-12-31 16:34
Category: django
Tags: django,python,webdev
Slug: django-versioned-static-assets
Authors: me
Summary: A robust strategy to manage static assets with Docker-based Django projects
PreviewImage: images/blog/frontend.jpg

# Introduction

When deploying Django applications with Docker, managing static files efficiently and safely is a common challenge. The need to use the `collectstatic` command—[which aggregates and processes all static files](https://docs.djangoproject.com/en/5.1/ref/contrib/staticfiles/#collectstatic) —complicates deployments, especially in multi-environment setups like staging and production. This article explores various approaches to handling static files and introduces a versioning strategy for more reliable deployments.

# The Problem with Static Files in Django Deployments

The `collectstatic` command is essential in Django to gather static files from various apps and prepare them for serving via a CDN from a storage service like AWS S3 or Azure Blob Storage. However, this step introduces deployment complexities:

## Option 1: Run `collectstatic` During Deployment

One approach is to avoid running `collectstatic` during the Docker build process and instead execute it during deployment for each environment (e.g., staging or production).

Problems:

* **Error Detection Delay**: Issues with static files are only discovered at deployment time, making debugging more challenging.
* **Discrepancies Between Environments**: `collectstatic` often performs additional optimizations like file compression (e.g., via `django-compressor`). Running it multiple times for different environments increases the risk of inconsistencies.
* **Rollback Challenges**: Rolling back a deployment requires re-running `collectstatic` for the previous version. This can be time-consuming, taking several minutes or even tens of minutes, and complicates rapid recovery.

## Option 2: Run `collectstatic` During Docker Build

Another approach is to execute `collectstatic` as part of the Docker build process.

Challenges:

* **Risk of Overwriting Files**: If the new static files are pushed to the same storage location used by the production environment, there is a risk of overwriting or corrupting existing files.
* **Increased Build Time**: Running `collectstatic` during the build process increases the time required to build the Docker image.

# A Versioned Approach to Static Assets

A more robust solution is to incorporate a versioning strategy during the Docker build process. By using a `RELEASE_VERSION` build argument—following semantic versioning—we can organize static files by version in the storage account. Here’s how it works:

1. **Set a Version Identifier**: During the Docker build, pass a `RELEASE_VERSION` argument to identify the application version (e.g., `v1.2.3`).
2. **Organize Static Files by Version**: Modify the `collectstatic` process to store files in a folder named after the version (e.g., `static/v1.2.3/`).
3. **Ensure Environment Independence**: Use a single storage account for all environments. Static files are an integral part of the application and should not depend on a specific environment. Since static files are versioned, there is no risk of interference between environments..

This strategy provides several benefits:

* **Easy Rollbacks**: To roll back, simply configure the application to use the static files from the previous version. No re-running of `collectstatic` is required.
* **Environment Consistency**: All environments use the same set of static files for a given version, eliminating discrepancies.
* **Preservation of Static Files**: Files from different versions are stored separately, avoiding overwrites and corruption. This approach also facilitates concurrent deployments and aligns well with blue-green deployment strategies, as each version's static files remain isolated and accessible without interference. When deploying a new version in a cluster, containers are typically updated incrementally rather than all at once. With this method, each running version maintains access to its specific static files until all containers are successfully updated to the latest version.

## Implementation Example with `django-storages`

`django-storages` is a typical package that simplifies using remote storage accounts in a Django application (see documentation at [https://django-storages.readthedocs.io](https://django-storages.readthedocs.io)).

Implementing the approach described in the previous section requires to modify the default behaviour of django-storages. Below is an implementation of the versioned approach using Azure Blob Storage. A similar approach can be used with AWS S3 or other storage services.

We first need to define a custom storage class to prefix each static filepath with the current app version, as shown below:

```python
# config/storages.py
import os

from django.conf import settings

from storages.backends.azure_storage import AzureStorage


class StaticAzureStorage(AzureStorage):
    """Define separate azure storage
    container for public files.
    """
    account_name = settings.AZURE_ACCOUNT_NAME_STATIC
    account_key = settings.AZURE_ACCOUNT_KEY_STATIC
    azure_container = settings.AZURE_CONTAINER_STATIC
    expiration_secs = None

    def _get_valid_path(self, name: str) -> str:
        """Concatenate the app version to the filename to make
        sure all files are stored within a versioned folder

        Args:
            name (str): filename

        Returns:
            str: filepath that includes the app version
        """
        version = settings.RELEASE_VERSION
        name = os.path.join(version, name)
        return super()._get_valid_path(name)

```

We can then configure the Django settings to use this custom storage class:

```python
# config/settings/base.py

# -------------------------------
# Azure Storage Configuration
# ---------------------------------

# Azure blob storage for static files
AZURE_ACCOUNT_KEY_STATIC = env.str("AZURE_STORAGE_ACCOUNT_KEY_STATIC", default=None)
AZURE_ACCOUNT_NAME_STATIC = env.str("AZURE_STORAGE_ACCOUNT_NAME_STATIC", default=None)
AZURE_CONTAINER_STATIC = env.str(
    "AZURE_STORAGE_CONTAINER_STATIC", default="lean-api-static"
)

AZURE_STORAGE_FOR_STATIC_ENABLED = AZURE_ACCOUNT_NAME_STATIC and AZURE_CONTAINER_STATIC
AZURE_CUSTOM_DOMAIN_STATIC = (
    f"{AZURE_ACCOUNT_NAME_STATIC}.blob.core.windows.net"
    if AZURE_ACCOUNT_NAME_STATIC
    else None
)

# ---------------------------------------------------------------------------
# Default storage options
# ---------------------------------------------------------------------------
STORAGES = {
    # See defaults in, https://docs.djangoproject.com/en/4.2/ref/settings/#storages
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# ---------------------------------------------------------------------------
# STATIC files
# ---------------------------------------------------------------------------

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_HOST = env("DJANGO_STATIC_HOST", default="")
STATIC_URL = STATIC_HOST + "/static/"

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# https://docs.djangoproject.com/en/4.0/ref/settings/#prefixes-optional
STATICFILES_DIRS = [
    # Specify static files in <root>/templates/static directory to be collected by collectstatic command
    ("templates", "templates/static"),
]

if AZURE_CUSTOM_DOMAIN_STATIC:
    # Azure Blob Storage
    # ---------------------------------------------------------------------------
    STORAGES["staticfiles"]["BACKEND"] = "config.storages.StaticAzureStorage"

    if STATIC_HOST:
        STATIC_URL = f"https://{STATIC_HOST}/{AZURE_CONTAINER_STATIC}/"
    else:
        # if a CDN host is not provided, then we set the static url to the
        # Blob storage container url
        STATIC_URL = f"https://{AZURE_CUSTOM_DOMAIN_STATIC}/{AZURE_CONTAINER_STATIC}/"
```

The last step is to modify our Dockerfile to run `collecstatic` command during build:

```docker
# Dockerfile
# ...

# define the build arguments
ARG AZURE_STORAGE_ACCOUNT_NAME_STATIC="" \
    AZURE_STORAGE_CONTAINER_STATIC="" \
    RELEASE_VERSION

# save build-arguments as environment variables in the image
ENV DJANGO_SETTINGS_MODULE=config.settings.production \
    AZURE_STORAGE_ACCOUNT_NAME_STATIC=$AZURE_STORAGE_ACCOUNT_NAME_STATIC \
    AZURE_STORAGE_CONTAINER_STATIC=$AZURE_STORAGE_CONTAINER_STATIC \
    RELEASE_VERSION=$RELEASE_VERSION

# Collect static files
# if it is a production build, use the azure storage key passed as a
# build secret to store all the static files in the azure storage account.
# To use this, run docker build --secret id=azure_storage_account_key_static,env=AZURE_STORAGE_ACCOUNT_KEY_STATIC ....
RUN --mount=type=secret,id=azure_storage_account_key_static,required AZURE_STORAGE_ACCOUNT_KEY_STATIC=$(cat /run/secrets/azure_storage_account_key_static) \
    python manage.py collectstatic --no-input


```
Sending static files to the storage account in Azure requires the name of the container, the name of the storage account and an account key. This last parameter is a secret and shouldn't be saved as an environment variable in the image. To prevent this, it is passed as a [build secret](https://docs.docker.com/build/building/secrets/). A build secret is temporarily mount inside the build container, for the duration of the build instruction.

#### Docker build command

When building the docker image, we now need to provide the release version, storage account name and container name as build argument, and the storage account key as a build secret:

```bash

VERSION=v1.2.3

# build the image
docker build -t your-app:$(RELEASE_VERSION) \
  -f Dockerfile \
  --build-arg RELEASE_VERSION=$(RELEASE_VERSION) \
  --build-arg AZURE_STORAGE_ACCOUNT_NAME_STATIC=<name of the storage account> \
  --build-arg AZURE_STORAGE_CONTAINER_STATIC=<name of the container> \
  --secret id=azure_storage_account_key_static,env=<private key> \
   .

# push the image to the registry
docker push your-app:$VERSION

```

## Key Considerations

* **Storage Costs**: Versioning static files increases storage usage. Without the approach described here, it's very hard to free space as the static files accumulate in the same folder. With this approach, it's easy to delete the folder matching old versions of the application that we don't intend to use in production anymore.
* **Environment Setup**: Since the Docker image contains the reference to the storage account as an environment variable, the Docker image can be deployed anywhere easily, ensuring all environments fetch static files from the correct version folder.

# Conclusion

By adopting a versioning strategy for static assets, you can address key challenges in Django deployments effectively. This approach ensures seamless rollbacks, maintains environment consistency, and avoids file overwrites or corruption. Additionally, because the Docker image includes environment-independent references to the storage account, deployment is streamlined across environments. While this strategy requires some upfront configuration and storage management, its reliability and scalability make it a worthwhile investment for production-grade applications.
