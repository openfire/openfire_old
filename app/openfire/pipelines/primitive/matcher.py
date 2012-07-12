# -*- coding: utf-8 -*-
import webapp2
from openfire.pipelines import AppPipeline
from google.appengine.api import prospective_search


## MatcherPipeline - parent to all matcher-related pipelines
class MatcherPipeline(AppPipeline):

    ''' Abstract parent class for low-level matcher pipelines. '''

    api = prospective_search


## GetSubscription
class GetSubscription(MatcherPipeline):

    ''' Retrieve information about a registered subscription. '''

    def run(self, document_class_path, sub_id, topic=None):

        ''' Returns a tuple which contains the subscription ID, query, expiration time, and the state of a single subscription. '''

        return self.api.get_subscription(webapp2.import_string(document_class_path), sub_id, topic)


## ListSubscriptions
class ListSubscriptions(MatcherPipeline):

    ''' List subscriptions for a document class. '''

    def run(self, document_class_path, sub_id_start='', topic=None, max_results=1000, expires_before=None):

        ''' Returns a list of tuples. Each tuple contains the subscription ID, query, expiration time, and state of the subscription. '''

        return self.api.list_subscriptions(webapp2.import_string(document_class_path), sub_id_start, topic, max_results, expires_before)


## ListTopics
class ListTopics(MatcherPipeline):

    ''' List available topics. '''

    def run(self, max_results=1000, topic_start=None):

        ''' Returns a list of topics as strings. '''

        return self.api.list_topics(max_results, topic_start)


## Match
class Match(MatcherPipeline):

    ''' Match a document using the prospective search API. '''

    def run(self, document, topic=None,
                  result_key=None, result_relative_url='/_internal/prospective_search',
                  result_task_queue='default', result_batch_size=100, result_return_document=True):

        ''' Matches a document with all subscribed queries on a specific topic and returns the results and db.Model document on the Task Queue. '''

        return self.api.match(document, topic, result_key, result_relative_url, result_task_queue, result_batch_size, result_return_document)


## Subscription
class Subscription(MatcherPipeline):

    ''' Creates a new subscription using the prospective search API. '''

    def run(self, document_class_path, vanilla_query, sub_id, topic=None, lease_duration_sec=0):

        ''' Register subscriptions using a subscription ID and query. If a subscription with the same ID already exists, it is overwritten. '''

        return self.api.subscribe(webapp2.import_string(document_class_path), vanilla_query, sub_id, topic, lease_duration_sec)


## RemoveSubscription
class RemoveSubscription(MatcherPipeline):

    ''' Delete an existing subscription on a topic. '''

    def run(self, document_class_path, sub_id, topic=None):

        ''' Remove a subscription. Once the last subscription for a given topic is removed, the topic also no longer exists. '''

        return self.api.unsubscribe(webapp2.import_string(document_class_path), sub_id, topic)
