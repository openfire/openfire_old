# -*- coding: utf-8 -*-
from openfire.pipelines.intenral import InternalPipeline


## CronPipeline - abstract parent for all cron-based pipelines
class CronPipeline(InternalPipeline):

    ''' Abstract parent for all cron pipelines. '''

    pass


## Tick - datamodel tick handlers (garbage collection/caching)
class Tick(CronPipeline):

    ''' Cron datamodel tick handler. '''

    pass


## Tock - async callback for cron Tick event
class Tock(CronPipeline):

    ''' Cron datamodel tock handler. '''

    async = True
