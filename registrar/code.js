fetch('/register', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
})
.then(response => response.text())
.then(data => {
    // Display success message
    document.getElementById('registrationMessage').textContent = data;
    document.getElementById('registrationMessage').style.display = 'block';

    // Clear form fields
    document.getElementById('registrationForm').reset();
})
.catch(error => {
    console.error('Error:', error);
});