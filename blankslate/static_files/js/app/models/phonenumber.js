(function() {
  var __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  rf.models.Phonenumber = (function(_super) {

    __extends(Phonenumber, _super);

    function Phonenumber() {
      Phonenumber.__super__.constructor.apply(this, arguments);
    }

    Phonenumber.prototype.defaults = {
      id: ""
    };

    Phonenumber.prototype.url = function() {
      console.log(this.get('profile'));
      return "/api/1.0/account/profile/phonenumbers/" + id + "/?format=json";
    };

    return Phonenumber;

  })(Backbone.Model);

  rf.models.PhonenumberList = (function(_super) {

    __extends(PhonenumberList, _super);

    function PhonenumberList() {
      PhonenumberList.__super__.constructor.apply(this, arguments);
    }

    PhonenumberList.prototype.url = function() {
      return "/api/1.0/account/profile/phonenumbers/?format=json";
    };

    return PhonenumberList;

  })(Backbone.Collection);

}).call(this);
