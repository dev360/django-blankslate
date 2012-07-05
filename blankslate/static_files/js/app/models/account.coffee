#
# Address
# ---------
#
class blankslate.models.Account extends Backbone.Model

  defaults:
    id: ""

  url: ->
    id = @.get('id')
    return "/api/1.0/account/?format=json"


