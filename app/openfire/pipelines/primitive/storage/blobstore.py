# -*- coding: utf-8 -*-
from openfire.pipelines.primitive import StoragePipeline


## BlobstorePipeline - abstract parent for all blobstore-related pipelines
class BlobstorePipeline(StoragePipeline):

    ''' Abstract parent class for low-level blobstore pipelines. '''

    pass


## GenerateUploadURL - generate and yield an upload URL for the blobstore
class GenerateUploadURL(BlobstorePipeline):

    ''' Generate an upload URL suitable for use with the blobstore. '''

    pass


## GenerateDownloadURL - generate and yield a URL to download the given blob
class GenerateDownloadURL(BlobstorePipeline):

    ''' Given a blob key, yield a URL to download the blob. '''

    pass


## GenerateServeURL - generate and yield a URL to serve the given blob
class GenerateServeURL(BlobstorePipeline):

    ''' Given a blob key, yield a URL to serve the blob. '''

    pass


## BlobstoreFile - parent for all blobstore file-yielding pipelines
class BlobstoreFile(BlobstorePipeline):

    ''' Write given data to the blobstore as a file. '''

    pass


## BlobstoreImage - given image data, yield an image file in the blobstore
class BlobstoreImage(BlobstoreFile):

    ''' Write given image data to the blobstore as a file. '''

    pass
