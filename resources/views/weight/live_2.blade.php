<div>
    Current Weight: <span id="weight-display">0.000</span> kg
</div>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
    function fetchWeight() {
        $.ajax({
            url: '/api/latest-weight',
            method: 'GET',
            success: function(response) {
                $('#weight-display').text(response.weight);
            },
            error: function() {
                $('#weight-display').text('Error fetching weight');
            }
        });
    }

    // Fetch every 1 second
    setInterval(fetchWeight, 500);

    // Initial fetch
    fetchWeight();
</script>
