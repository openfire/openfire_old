# -*- coding: utf-8 -*-
from openfire.pipelines.intenral import InternalPipeline


class CronPipeline(InternalPipeline):

    ''' Abstract parent for all cron pipelines. '''

    pass


class Tick(CronPipeline):

    ''' Cron datamodel tick handler. '''

    pass


class Tock(CronPipeline):

    ''' Cron datamodel tock handler. '''

    async = True
