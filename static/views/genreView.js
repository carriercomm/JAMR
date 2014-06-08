define([
  "text!templates/genre.html"
], function(template){
  return Backbone.View.extend({
    tagName: "div",
    template: template,

    initialize: function() {
      this.render();
    },

    events: {
      "click #next": "next",
    },

    next: function() {
      var genre = $('.ui-selected').attr('id');
      if(genre && genre.length > 0) {
        this.remove();
        app.map();
      }
    },

    render: function() {
      this.$el.html( this.template );
      this.delegateEvents();
      return this;
    },
  });
});
