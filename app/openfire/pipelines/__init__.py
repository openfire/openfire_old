# -*- coding: utf-8 -*-

## Project Pipelines Init
from pipeline import pipeline

## Core API mixins
from apptools.api.assets import AssetsMixin
from apptools.api.output import OutputMixin


class AppPipeline(pipeline.Pipeline, AssetsMixin, OutputMixin):

    ''' Abstract pipeline for all openfire pipelines. '''

    def finalized(self):
        return
