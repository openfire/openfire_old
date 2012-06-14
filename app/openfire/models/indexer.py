from google.appengine.ext import ndb


class Index(ndb.Model):

	''' A container for traversible index entries. '''

	pass


class IndexEntry(ndb.Model):

	''' A value entry in the index. '''

	pass


class IndexMapping(ndb.Model):

	''' A mapping: entry => key. '''

	pass


class IndexEvent(ndb.Model):

	''' An event performed by the indexer, like rebuilding/optimizing/creating indexes. '''

	pass


class IndexMutation(ndb.Model):

	''' A mutation event on the mapping/entry/index, built as part of an index event. '''

	pass
