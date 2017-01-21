var $ = require('jquery');

$(document).ready(function () {

    $('.rating-star').on('click', function () {
        var starNumber = this.id.slice(-1);
        for (var i = 1; i <= 5; i++) {
            if (i <= starNumber) {
                $('#star' + i).removeClass('glyphicon-star-empty');
                $('#star' + i).addClass('glyphicon-star');
            } else {
                $('#star' + i).removeClass('glyphicon-star');
                $('#star' + i).addClass('glyphicon-star-empty');
            }
        }

    });

});

