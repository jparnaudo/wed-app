var show_message = function(message, type) {
	if (!type)
		type = "success";

	$('.top-right').notify({
		"type" : type,
		message : {
			"text" : message
		},
		fadeOut: { enabled: true, delay: 5000 }
	}).show();
}

$(document).ready(function() {
	var BUTTONS_SELECTOR = ":button, button";
	$.ajaxSetup({
		beforeSend : function() {
			$("#loading").show();
			$(BUTTONS_SELECTOR).prop("disabled", true);
		},
		complete : function() {
			$("#loading").hide();
			$(BUTTONS_SELECTOR).prop("disabled", false);
		}
	});

});