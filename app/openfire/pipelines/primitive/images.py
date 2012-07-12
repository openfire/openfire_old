# -*- coding: utf-8 -*-
from google.appengine.api import images
from openfire.pipelines import AppPipeline


## ImagePipeline - parent to all image API-related pipelines
class ImagePipeline(AppPipeline):

    ''' Abstract parent class for low-level image API pipelines. '''

    api = images


## CompositeImage
class CompositeImage(ImagePipeline):

    ''' Create a composited image from multiple image inputs. '''

    def run(self):

        ''' Produces a composite image from multiple images, returning the composite image data as a byte string in the requested format. '''

        raise NotImplemented  # @TODO


## CropImage
class CropImage(ImagePipeline):

    ''' Crop an image to a new set of dimensions. '''

    def run(self):

        ''' Crops an image to a given bounding box. The function takes the image data to crop, and returns the transformed image in the same format. '''

        raise NotImplemented  # @TODO


## GetServingURL
class GetServingURL(ImagePipeline):

    ''' Enable an image to be served via the high performance image serving infrastructure. '''

    def run(self):

        ''' Returns a URL that serves the image. Images are served with low latency from a highly optimized, cookieless infrastructure. '''

        raise NotImplemented  # @TODO


## Histogram
class Histogram(ImagePipeline):

    ''' Generate a color histogram for an image. '''

    def run(self):

        ''' Calculates a histogram of the image's color values. '''

        raise NotImplemented  # @TODO


## HorizontalFlip
class HorizontalFlip(ImagePipeline):

    ''' Horizontally flip an image. '''

    def run(self):

        ''' Flips an image horizontally. The edge that was the left becomes the right edge, and vice versa. '''

        raise NotImplemented  # @TODO


## ImFeelingLucky
class ImFeelingLucky(ImagePipeline):

    ''' Perform auto-optimizations on an image. '''

    def run(self):

        ''' Adjusts the contrast and color levels of an image according to an algorithm for improving photographs. '''

        raise NotImplemented  # @TODO


## ResizeImage
class ResizeImage(ImagePipeline):

    ''' Resize an image to a new set of dimensions. '''

    def run(self):

        ''' Resizes an image, scaling down or up to the given width and height. '''

        raise NotImplemented  # @TODO


## RotateImage
class RotateImage(ImagePipeline):

    ''' Rotate an image. '''

    def run(self):

        ''' Rotates an image. The amount of rotation must be a multiple of 90 degrees. '''

        raise NotImplemented  # @TODO


## VerticalFlip
class VerticalFlip(ImagePipeline):

    ''' Vertically flip an image. '''

    def run(self):

        ''' Flips an image vertically. The edge that was the top becomes the bottom edge, and vice versa. '''

        raise NotImplemented  # @TODO
