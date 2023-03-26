$('#postsModal').on('hidden.bs.modal', function(e) {
    var table = $('#dataTableForPosts').DataTable()
    table.clear().draw();
    table.destroy();
});

$(document).on("click", ".open-PostsDialog", function () {
     var camp = $(this).data('id');
     $.ajax({
                type: 'POST',
                async: true,
                url: '/campaigns/what_publish/scrap_and_share_post',
                data: {'camp': camp},
                headers:{
                    "X-CSRFToken": csrftoken
                },
                success: function(data) {
                    data.forEach(makeTable);
                    $('#dataTableForPosts').DataTable({
                        responsive: true
                    });
                },
            dataType: 'json',
            });

     var tableRef = document.getElementById('dataTableForPosts').getElementsByTagName('tbody')[0];
     function makeTable(value, index, array) {
        console.log(value.url);
        var newRow = tableRef.insertRow();
        var newCell1  = newRow.insertCell(0);
        var newCell2  = newRow.insertCell(1);
        var url = document.createElement('a');
        var createText = document.createTextNode('link');
        url.setAttribute('href', value.url);
        url.appendChild(createText);
        var screenShot = document.createElement("td");
        screenShot.innerHTML = "<button name='openImage' type='button' data-value='"+value.screen+"' class='open-screenDialog btn btn-outline btn-link' data-toggle='modal' data-target='#screenModal'><img src='data:image/png;base64, "+value.screen+"' width='50' height='50' /></button>";
        newCell1.appendChild(url);
        newCell2.appendChild(screenShot);
     }
});