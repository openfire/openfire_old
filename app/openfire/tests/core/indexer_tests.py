## openfire indexer tests


from openfire.tests import OFTestCase
import openfire.fixtures.fixture_util as db_loader

from openfire.core.indexer import IndexerAPI


class CoreIndexerAPITestCase(OFTestCase):
    """ Test cases for indexer core API.
    """

    def test_substring_list(self):

        ''' Test the substring_list method of the indexer core api. '''

        correct_subs = set(['1234', '2345', '123', '12', '23', '45', '34', '1', '345', '3', '2', '5', '4', '234', '12345'])
        correct_subs_2 = set(['1234', '2345', '123', '12', '23', '45', '34', '345', '234', '12345'])
        correct_subs_3 = set(['1234', '2345', '123', '345', '234', '12345'])
        correct_subs_4 = set(['1234', '2345', '12345'])
        correct_subs_5 = set(['12345'])
        correct_subs_6 = set([])

        self.assertEqual(IndexerAPI.substring_list('12345'), correct_subs,
            'Returned wrong set of substrings for "12345" with no minimum length.')
        self.assertEqual(IndexerAPI.substring_list('12345', min_len=2), correct_subs_2,
            'Returned wrong set of substrings for "12345" with 2 minimum length.')
        self.assertEqual(IndexerAPI.substring_list('12345', min_len=3), correct_subs_3,
            'Returned wrong set of substrings for "12345" with 3 minimum length.')
        self.assertEqual(IndexerAPI.substring_list('12345', min_len=4), correct_subs_4,
            'Returned wrong set of substrings for "12345" with 4 minimum length.')
        self.assertEqual(IndexerAPI.substring_list('12345', min_len=5), correct_subs_5,
            'Returned wrong set of substrings for "12345" with 5 minimum length.')
        self.assertEqual(IndexerAPI.substring_list('12345', min_len=6), correct_subs_6,
            'Returned wrong set of substrings for "12345" with 6 minimum length.')
