# -*- coding: utf-8 -*-
from openfire.pipelines.primitive import StoragePipeline


class BlobstorePipeline(StoragePipeline):

    ''' Abstract parent class for low-level blobstore pipelines. '''

    pass


class GenerateUploadURL(BlobstorePipeline):

    ''' Generate an upload URL suitable for use with the blobstore. '''

    pass


class GenerateDownloadURL(BlobstorePipeline):

    ''' Given a blob key, yield a URL to download the blob. '''

    pass


class BlobstoreFile(BlobstorePipeline):

    ''' Write given data to the blobstore as a file. '''

    pass


class BlobstoreImage(BlobstoreFile):

    ''' Write given image data to the blobstore as a file. '''

    pass


class GenerateServeURL(BlobstorePipeline):

    ''' Given a blob key, yield a URL to serve the blob. '''

    pass
