$('#joinedModal').on('hidden.bs.modal', function(e) {
    var table = $('#dataTableForJoinedGroups').DataTable()
    table.clear().draw();
    table.destroy();
});

$(document).on("click", ".open-AddGroupsDialog", function () {
     var botIds = $(this).data('id');
     var group_link = $(this).data('value');
     $.ajax({
                type: 'POST',
                async: true,
                url: '/tools/joiner',
                data: {'bot_ids': botIds,
                    'group_url': group_link},
                headers:{
                    "X-CSRFToken": csrftoken
                },
                success: function(data) {
                    data.forEach(makeTable);
                    $('#dataTableForJoinedGroups').DataTable({
                        responsive: true
                    });
                },
            dataType: 'json',
            });

     var tableRef = document.getElementById('dataTableForJoinedGroups').getElementsByTagName('tbody')[0];
     function makeTable(value, index, array) {
        console.log(value.group_name);
        var newRow = tableRef.insertRow();
        var newCell1  = newRow.insertCell(0);
        var newCell2  = newRow.insertCell(1);
        var newCell3  = newRow.insertCell(2);
        var newCell4  = newRow.insertCell(3);
        var bot_id = document.createTextNode(value.bot_id);
        var group = document.createTextNode(value.group_name);
        var status = document.createTextNode(value.status);
        var screenShot = document.createElement("td");
        screenShot.innerHTML = "<button name='openImage' type='button' data-value='"+value.screen+"' class='open-screenDialog btn btn-outline btn-link' data-toggle='modal' data-target='#screenModal'><img src='data:image/png;base64, "+value.screen+"' width='50' height='50' /></button>";
        newCell1.appendChild(bot_id);
        newCell2.appendChild(group);
        newCell3.appendChild(status);
        newCell4.appendChild(screenShot);
     }
});