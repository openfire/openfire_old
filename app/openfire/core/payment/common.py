from openfire.core import construct_enum


OFPaymentFees = {
    'TOTAL_CUT': .0475,             # openfire takes 4.75%
    'WEPAY_PERCENT': .029,          # wepay takes 2.9%
    'WEPAY_ADDITIONAL_CHARGE': .3,  # wepay also takes .30 cents.
}

OFPaymentError = construct_enum(
    'NONE',
    'UNKNOWN',
    'WEPAY_UNKNOWN',
    'WEPAY_OAUTH_URL',
    'WEPAY_NEED_REAUTH',
    'WEPAY_CREATE_ACCOUNT_FOR_USER',
    'NO_WEPAY_ACCOUNT_FOUND',
    'WEPAY_CC_CREATE',
    'WEPAY_CC_AUTHORIZE',
    'WEPAY_CHECKOUT_CREATE',
    'WEPAY_CHECKOUT_CANCEL',
    'WEPAY_WITHDRAWAL_CREATE',
    'OF_FAILED_IMMEDIATE_CHARGE',
    'OF_NO_ACTIVE_PROJECT_GOAL',
    'OF_NO_PROJECT_COLLECTION_ACCOUNT',
)


class CorePaymentResponse(object):

    ''' A small object that can be returned from the any core api with an error. '''

    def __init__(self, success=False, response=None, error_code=OFPaymentError.NONE, error_message=''):

        ''' Create a WePay response. '''

        self.success = success
        self.response = response
        self.error_code = error_code
        self.error_message = error_message
