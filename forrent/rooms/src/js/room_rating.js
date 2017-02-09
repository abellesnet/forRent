var $ = require('jquery');
var RatingService = require('./rating_service');

var RoomRating = {
    _selector: '.room-rating',
    getRoomPk: function () {
        return $(this._selector).data('room-pk');
    },
    getApi: function () {
        return $(this._selector).data('roomrating-api');
    },
    drawStars: function (rating) {
        for (var i = 1; i <= 5; i++) {
            if (i <= rating) {
                $(this._selector).find('#star' + i).removeClass('glyphicon-star-empty');
                $(this._selector).find('#star' + i).addClass('glyphicon-star');
            } else {
                $(this._selector).find('#star' + i).removeClass('glyphicon-star');
                $(this._selector).find('#star' + i).addClass('glyphicon-star-empty');
            }
        }
        return this;
    },
    setStarsBehavior: function (rating) {
        var self = this;
        $(this._selector).find('.rating-star').on('click', function () {
            var starNumber = this.id.slice(-1);
            if (!rating) {
                rating = {}
            }
            rating.rate = starNumber;
            RatingService.setMyRating(
                RoomRating.getApi(),
                RoomRating.getRoomPk(),
                rating,
                function (response) {
                    self.drawStars(starNumber);
                },
                function (response) {
                    alert(response.responseJSON.detail);
                }
            );

        });
    },
};

$(document).ready(function () {

    if ((RoomRating.getRoomPk()) && (RoomRating.getApi())) {
        RatingService.getMyRating(
            RoomRating.getApi(),
            RoomRating.getRoomPk(),
            function (response) {
                if (response.length > 0) {
                    RoomRating.setStarsBehavior(response[0]);
                    RoomRating.drawStars(response[0].rate);
                } else {
                    RoomRating.setStarsBehavior();
                }
            },
            function (response) {
                alert(response.responseJSON.detail);
            }
        );
    }

});

