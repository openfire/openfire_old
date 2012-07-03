# -*- coding: utf-8 -*-
from openfire.pipelines.primitive import StoragePipeline


class CloudStoragePipeline(StoragePipeline):

    ''' Abstract parent class for low-level cloud storage pipelines. '''

    pass


class GenerateUploadURL(CloudStoragePipeline):

    ''' Generate an upload URL suitable for use with Google Cloud Storage. '''

    pass


class GenerateServeURL(CloudStoragePipeline):

    ''' Given a blob key, yield a URL to serve the stored item. '''

    pass


class GenerateDownloadURL(CloudStoragePipeline):

    ''' Given a blob key, yield a URL to download the stored item. '''

    pass


class CloudStorageFile(CloudStoragePipeline):

    ''' Write given data to cloud storage as a file. '''

    pass


class CloudStorageImage(CloudStorageFile):

    ''' Write given image data to cloud storage as a file. '''

    pass
