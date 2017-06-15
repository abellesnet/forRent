var $ = require('jquery');

module.exports = {

    clearCommentsList: function () {
        $(".comments-list").html('<div class="comments-container"></div>');
    },

    renderComment: function (comment) {
        const htmlComment = '\
            <div class="row">\
                <div class="col-xs-2 col-sm-1">\
                    <a class="author author-photo" href="/author-endpoint">\
                        <img class="host-photo"\
                             src="/author-photo"\
                             alt="Author full name">\
                    </a>\
                </div>\
                <div class="col-xs-10 col-sm-11">\
                    <div class="row">\
                        <div class="col-xs-12">\
                            <a class="author author-name"\
                               href="{{ room.host.profile.get_absolute_url }}">\
                                Author full name\
                            </a>\
                        </div>\
                        <div class="col-xs-12">\
                            <span class="comment-date">The date</span>\
                        </div>\
                    </div>\
                </div>\
            </div>\
            <div class="row">\
                <div class="comment col-xs-12">\
                    <p class="comment-text">The comment</p>\
                </div>\
            </div>\
            <hr>\
        ';
        const newComment = $(htmlComment);
        var commentDate = new Date(comment.created_at);
        newComment.find("a.author").attr('href', comment.author_url);
        newComment.find("img").attr('src', comment.author_photo);
        newComment.find("img").attr('alt', comment.author_full_name);
        newComment.find("a.author-name").text(comment.author_full_name);
        newComment.find(".comment-date").text(commentDate.toLocaleString(window.navigator.language));
        newComment.find(".comment-text").text(comment.comment);
        $(".comments-container").append(newComment);
    }

};
