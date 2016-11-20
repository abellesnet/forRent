var $ = require('jquery');

$(document).ready(function () {
    $('.go-top').on("click", function () {
        $('body').animate({scrollTop: 0}, 1000);
    });
});

