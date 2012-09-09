# -*- coding: utf-8 -*-

# base imports
import base64, config, webapp2
from apptools.util import debug
from openfire.services import RemoteService

# protorpc imports
from protorpc import remote, message_types

# sdk imports
from google.appengine.ext import ndb

# models/messages
from openfire.models import beta as models
from openfire.messages import beta as messages


## BetaService - powers the placeholder landing page, accepts private beta signups
class BetaService(RemoteService):

    ''' Handles remote methods related to beta signup/invite management/etc. '''

    ## Exceptions
    class BetaServiceException(RemoteService.exceptions.ApplicationError): ''' Abstract - thrown when an exception occurs in `BetaService`. '''
    class BetaSignupException(BetaServiceException): ''' Abstract - thown when an exception occurs in `BaseService.signup`. '''
    class AlreadySubmittedException(BetaSignupException): ''' Concrete - thrown when a submission already exists in the datastore. '''
    class MissingDataException(BetaSignupException): ''' Concrete - thrown when a property such as `name` or `email` is missing from a submission. '''
    class InvalidEmailException(BetaSignupException): ''' Concrete - thrown when a given signup email address fails validation. '''
    class StorageFailureException(BetaSignupException): ''' Concrete - thrown when the signup service fails to store the signup for an unknown reason. '''

    exceptions = RemoteService.exceptions.extend({

        'BetaServiceException': BetaServiceException,
        'BetaSignupException': BetaSignupException,
        'AlreadySubmittedException': AlreadySubmittedException,
        'MissingDataException': MissingDataException,
        'InvalidEmailException': InvalidEmailException,
        'StorageFailureException': StorageFailureException

    })

    @webapp2.cached_property
    def config(self):

        ''' Named config pipe. '''

        return config.config.get('openfire.services.BetaService', {})

    @webapp2.cached_property
    def log(self):

        ''' Named logging pipe. '''

        return debug.AppToolsLogger(path='openfire.services', name='BetaService')._setcondition(self.config.get('debug', False))

    @remote.method(messages.BetaSignup, messages.BetaSignupResponse)
    def signup(self, request):

        ''' Process a request for a user signup. '''

        try:

            if any(map(lambda x: x in frozenset([None, False, '']) and True or False, [request.name, request.email, request.token])):
                raise BetaService.MissingDataException('One or more required fields were left empty.')
            else:
                b64_email = base64.b64encode(request.email)
                existing = models.Signup.get_by_id(b64_email)
                if existing is None:

                    # Calculate name
                    namesplit = request.name.split(' ')[0]
                    if request.name.split(' ') > 1:
                        firstname, lastname = namesplit[0], namesplit[1]
                    else:
                        firstname, lastname = namesplit[0], None

                    # Store signup
                    b = models.Signup(**{

                        'key': ndb.Key(models.Signup, b64_email),
                        'firstname': firstname,
                        'lastname': lastname,
                        'email': request.email,
                        'token': request.token,
                        'message': request.message

                    }).put(use_datastore=True, use_cache=True, use_memcache=True)

                    if isinstance(b, ndb.Key):
                        return messages.BetaSignupResponse(key=b.urlsafe(), token=request.token)
                    else:
                        raise BetaService.StorageFailureException("Woops, something went wrong storing your signup! Please try again.")
                else:
                    raise BetaService.AlreadySubmittedException("You have already submitted your signup!")

        # Catch all BetaService exceptions to re-raise
        except BetaService.BetaServiceException, e:
            raise

        # Catch all other unhandled exceptions with a generic message
        except Exception, e:
            if not config.debug:
                raise BetaService.BetaServiceException("Woops, something went wrong! Please try again.")
            else:
                raise
