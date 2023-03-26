$('#screenModal').on('hidden.bs.modal', function(e) {
});
$(document).on("click", ".open-AddGroupsDialog", function () {
     var botId = $(this).data('id');
     var stackId = $(this).data('value');
     $(".modal-header #botId").val( botId );
     document.getElementById("stackId").textContent=stackId;

});