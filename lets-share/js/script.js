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
    $('#minbudget').change(function() {
        var min = parseInt($(this).val());
        var max = parseInt($('#maxbudget').val());
        if (min > max) {
            $(this).val(max);
            $(this).slider('refresh');
        }
    });
    $('#maxbudget').change(function() {
        var min = parseInt($('#minbudget').val());
        var max = parseInt($(this).val());

        if (min > max) {
            $(this).val(min);
            $(this).slider('refresh');
        }
    });
});
