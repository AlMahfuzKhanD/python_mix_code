<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Live Weight</title>
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; }
        #liveWeight { font-size: 3em; color: green; }
    </style>
</head>
<body>

    <h2>Live Weight</h2>
<div id="liveWeight">Waiting...</div>
<button onclick="saveWeight()">💾 Save</button>

<script>
    // Fetch live weight every 2 seconds
    setInterval(() => {
        fetch('/api/latest-weight')
            .then(res => res.json())
            .then(data => {
                document.getElementById('liveWeight').innerText = data.weight + ' kg';
            })
            .catch(err => console.error("Fetch error:", err));
    }, 2000);

    // Save button function
    function saveWeight() {
        fetch('/api/save-weight', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            }
        })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
        })
        .catch(err => {
            console.error("Save error:", err);
            alert("Failed to save weight.");
        });
    }
</script>



</body>
</html>
