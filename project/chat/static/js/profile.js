document.getElementById('profileImage').addEventListener('click', function() {
    document.getElementById('profilePictureInput').click();
});

document
    .getElementById("profilePictureInput")
    .addEventListener("change", function(event) {
        const fileReader = new FileReader();
        fileReader.onload = function(e) {
            document.querySelector(".profile-img img").src = e.target.result;
        };
        fileReader.readAsDataURL(event.target.files[0]);
    });

document.getElementById('profilePictureInput').addEventListener('change', function() {
    var form_data = new FormData();
    form_data.append('profile_picture', this.files[0]);

    fetch("{% url 'your_django_upload_view_url_name' %}", {
            method: 'POST',
            body: form_data,
            credentials: 'include', // For CSRF token
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // CSRF token
            }
        })
        .then(response => response.json())
        .then(data => {
            // Update the profile image if upload is successful
            if (data.success) {
                document.getElementById('profileImage').src = data.image_url;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

// Helper function to get the value of a cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}