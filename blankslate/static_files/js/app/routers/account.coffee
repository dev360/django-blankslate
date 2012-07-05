class blankslate.routers.Account extends Backbone.Router
  routes:
    'account': "account"

  account: ->
    view = new blankslate.forms.AccountForm(model: @page)
    $('.profile.edit').html view.render()
