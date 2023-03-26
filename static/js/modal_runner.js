$('#runnerModal').on('hidden.bs.modal', function(e) {
    var table = $('#dataTableForRunning').DataTable()
    table.clear().draw();
    table.destroy();
});

$(document).on("click", ".open-RunningDialog", function () {
     var dst_id = $(this).data('id');
     $.ajax({
                type: 'POST',
                async: true,
                url: '/tools/',
                data: {'dst_id': dst_id},
                headers:{
                    "X-CSRFToken": csrftoken
                },
                success: function(data) {
                    data.forEach(makeTable);
                    $('#dataTableForRunning').DataTable({
                        responsive: true
                    });
                },
            dataType: 'json',
            });

     var tableRef = document.getElementById('dataTableForRunning').getElementsByTagName('tbody')[0];
     function makeTable(value, index, array) {
        var newRow = tableRef.insertRow();
        var newCell1  = newRow.insertCell(0);
        var newCell2  = newRow.insertCell(1);
        var newCell3  = newRow.insertCell(2);
        var bot_id = document.createTextNode(value.bot_id);
        var link = document.createElement("div");
        var ip = document.createTextNode("ssh -i dsirf_fb_scrappers.pem -L 6080:"+value.ip+":6080 -C -N -l ubuntu 3.126.146.115");
        var redirect_link = value.link;
        //link.innerHTML = "<button name='check' type='button' data-id='"+value.bot_id+"' class='open-StreamDialog btn btn-outline btn-link' data-toggle='modal' data-target='#streamModal'>Open</button>"
        link.innerHTML = "<input type='button' value='Open' onclick='window.open(\""+redirect_link+"\")'>"
        newCell1.appendChild(bot_id);
        newCell2.appendChild(link);
        newCell3.appendChild(ip);
     }
});

$(document).on("click", ".open-StreamDialog", function () {
     var bot_id = $(this).data('id');
     $.ajax({
                type: 'POST',
                async: true,
                url: '/tools/',
                data: {'bot_id': bot_id},
                headers:{
                    "X-CSRFToken": csrftoken
                },
            dataType: 'json',
            });
});