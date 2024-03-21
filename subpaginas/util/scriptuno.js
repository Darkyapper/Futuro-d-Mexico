function submitForm()
{
    var form = document.getElementById('registrationForm');
    var formData = new formData(form);
    var xhr = new XMLHttpRequest();

    xhr.open("POST", "http://localhost:8000/subpaginas/registro.html");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function()
    {
        if (xhr.readyState == 4)
        {
            if (xhr.status == 200)
            {
                var registrationMessage = document.getElementById('registrationMessage');
                registrationMessage.style.display = 'block';
                setTimeout(function()
                {
                    registrationMessage.style.display = 'none';
                }, 3000);
            } else
            {
                console.error(xhr.statusText);
            }
        }
    };
    var jsonData = {};
    formData.forEach(function (value, key) {
        jsonData[key] = value;
    });
    xhr.send(JSON.stringify(jsonData));
}