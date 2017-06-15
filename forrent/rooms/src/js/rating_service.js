var $ = require('jquery');

module.exports = {

    getMyRating: function (api, roomPk, successCallBack, errorCallBack) {
        $.get(api, {'room': roomPk})
            .then(successCallBack)
            .catch(errorCallBack);
    },

    setMyRating: function (api, roomPk, rating, successCallBack, errorCallBack) {
        if (rating.id) {
            // $.put(api + rating.id + '/', {'rate': rating.rate})
            $.ajax(api + rating.id + '/', {method: 'PATCH', data: {'rate': rating.rate}})
                .then(successCallBack)
                .catch(errorCallBack);
        } else {
            $.post(api, {'room': roomPk, 'rate': rating.rate})
                .then(successCallBack)
                .catch(errorCallBack);

        }
    },

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