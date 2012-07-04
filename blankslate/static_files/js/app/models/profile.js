(function() {
  var __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  rf.models.Profile = (function(_super) {

    __extends(Profile, _super);

    function Profile() {
      Profile.__super__.constructor.apply(this, arguments);
    }

    Profile.prototype.defaults = {
      id: ""
    };

    Profile.prototype.url = function() {
      return "/api/1.0/account/profile/?format=json";
    };

    return Profile;

  })(Backbone.Model);

  rf.app.data.profile = new rf.models.Profile();

}).call(this);
