$(document).ready(function() {
    $('#uploadForm').submit(function(event) {
        event.preventDefault();
        let formData = new FormData($(this)[0]);
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                $('#message').text(response);
            },
            error: function(xhr, status, error) {
                $('#message').text('Error uploading image');
            }
        });
    });
});
