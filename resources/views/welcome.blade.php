<h3>Current Weight: <span id="liveWeight">Waiting...</span></h3>
<script>
    Echo.channel('weight-channel')
    .listen('.weight-received', (e) => {
        console.log("Weight:", e.weight);
        document.getElementById('liveWeight').innerText = e.weight + ' kg';
    });

</script>