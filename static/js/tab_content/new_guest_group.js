$(document).ready(function() {

	var new_guest_group_form = $("#new_guest_group_form");
	
	new_guest_group_form.submit(function(event) {
		event.preventDefault();
		var data = new_guest_group_form.serialize();
		jQuery.ajax({
			type : "POST",
			dataType: "json", 
			url : "/api/guest_group/new",
			data : data,
			success : function(data) {
				if (data.success == true) {
					show_message("Succesfully created new Guest Group");
					// TODO: update table
				}
				else{
					show_message(data.info, "error");
				}
			}
		});

	});
});