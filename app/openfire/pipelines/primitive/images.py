# -*- coding: utf-8 -*-
from openfire.pipelines import AppPipeline


## ImagePipeline - parent to all image API-related pipelines
class ImagePipeline(AppPipeline):

    ''' Abstract parent class for low-level image API pipelines. '''

    pass


## CompositeImage
class CompositeImage(ImagePipeline):

    ''' Create a composited image from multiple image inputs. '''

    pass


## CropImage
class CropImage(ImagePipeline):

    ''' Crop an image to a new set of dimensions. '''

    pass


## GetServingURL
class GetServingURL(ImagePipeline):

    ''' Enable an image to be served via the high performance image serving infrastructure. '''

    pass


## Histogram
class Histogram(ImagePipeline):

    ''' Generate a color histogram for an image. '''

    pass


## HorizontalFlip
class HorizontalFlip(ImagePipeline):

    ''' Horizontally flip an image. '''

    pass


## ImFeelingLucky
class ImFeelingLucky(ImagePipeline):

    ''' Perform auto-optimizations on an image. '''

    pass


## ResizeImage
class ResizeImage(ImagePipeline):

    ''' Resize an image to a new set of dimensions. '''

    pass


## RotateImage
class RotateImage(ImagePipeline):

    ''' Rotate an image. '''

    pass


## VerticalFlip
class VerticalFlip(ImagePipeline):

    ''' Vertically flip an image. '''

    pass
