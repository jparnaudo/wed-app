$(document).ready(function() {

	var guest_form = $("#new_guest_form");
	var guest_id = window.location.pathname.split("/")[2];
	
	var submit_guest_data = function(guest_id) {
		var data = guest_form.serialize();
		data += "&guest_id="+guest_id;
		jQuery.ajax({
			type : "POST",
			dataType: "json", 
			url : "/api/guest/update",
			data : data,
			success : function(data) {
				if (data.success == true) {
					show_message("Succesfully updated guest data");
					
				}
			}
		});
	};
	
	guest_form.submit(function(event) {
		event.preventDefault();
		if (guest_id) {
			submit_guest_data(guest_id);
		} else {
			jQuery.ajax({
				type : "POST",
				dataType: "json", 
				url : '/api/guest/new',
				data : {},
				success : function(data) {
					if (data.success == true) {
						show_message("Succesfully created new guest");
						setTimeout(function() {
							submit_guest_data(data.guest_id);
						}, 100);
						
					}
				}
			});
		}

	});
	
	if (guest_id) {
		
	}
});