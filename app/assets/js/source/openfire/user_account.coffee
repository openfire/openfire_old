## openfire user account controllers

class UserAccountController extends OpenfireController

    constructor: (openfire, window) ->

        @_init = () =>
            linkWePayBtn = document.getElementById('link-wepay-account-btn')
            if linkWePayBtn
                linkWePayBtn.addEventListener('click', @linkWePayAccount, false)

            createAccountBtns = document.getElementsByClassName('create-account-for-project')
            for btn in createAccountBtns
                btn.addEventListener('click', @createAccoutForProject, false)

            removeMoneySourceBtns = document.getElementsByClassName('remove-money-source')
            for btn in removeMoneySourceBtns
                btn.addEventListener('click', @removeMoneySource, false)

            cancelPaymentBtns = document.getElementsByClassName('cancel-payment')
            for btn in cancelPaymentBtns
                btn.addEventListener('click', @cancelPayment, false)

        @linkWePayAccount = () =>
            $.apptools.api.payment.get_auth_url().fulfill
                success: (response) =>
                    $("#link-wepay-account-inline").show()
                    $("#link-wepay-account-link").html(response.url)
                    $("#link-wepay-account-link").attr('href', response.url)

                failure: (error) =>
                    @log "Failed to get auth url to link WePay account: " + error

        @createAccoutForProject = () ->
            $.apptools.api.payment.create_project_payment_account(
                "project": this.id
            ).fulfill
                success: (response) =>
                    alert("Success! Reloading page...")
                    window.location.reload()
                failure: (error) =>
                    alert("failure!")

        @removeMoneySource = () ->
            $.apptools.api.payment.remove_money_source(
                "source": this.id
            ).fulfill
                success: (response) =>
                    alert("Success! Reloading page...")
                    window.location.reload()
                failure: (error) =>
                    alert("failure!")

        @cancelPayment= () ->
            $.apptools.api.payment.cancel_payment(
                "payment": this.id
            ).fulfill
                success: (response) =>
                    alert("Success! Reloading page...")
                    window.location.reload()
                failure: (error) =>
                    alert("failure!")


if @__openfire_preinit?
    @__openfire_preinit.abstract_base_controllers.push(UserAccountController)
