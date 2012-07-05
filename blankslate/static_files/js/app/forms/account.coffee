#
# Account Form
# ------------
#
class blankslate.forms.AccountForm extends Backbone.Form

  id: 'account-form'

  model: blankslate.models.Account

  placeholder: '.form-horizontal'

  template: _.template($('#account-template').html())

  events: {
    '.btn-primary': 'save'
  }

  fields: {
    firstName: new Backbone.Fields.CharField({ attr: 'first_name', label: 'First name', maxLength: 255 }),
    middleName: new Backbone.Fields.CharField({ attr: 'middle_name', label: 'Middle name', maxLength: 255 }),
    lastName: new Backbone.Fields.CharField({ attr: 'last_name', label: 'Last name', maxLength: 255 }),
    email: new Backbone.Fields.EmailField({ attr: 'email', label: 'Email' }),
  }


