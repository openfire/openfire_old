#!/usr/bin/python
#
#   Basic test runner.
#   Inspired by:
#       https://developers.google.com/appengine/docs/python/tools/localunittesting
#

import optparse
import os
import sys
import unittest2

USAGE = """
%prog GAE_PATH APP_DIR
Run unit tests for apptools apps.

GAE_PATH    Path to the Google App Engine SDK installation
APP_DIR     Path to your 'app' directory"""


PATTERN = 'login_test*'


def main(gae_path, app_path):
    os.environ["SERVER_SOFTWARE"] = "Development"
    sys.path.insert(0, gae_path)
    import dev_appserver
    dev_appserver.fix_sys_path()
    if os.name == 'nt':
        sys.path.insert(0, ".\\lib\\dist\\")
        sys.path.insert(0, ".\\lib")
    else:
        sys.path.insert(0, "./lib/dist/")
        sys.path.insert(0, "./lib/")
    suite = unittest2.loader.TestLoader().discover(app_path, pattern=PATTERN)
    unittest2.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) != 2:
        parser.print_help()
        APP_DIR = "."
        if os.name == 'nt':
            GAE_PATH = "..\\var\\parts\\google_appengine"
        else:
            GAE_PATH = "/usr/local/google_appengine/"
        print "GAE and APP paths not specified. Using default:"
        print "GAE_PATH: %s  APP_DIR: %s" % (GAE_PATH, APP_DIR)
    else:
        GAE_PATH = args[0]
        APP_DIR = args[1]
    main(GAE_PATH, APP_DIR)
