## openfire user account controllers

class UserAccountController extends OpenfireController

    constructor: (openfire, window) ->

        @_init = () =>
            linkWePayBtn = document.getElementById('link-wepay-account-btn')
            if linkWePayBtn
                linkWePayBtn.addEventListener('click', @linkWePayAccount, false)

        @linkWePayAccount = () =>
            $.apptools.api.payment.get_auth_url().fulfill
                success: (response) =>
                    $("#link-wepay-account-inline").show()
                    $("#link-wepay-account-link").html(response.url)
                    $("#link-wepay-account-link").attr('href', response.url)

                failure: (error) =>
                    @log "Failed to get auth url to link WePay account: " + error


if @__openfire_preinit?
    @__openfire_preinit.abstract_base_controllers.push(UserAccountController)
