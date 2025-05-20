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

    {{-- <script>
        setInterval(() => {
            fetch('/api/latest-weight')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('liveWeight').innerText = data.weight + ' kg';
                })
                .catch(err => console.error("Fetch error:", err));
        }, 5000); // refresh every second
    </script> --}}

    <script>
    setInterval(() => {
        fetch('/api/latest-weight')
            .then(res => {
                if (!res.ok) {
                    throw new Error(`HTTP error! status: ${res.status}`);
                }
                return res.json();
            })
            .then(data => {
                document.getElementById('liveWeight').innerText = data.weight + ' kg';
            })
            .catch(err => {
                console.error("Fetch error:", err);
                document.getElementById('liveWeight').innerText = "Error fetching weight";
            });
    }, 1000); // refresh every 5 seconds
</script>


</body>
</html>
