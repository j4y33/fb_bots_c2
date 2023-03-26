$('#groupsModal').on('hidden.bs.modal', function(e) {
    var table = $('#dataTableForGroups').DataTable()
    table.clear().draw();
    table.destroy();
});

function saveChanges() {
        var checkedBoxes = getCheckedBoxes("bot_groups");
        var botId = document.getElementsByName("botId")[0].value;

        console.log(rows_selected);
        $.ajax({
                type: 'POST',
                async: true,
                url: '/destination_lists/add',
                data: {'bot_id': botId, 'checked': checkedBoxes},
                headers:{
                    "X-CSRFToken": csrftoken
                },
                success: function() {
                    $('#groupsModal').modal('hide');
                },
            dataType: 'json',
            });
}
function getCheckedBoxes(chkboxName) {
  var checkboxes = document.getElementsByName(chkboxName);
  var checkboxesChecked = [];
  // loop over them all
  for (var i=0; i<checkboxes.length; i++) {
     // And stick the checked ones onto an array...
     if (checkboxes[i].checked) {
        checkboxesChecked.push(checkboxes[i].value);
     }
  }
  // Return the array if it is non-empty, or null
  return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}
$(document).on("click", ".open-AddGroupsDialog", function () {
     var botId = $(this).data('id');
     $(".modal-header #botId").val( botId );
     $.ajax({
                type: 'POST',
                async: true,
                url: '/destination_lists/add',
                data: {'bot_id': botId},
                headers:{
                    "X-CSRFToken": csrftoken
                },
                success: function(data) {
                    data.forEach(makeTable);
                    $('#dataTableForGroups').DataTable({
                        responsive: true
                    });
                },
            dataType: 'json',
            });

     var tableRef = document.getElementById('dataTableForGroups').getElementsByTagName('tbody')[0];
     function makeTable(value, index, array) {
        console.log(value.group_name);
        var newRow = tableRef.insertRow();
        var newCell1  = newRow.insertCell(0);
        var newCell2  = newRow.insertCell(1);

        var cb = document.createElement('input');
            cb.type = 'checkbox';
            cb.name = 'bot_groups';
            cb.value = value.id;
            cb.checked = value.dst_select_status;

        var group = document.createTextNode(value.group_name);
        newCell1.appendChild(cb);
        newCell2.appendChild(group);
     }
});