$('#screenModal').on('hidden.bs.modal', function(e) {
});
$(document).on("click", ".open-screenDialog", function () {
     var image = $(this).data('value');
     document.getElementById("postImage").src = 'data:image/png;base64, '+ image;

});