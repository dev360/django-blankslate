if (window.location.hash == "#_")
  window.location.hash = "#";


// Provide top-level namespaces for our javascript.
(function() {
  window.blankslate = {}

  // Set the class namespaces
  blankslate.forms = {};
  blankslate.routers = {};
  blankslate.models = {};
  blankslate.views = {};

  // Set instance namespaces where
  // instances of the classes will live
  blankslate.app = {};
  blankslate.app.routers = {};
  blankslate.app.ui = {};
  blankslate.app.data = {}; 




})();

