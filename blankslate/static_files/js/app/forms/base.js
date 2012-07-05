// Generated by CoffeeScript 1.3.3
(function() {
  var endsWith, matchAt, startsWith,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  matchAt = function(s, frag, i) {
    return s.slice(i, i + frag.length) === frag;
  };

  startsWith = function(s, frag) {
    return matchAt(s, frag, 0);
  };

  endsWith = function(s, frag) {
    return matchAt(s, frag, s.length - frag.length);
  };

  Backbone.Form = (function(_super) {

    __extends(Form, _super);

    function Form() {
      return Form.__super__.constructor.apply(this, arguments);
    }

    Form.prototype.template = _.template($('#form-template').html());

    Form.prototype.fieldsetTemplate = _.template($('#form-fieldset-template').html());

    Form.prototype.fieldTemplate = _.template($('#form-field-template').html());

    Form.prototype.fields = {};

    Form.prototype.render = function() {
      var fieldTemplate,
        _this = this;
      $(this.el).html(this.template());
      fieldTemplate = this.fieldTemplate;
      _.each(_.values(this.fields).reverse(), function(field) {
        var fieldView, placeholder;
        fieldView = field;
        fieldView.template = fieldTemplate;
        placeholder = typeof _this.placeholder !== 'undefined' ? _this.placeholder : 'form';
        return $(_this.el).find(placeholder).prepend(fieldView.render().el);
      });
      return this.el;
    };

    Form.prototype.save = function() {
      var errors, field, _fn, _i, _len, _ref;
      errors = [];
      _ref = this.fields;
      _fn = function(field) {
        return errors = errors.concat(field.validateFields(field.getValue()));
      };
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        field = _ref[_i];
        _fn(field);
      }
      if (errors.length === 0) {
        return console.log("save");
      }
    };

    return Form;

  })(Backbone.View);

  Backbone.Fields = {};

  Backbone.Fields.BaseField = (function(_super) {

    __extends(BaseField, _super);

    BaseField.prototype.className = 'control-group';

    BaseField.prototype.tagName = 'div';

    BaseField.prototype.type = 'input["text"]';

    BaseField.prototype.value = null;

    BaseField.prototype.errors = [];

    function BaseField(opts) {
      this.changed = __bind(this.changed, this);
      this.attr = opts.attr;
      this.name = typeof opts.id !== 'undefined' ? "id_" + opts.name : "";
      this.label = opts.label || "";
      this.maxLength = opts.maxLength || 100;
      this.required = typeof opts.required !== 'undefined' ? opts.required : true;
      this["default"] = typeof opts["default"] !== 'undefined' ? opts["default"] : '';
      BaseField.__super__.constructor.call(this, "Backbone.Fields.BaseField");
    }

    BaseField.prototype.initialize = function() {
      _.bindAll(this, "render");
      return this.render();
    };

    BaseField.prototype.getValue = function() {
      if (startsWith(this.type, "input")) {
        return $(this.el).find('input').val();
      }
    };

    BaseField.prototype.validateFields = function(value) {
      var errors;
      errors = [];
      if (this.required && !value) {
        errors.push(['This field is required']);
      }
      if (this.maxLength && value.length > this.maxLength) {
        errors.push(['The value is too long']);
      }
      return errors;
    };

    BaseField.prototype.changed = function() {
      var errors, moreErrors, value;
      value = this.getValue();
      errors = this.validateFields(value);
      moreErrors = typeof this.validate !== 'undefined' ? this.validate(value) : [];
      this.errors = errors.concat(moreErrors);
      return this.render();
    };

    BaseField.prototype.render = function() {
      var data;
      data = {
        id: "id_" + this.attr,
        name: this.name,
        type: this.type,
        label: this.label,
        maxLength: this.maxLength,
        required: this.required,
        value: this.getValue() || this["default"],
        errors: this.errors
      };
      $(this.el).html(this.template(data));
      if (this.required) {
        $(this.el).addClass('required');
      }
      if (this.errors.length > 0) {
        $(this.el).addClass('error');
      } else {
        $(this.el).removeClass('error');
      }
      if (startsWith(this.type, "input")) {
        $(this.el).find('input').blur(this.changed);
      }
      return this;
    };

    return BaseField;

  })(Backbone.View);

  Backbone.Fields.CharField = (function(_super) {

    __extends(CharField, _super);

    function CharField() {
      return CharField.__super__.constructor.apply(this, arguments);
    }

    CharField.prototype.initialize = function(opts) {
      return console.log(opts);
    };

    return CharField;

  })(Backbone.Fields.BaseField);

  Backbone.Fields.EmailField = (function(_super) {

    __extends(EmailField, _super);

    function EmailField() {
      return EmailField.__super__.constructor.apply(this, arguments);
    }

    EmailField.prototype.type = 'input["email"]';

    EmailField.prototype.maxLength = 255;

    EmailField.prototype.validate = function(value) {
      var errors, pattern;
      errors = [];
      pattern = /.+\@.+\..+/;
      if (value && !value.match(pattern)) {
        errors.push(['Invalid email address']);
      }
      return errors;
    };

    return EmailField;

  })(Backbone.Fields.CharField);

}).call(this);