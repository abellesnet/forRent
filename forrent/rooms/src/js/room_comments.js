var $ = require('jquery');
var commentsController = require('./comments-controller');

$(document).ready(function () {

    var roomId = $(".comments").data('room-pk');
    var api = $(".comments").data('roomcomments-api');
    if ((roomId) && (api)) {
        commentsController.init(roomId, api);
    }
});


