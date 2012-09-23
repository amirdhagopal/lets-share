var accommodationPage = {
	submit: function() {
      $("#accommodation").submit();
    }
}

var profilePage = {
	submit: function() {
      $("#profile").submit();
    }
}

var transportPage = {
	submit: function() {
      $("#transport").submit();
    }
}

var corporatePage = {
  submit: function() {
      $("#corporate").submit();
    }
}

var userOperation = {
	logout: function(){
	}
}

$('[data-role="page"]').live('pageshow', function () {
    //priceRange
    $('#buying_slider_min').change(function() {
        var min = parseInt($(this).val());
        var max = parseInt($('#buying_slider_max').val());
        if (min > max) {
            $(this).val(max);
            $(this).slider('refresh');
        }
    });
    $('#buying_slider_max').change(function() {
        var min = parseInt($('#buying_slider_min').val());
        var max = parseInt($(this).val());

        if (min > max) {
            $(this).val(min);
            $(this).slider('refresh');
        }
    });
});
