$('#screenModal').on('hidden.bs.modal', function(e) {
});
$(document).on("click", ".open-AddGroupsDialog", function () {
     var botId = $(this).data('id');
     var image = $(this).data('value');
     $(".modal-header #botId").val( botId );
     document.getElementById("botImage").src = 'data:image/png;base64, '+ image;

});