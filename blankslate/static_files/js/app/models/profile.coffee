#
# Profile
# -------
#
class blankslate.models.Profile extends Backbone.Model

  defaults:
    id: ""

  url: ->
    return "/api/1.0/account/profile/?format=json"

blankslate.app.data.profile = new blankslate.models.Profile()
