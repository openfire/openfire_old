## openfire user account controllers

class UserAccountController extends OpenfireController

    constructor: (openfire, window) ->

        @_init = () =>

            wepaybtn.bind('click', @linkWePayAccount, false) if (wepaybtn = _('#link-wepay-account-btn'))?

            btn.bind('click', @createAccountForProject, false) for btn in _('.create-account-for-project')
            btn.bind('click', @removeMoneySource, false) for btn in _('.remove-money-source')
            btn.bind('click', @cancelPayment, false) for btn in _('.cancel-payment')
            btn.bind('click', @refundPayment, false) for btn in _('.refund-payment')
            btn.bind('click', @updateAccountBalance, false) for btn in _('.update-account-balance')
            btn.bind('click', @generateWithdrawal, false) for btn in _('.start-withdrawal')

            # Init jQuery.dataTable
            _.ready ->
                if (dt = $(".payment-table")).length
                    dt.dataTable()

            return @

        @linkWePayAccount = () =>
            $.apptools.api.payment.get_auth_url().fulfill
                success: (response) =>
                    _('#link-wepay-account-inline').fadeIn()
                    link = _('#link-wepay-account-link')
                    link.html(response.url)
                    link.attr('href', response.url)

                failure: (error) =>
                    @log "Failed to get auth url to link WePay account: " + error

        @createAccountForProject = () ->
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

        @refundPayment= () ->
            $.apptools.api.payment.refund_payment(
                "payment": this.id
            ).fulfill
                success: (response) =>
                    alert("Success! Reloading page...")
                    window.location.reload()
                failure: (error) =>
                    alert("failure!")

        @updateAccountBalance = () ->
            $.apptools.api.payment.update_account_balance(
                "key": this.id
            ).fulfill
                success: (response) =>
                    alert("Success! Reloading page...")
                    window.location.reload()
                failure: (error) =>
                    alert("failure!")

        @generateWithdrawal = () ->
            accountID = this.id
            $.apptools.api.payment.withdraw_funds(
                "account": accountID
            ).fulfill
                success: (response) =>
                    elem = _('#account-'+accountID)
                    elem.fadeIn()
                    elem.html(response.wepay_withdrawal_uri)
                    elem.attr('href', response.wepay_withdrawal_uri)

                failure: (error) =>
                    alert("failure!")

        return @

if @__openfire_preinit?
    @__openfire_preinit.abstract_base_controllers.push(UserAccountController)
