
matchAt = (s, frag, i) ->
  s[i...i+frag.length] == frag
 
startsWith = (s, frag) ->
  matchAt s, frag, 0
 
endsWith = (s, frag) ->
  matchAt s, frag, s.length - frag.length


#
# Address
# ---------
#
class Backbone.Form extends Backbone.View

  # Templates
  template: _.template($('#form-template').html())
  fieldsetTemplate: _.template($('#form-fieldset-template').html())
  fieldTemplate: _.template($('#form-field-template').html())


  fields: {
    
  }

  render: () ->
    $(@el).html(@template())
    #$('.profile.edit').html(@el)

    #fieldsets = if @fieldset then @fieldset else []

    fieldTemplate = @fieldTemplate

    _.each(_.values(@fields).reverse(), (field)=>

      fieldView = field
      fieldView.template = fieldTemplate

      placeholder = if typeof @placeholder isnt 'undefined' then @placeholder else 'form'

      $(@el).find(placeholder).prepend(fieldView.render().el)
    )


    # $(@el).html @template()
    return @el

  save: () ->
    
    errors = []

    for field in @fields
      do (field) ->
        errors = errors.concat field.validateFields(field.getValue())

    if errors.length == 0
      # save shit
      console.log "save"
    


Backbone.Fields = {}

class Backbone.Fields.BaseField extends Backbone.View

  className: 'control-group'
  tagName: 'div'

  type: 'input["text"]'

  value: null

  errors: []

  constructor: (opts) ->
    @attr = opts.attr
    @name = if typeof opts.id isnt 'undefined' then "id_#{opts.name}" else ""
    @label = opts.label or ""
    @maxLength = opts.maxLength or 100
    @required = if typeof opts.required isnt 'undefined' then opts.required else true
    @default = if typeof opts.default isnt 'undefined' then opts.default else ''
    
    super("Backbone.Fields.BaseField")

  initialize: () ->
    _.bindAll(@, "render")
    @render()

  getValue: () ->
    if startsWith @type, "input"
      return $(@el).find('input').val()

  validateFields: (value) ->
    errors = []
    
    # TODO: Check required
    if @required and not value
      errors.push ['This field is required']

    if @maxLength and value.length > @maxLength
      errors.push ['The value is too long']

    return errors
 
  changed: () =>
    value = @getValue()
    errors = @validateFields(value)

    moreErrors = if typeof @validate isnt 'undefined' then @validate(value) else []

    @errors = errors.concat moreErrors
    @render()


  render: () ->
    
    data = 
      id: "id_#{@attr}"
      name: @name
      type: @type
      label: @label
      maxLength: @maxLength
      required: @required
      value: @getValue() or @default
      errors: @errors

    $(@el).html @template(data)

    if @required
      $(@el).addClass('required')

    if @errors.length > 0
      $(@el).addClass('error')
    else
      $(@el).removeClass('error')

    if startsWith @type, "input"
      $(@el).find('input').blur(@changed)

    return @


class Backbone.Fields.CharField extends Backbone.Fields.BaseField 
  
  initialize: (opts) ->
    
    console.log(opts)


class Backbone.Fields.EmailField extends Backbone.Fields.CharField

  type: 'input["email"]'
  
  maxLength: 255


  validate: (value) ->
    errors = []
    pattern = ///
      .+\@.+\..+
    ///

    if value and not value.match(pattern)
      errors.push ['Invalid email address']

    return errors

