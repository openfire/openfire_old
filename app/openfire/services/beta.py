# -*- coding: utf-8 -*-

# base imports
import base64, config, webapp2, hashlib
from openfire.services import RemoteService
from apptools.util import debug
from webapp2_extras import security

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

            if any(map(lambda x: x in frozenset([None, False, '']) and True or False, [request.name, request.email])):
                raise BetaService.MissingDataException('One or more required fields were left empty.')
            else:
                if self.api.mail.is_email_valid(request.email):
                    b64_email = base64.b64encode(hashlib.sha256(request.email).hexdigest())
                else:
                    raise self.exceptions.InvalidEmailException("The email you provided isn't valid for some reason!")

                # Generate signup token
                signup_token = security.generate_random_string(32)
                b64_encoded_token = base64.b64encode(hashlib.sha512(signup_token).hexdigest())

                existing = models.Signup.get_by_id(b64_email)
                if existing is None:

                    # Calculate name
                    namesplit = request.name.split(' ')[0]
                    if request.name.split(' ') > 1:
                        firstname, lastname = namesplit[0], namesplit[1]
                    else:
                        firstname, lastname = namesplit[0], None

                    # Generate signup key to avoid 2-step datastore commit
                    signup_key = ndb.Key(models.Signup, b64_email)

                    # Store signup
                    b = models.Signup(**{

                        'key': signup_key,
                        'firstname': firstname,
                        'lastname': lastname,
                        'email': request.email,
                        'token': ndb.Key(models.InviteToken, b64_encoded_token, parent=signup_key),

                    }).put(use_datastore=True, use_cache=True, use_memcache=True)

                    # Store token
                    i = models.InviteToken(**{

                        'key': ndb.Key(models.InviteToken, b64_encoded_token, parent=b),
                        'token': b64_encoded_token,
                        'signup': b,
                        'used': False,
                        'sent': False

                    }).put(use_datastore=True, use_cache=False, use_memcache=False)

                    if isinstance(b, ndb.Key):
                        return messages.BetaSignupResponse(token=b64_encoded_token)
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
