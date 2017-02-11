var apiClientComments = require('./api-client-comments');
var commentsRenderer = require('./comments-renderer');
var newCommentForm = require('./new-comment-form');


module.exports = {

    init: function (roomId, api) {
        this.loadComments(roomId, api);
        newCommentForm.setupSubmitEvent(roomId, api, this.loadComments);
    },

    loadComments: function (roomId, api) {
        apiClientComments.list(roomId, api, function (response) {
            commentsRenderer.clearCommentsList();
            for (var i = 0; i < response.length; i++) {
                var comment = response[i];
                commentsRenderer.renderComment(comment);
            }
        }, function (response) {
            commentsRenderer.clearCommentsList();
        });
    }

};