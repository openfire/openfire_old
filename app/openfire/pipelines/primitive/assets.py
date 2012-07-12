# -*- coding: utf-8 -*-
from openfire.pipelines import AppPipeline


## AssetPipeline - parent to all asset-related pipelines
class AssetPipeline(AppPipeline):

    ''' Abstract parent class for low-level asset pipelines. '''

    pass


## NewAsset - create a new asset
class NewAsset(AssetPipeline):

    ''' Create a new Asset record. '''

    def run(self):

        pass


## UpdateAsset - update an asset record
class UpdateAsset(AssetPipeline):

    ''' Update an Asset record. '''

    def run(self):

        pass


## NewAvatar - create a new avatar record
class NewAvatar(AssetPipeline):

    ''' Create a new Avatar record. '''

    def run(self):

        pass


## UpdateAvatar - update an avatar record
class UpdateAvatar(AssetPipeline):

    ''' Update an Avatar record. '''

    def run(self):

        pass


## SetAvatar - set an avatar for a project or user
class SetAvatar(AssetPipeline):

    ''' Set the avatar for a user or project. '''

    def run(self):

        pass
