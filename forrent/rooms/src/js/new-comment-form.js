var $ = require('jquery');
var apiClientComments = require('./api-client-comments');


module.exports = {

    setupSubmitEvent: function (roomId, api, afterSavingCB) {
        var self = this;
        $('.new-comment').on("submit", function () {
            var elements = $(".form-control");
            for (var i = 0; i < elements.length; i++) {
                var element = elements[i];
                if (element.checkValidity() == false) {
                    alert(element.validationMessage);
                    $(element).focus();
                    return false;
                }
            }
            var commentObject = {
                roomId: roomId,
                comment: $(".comments").find("#comment").val()
            };
            self.setSavingComment();
            apiClientComments.save(commentObject, api, function () {
                $(".new-comment")[0].reset();
                self.unsetSavingComment();
                $(".comments").find("#name").focus();
                afterSavingCB(roomId, api);
            }, function () {
                alert('Comment sending error');
                self.unsetSavingComment();
                $(".comments").find("#name").focus();
            });
            return false;
        });
    },

    setSavingComment: function () {
        $('.form-control').attr("disabled", true);
        $('.form-button').text("Sending comment...").attr("disabled", true);
    },

    unsetSavingComment: function () {
        $('.form-control').attr("disabled", false);
        $('.form-button').text("Send comment").attr("disabled", false);
    },

};