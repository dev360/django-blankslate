(function() {
  var __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  rf.models.Address = (function(_super) {

    __extends(Address, _super);

    function Address() {
      Address.__super__.constructor.apply(this, arguments);
    }

    Address.prototype.defaults = {
      id: ""
    };

    Address.prototype.url = function() {
      var id;
      id = this.get('id');
      return "/api/1.0/account/profile/addresses/" + id + "/?format=json";
    };

    return Address;

  })(Backbone.Model);

  rf.models.AddressList = (function(_super) {

    __extends(AddressList, _super);

    function AddressList() {
      AddressList.__super__.constructor.apply(this, arguments);
    }

    AddressList.prototype.defaults = {
      id: ""
    };

    AddressList.prototype.url = function() {
      return "/api/1.0/account/profile/addresses/?format=json";
    };

    return AddressList;

  })(Backbone.Collection);

}).call(this);
