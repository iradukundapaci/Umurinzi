$(document).ready(function () {
    // Attach a click event listener to the "Report" button
    $('#submit-report').click(function (e) {
        e.preventDefault();  // Prevent the default button click behavior

        // Submit the form using the submit method
        $('#report-form').submit();
    });
});