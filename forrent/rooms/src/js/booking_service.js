var $ = require('jquery');

module.exports = {

    create: function (api, booking) {
        var deferred = $.Deferred();
        $.post(api, booking)
            .done(function (response) {
                deferred.resolve(response);
            })
            .fail(function (response) {
                deferred.reject(response);
            });
        return deferred;
    }

};