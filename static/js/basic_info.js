$(document).ready(function() {
	var form = $("#form");
	
	var person_id = window.location.pathname.split("/")[2];
	$('.datepicker').datepicker();
	
	var get_basic_info = function(person_id){
		var data = "person_id="+person_id;
		jQuery.ajax({
			type : "POST",
			dataType: "json", 
			url : "/api/person/basic_info/get",
			data : data,
			success : function(data) {
				if (data.success == true) {
					except = []
					$.each(data.value, function( name, value ) {
						if (jQuery.inArray(name, except)  > -1) {
							return;
						}
						$("[name="+name+"]").val(value);
					});
				} else {
					show_message(data.reason, "error");
				}
			}
		});
	}

	var submit_data = function(person_id) {
		var data = form.serialize();
		data += "&person_id="+person_id;
		jQuery.ajax({
			type : "POST",
			dataType: "json", 
			url : "/api/person/basic_info/update",
			data : data,
			success : function(data) {
				if (data.success == true) {
					show_message("Succesfully updated basic info for person");
					window.location.href = "/id_upload/"+person_id;
				}
			}
		});
	};
	
	if (person_id) {
		get_basic_info(person_id);
		navbar(person_id, $("#navbar_container"));
	}
	
	form.submit(function(event) {
		event.preventDefault();
		if (person_id) {
			submit_data(person_id);
		} else {
			jQuery.ajax({
				type : "POST",
				dataType: "json", 
				url : '/api/person/new',
				data : {},
				success : function(data) {
					if (data.success == true) {
						show_message("Succesfully created new person. Submitting data... ");
						setTimeout(function() {
							submit_data(data.person_id);
						}, 100);
						
					}
				}
			});
		}

	});
});