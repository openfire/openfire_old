# -*- coding: utf-8 -*-
from openfire.pipelines.primitive import StoragePipeline


## CloudStoragePipeline - abstract parent for all cloud storage-related pipelines
class CloudStoragePipeline(StoragePipeline):

    ''' Abstract parent class for low-level cloud storage pipelines. '''

    pass


## GenerateUploadURL - generate and yield  a URL suitable for uploading to cloud storage
class GenerateUploadURL(CloudStoragePipeline):

    ''' Generate an upload URL suitable for use with Google Cloud Storage. '''

    pass


## GenerateServeURL - generate and yield a URL suitable for serving an item from cloud storage
class GenerateServeURL(CloudStoragePipeline):

    ''' Given a blob key, yield a URL to serve the stored item. '''

    pass


## GenerateDownloadURL - generate and yield a URL suitable for downloading an item from cloud storage
class GenerateDownloadURL(CloudStoragePipeline):

    ''' Given a blob key, yield a URL to download the stored item. '''

    pass


## CloudStorageFile - parent for all cloud storage file-yielding pipelines
class CloudStorageFile(CloudStoragePipeline):

    ''' Write given data to cloud storage as a file. '''

    pass


## CloudStorageImage - given image data, yield a cloud storage-based file
class CloudStorageImage(CloudStorageFile):

    ''' Write given image data to cloud storage as a file. '''

    pass
