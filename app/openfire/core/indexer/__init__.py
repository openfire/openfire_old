# -*- coding: utf-8 -*-
from openfire.core import CoreAPI


class CoreIndexerAPI(CoreAPI):

    ''' The Core Indexer API manages search index construction and management. '''

    def substring_list(self, string, min_len=1):

        ''' Find all substrings of the given string between (and including) min and max length. '''

        subs = set()
        str_len = len(string)
        if str_len < 1 or min_len > str_len:
            return subs

        i = min_len
        for i in range(min_len, str_len + 1):
            for j in range(str_len - i + 1):
                subs.add(string[j:j+i])
        return subs

IndexerAPI = CoreIndexerAPI()
