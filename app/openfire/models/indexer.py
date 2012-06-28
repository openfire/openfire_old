from openfire.models import AppModel
from google.appengine.ext import ndb


class Index(AppModel):

	''' A container for traversible index entries. '''

	pass


class IndexEntry(AppModel):

	''' A value entry in the index. '''

	pass


class IndexMapping(AppModel):

	''' A mapping: entry => key. '''

	pass


class IndexEvent(AppModel):

	''' An event performed by the indexer, like rebuilding/optimizing/creating indexes. '''

	pass


class IndexMutation(AppModel):

	''' A mutation event on the mapping/entry/index, built as part of an index event. '''

	pass
