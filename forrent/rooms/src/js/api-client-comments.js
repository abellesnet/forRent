var $ = require('jquery');

module.exports = {

    save: function (comment, api, successCallback, errorCallback) {
        var formData = new FormData();
        formData.append("room", comment.roomId);
        formData.append("comment", comment.comment);
        $.ajax({
            url: api,
            method: "post",
            data: formData,
            processData: false,
            contentType: false,
            success: successCallback,
            error: errorCallback
        });
    },

    list: function (roomId, api, successCallback, errorCallback) {
        $.ajax({
            url: api + "?room=" + roomId,
            method: "get",
            success: successCallback,
            error: errorCallback
        });
    }

};