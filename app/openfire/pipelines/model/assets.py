# -*- coding: utf-8 -*-
from openfire.pipelines.model import ModelPipeline


## AssetPipeline - fired when a Asset entity is put/deleted
class AssetPipeline(ModelPipeline):

    ''' Processes asset puts/deletes. '''

    _model_binding = 'openfire.models.assets.Asset'


## MediaPipeline - fired when a Media entity is put/deleted
class MediaPipeline(ModelPipeline):

    ''' Processes media puts/deletes. '''

    _model_binding = 'openfire.models.assets.Media'


## AvatarPipeline - fired when a Avatar entity is put/deleted
class AvatarPipeline(ModelPipeline):

    ''' Processes avatar puts/deletes. '''

    _model_binding = 'openfire.models.assets.Avatar'


## ImagePipeline - fired when a Image entity is put/deleted
class ImagePipeline(ModelPipeline):

    ''' Processes video puts/deletes. '''

    _model_binding = 'openfire.models.assets.Image'


## VideoPipeline - fired when a Video entity is put/deleted
class VideoPipeline(ModelPipeline):

    ''' Processes video puts/deletes. '''

    _model_binding = 'openfire.models.assets.Video'


## CustomURLPipeline - fired when a CustomURL entity is put/deleted
class CustomURLPipeline(ModelPipeline):

    ''' Processes custom URL puts/deletes. '''

    _model_binding = 'openfire.models.assets.CustomURL'
