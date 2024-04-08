function submitForm() {
    const serialNumber = document.getElementById('validationDefault01').value;
    const location = document.getElementById('validationDefaultUsername').value;
    const status = document.getElementById('validationDefault04').value;

    const data = {serialNumber, location, status};

    fetch ("/registro/database", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(data)
    }).then(response => response.json())
    .then(responseData => {
        const messageElement = document.getElementById('registrationMessage');
        messageElement.textContent = responseData.message;
        messageElement.style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}