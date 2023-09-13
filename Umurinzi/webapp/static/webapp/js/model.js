$(document).ready(function () {
    // Attach a click event listener to the "Claim Item" button
    $('#claim-form-btn').click(function () {
        // Get the item ID from the button's data attribute
        var itemID = $(this).data('item-id');
        console.log("item", itemID);

        // Get the CSRF token from the cookie
        var csrftoken = getCookie('csrftoken');

        // Make an AJAX request to the Django view
        $.ajax({
            url: '/claimitem/' + itemID,
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },  // Include the CSRF token in the headers
            success: function (response) {
                if (response.hasOwnProperty('user')) {
                    var formattedContent = '<div>';
                    formattedContent += '<p><strong>Names:</strong> ' + response.user.Names + '</p>';

                    if (response.user.tel_no) {
                        formattedContent += '<p><strong>Telephone:</strong> ' + response.user.tel_no + '</p>';
                    }

                    formattedContent += '</div>';

                    // Update the modal body content with the formatted HTML
                    $('#staticBackdrop .modal-body').html(formattedContent);

                    // Open the modal
                    $('#staticBackdrop').modal('show');
                } else {
                    // Display the "message" property from the JSON response
                    var message = response.hasOwnProperty('message') ? response.message : 'No message available';
                    $('#staticBackdrop .modal-body').html('<p><strong>Message:</strong> ' + message + '</p>');
                    $('#staticBackdrop').modal('show');
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });

    // Function to get the CSRF token from the cookie
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $("#report-form-btn").click(function (event) {
        // Prevent the default form submission
        event.preventDefault();

        // Submit the form programmatically
        $("#report-form").submit();
    });

});