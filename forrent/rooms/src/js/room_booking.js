var $ = require('jquery');
var BookingService = require('./booking_service');

var RoomBookingForm = {

    _selector: '.booking-form',
    since: null,
    to: null,

    getRoomPk: function () {
        return $(this._selector).find('.range').data('room-pk')
    },

    getPrice: function () {
        return parseFloat($(this._selector).find('.range').data('price'));
    },

    getApi: function () {
        return $(this._selector).find('.range').data('api')
    },

    getLanguage: function () {
        return $(this._selector).find('.range').data('date-language');
    },

    setSince: function (since) {
        this.since = since;
    },

    setTo: function (to) {
        this.to = to;
    },

    getDays: function () {
        if (!this.since || !this.to) {
            return 0;
        }
        var start = new Date(this.since);
        var end = new Date(this.to);
        return Math.floor((end - start) / (24 * 60 * 60 * 1000));
    },

    isValid: function () {
        return this.getRoomPk() && this.since && this.to && this.getDays() > 0;
    },

    disableButton: function () {
        $(this._selector).find("#submit_button").attr('disabled', 'disabled');
        return this;
    },

    enableButton: function () {
        $(this._selector).find("#submit_button").removeAttr('disabled');
        return this;
    },

    getBooking: function () {
        return {
            room: this.getRoomPk(),
            since: this.since,
            to: this.to,
            total_price: (this.getPrice() * this.getDays()).toFixed(2)
        };
    },

};

function updatePrice() {
    if (RoomBookingForm.isValid()) {
        var days = RoomBookingForm.getDays();
        $('#days').html(days);
        var pricePerDay = RoomBookingForm.getPrice();
        $('#price').html((pricePerDay * days).toFixed(2).concat(' €'));
        RoomBookingForm.enableButton();
    } else {
        $('#days').html('');
        $('#price').html('');
        RoomBookingForm.disableButton();
    }
}


$(document).ready(function () {

    RoomBookingForm.disableButton();

    $('.range').datepicker({
        inputs: $('.range-start, .range-end')
    });

    $('#datepicker1').on('changeDate', function () {
        var since = $('#datepicker1').datepicker('getFormattedDate');
        RoomBookingForm.setSince(since);
        $('#since').html(new Date(since).toLocaleDateString(RoomBookingForm.getLanguage()));
        updatePrice();
    });

    $('#datepicker2').on('changeDate', function () {
        var to = $('#datepicker2').datepicker('getFormattedDate');
        RoomBookingForm.setTo(to);
        $('#to').html(new Date(to).toLocaleDateString(RoomBookingForm.getLanguage()));
        updatePrice();
    });

    $(".booking-form").on("submit", function () {
        if (RoomBookingForm.isValid()) {
            $('ul.errorlist').html('');
            RoomBookingForm.disableButton();
            BookingService.create(RoomBookingForm.getApi(), RoomBookingForm.getBooking())
                .done(function (createdBooking) {
                    window.location.replace(createdBooking.url);
                })
                .fail(function (response) {
                    $('ul.errorlist').append('<li>' + response.responseText + '</li>');
                });
        }
        return false;
    });

});


