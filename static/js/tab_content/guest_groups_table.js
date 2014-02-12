$(document).ready(function() {

	var table = $("#guest_groups_table");
	var head = $('<thead></thead>').appendTo(table);
	var head_row = $('<tr></tr>').appendTo(head);
	$('<th></th>').text("Guest Group").appendTo(head_row);
	$('<th></th>').text("Group Size").appendTo(head_row);
	$('<th></th>').text("Action").appendTo(head_row);
	var body = $("<tbody></tbody>").appendTo(table)

	$.getJSON("/api/guest_group/list", function(data) {
		if (data.success == true) {

			$.each(data.list, function(key, gg) {
				var gg_name = gg.group_name;
				var gg_size = gg.group_size;

				var body_row = $('<tr></tr>').appendTo(body);
				$('<td></td>').text(gg_name).appendTo(body_row);
				$('<td></td>').text(gg_size).appendTo(body_row);
				var button_cell = $('<td></td>').appendTo(body_row);

				var link = $('<a></a>', {"class":"btn input-medium btn-inverse"}).text("Delete group ").appendTo(button_cell);
				link.append($("<i></i>",{"class":"icon-trash icon-white"}));
				
				link.click(function(){
					var data = "group_name="+gg_name;
					jQuery.ajax({
						type : "POST",
						dataType : "json",
						url : "/api/guest_group/delete",
						data : data,
						success : function(data) {
							if (data.success == true) {
								show_message("Guest Group deleted.", "success");
								// TODO: update table

							} else {
								show_message(data.info, "error");
							}
						}
					});
				});

			});
		}

	});
});