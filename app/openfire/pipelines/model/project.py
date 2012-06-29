# -*- coding: utf-8 -*-
import logging
from openfire.pipelines.model import ModelPipeline


## CategoryPipeline - fired when a Category entity is put/deleted
class CategoryPipeline(ModelPipeline):

    ''' Processes category puts/deletes. '''

    def put(self, key, category):

        ''' Fired when a category is put. '''

        logging.info('=== FIRED ON PUT ===')
        return

    def delete(self, key):

        ''' Fired when a category is deleted. '''

        logging.info('=== FIRED ON DELETE ===')
        return


## ProjectPipeline - fired when a Project entity is put/deleted
class ProjectPipeline(ModelPipeline):

    ''' Processes project puts/deletes. '''

    def put(self, key, project):

        ''' Fired when a project is put. '''

        logging.info('=== FIRED ON PUT ===')
        return

    def delete(self, key):

        ''' Fired when a project is deleted. '''

        logging.info('=== FIRED ON DELETE ===')
        return


## GoalPipeline - fired when a Goal entity is put/deleted
class GoalPipeline(ModelPipeline):

    ''' Processes goal puts/deletes. '''

    def put(self, key, goal):

        ''' Fired when a goal is put. '''

        logging.info('=== FIRED ON PUT ===')
        return

    def delete(self, key):

        ''' Fired when a goal is deleted. '''

        logging.info('=== FIRED ON DELETE ===')
        return


## TierPipeline - fired when a Tier entity is put/deleted
class TierPipeline(ModelPipeline):

    ''' Processes tier puts/deletes. '''

    def put(self, key, tier):

        ''' Fired when a tier is put. '''

        logging.info('=== FIRED ON PUT ===')
        return

    def delete(self, key):

        ''' Fired when a tier is deleted. '''

        logging.info('=== FIRED ON DELETE ===')
        return
