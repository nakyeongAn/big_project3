// DOM 요소 캐싱
var profileImage = document.getElementById("currentImage");
var profilePictureInput = document.getElementById("profilePictureInput");
var uploadUrl = uploadButton.getAttribute("data-upload-url");

// 파일 선택 시 동작하는 함수
function uploadImage(file) {
    // 로컬에서 이미지 미리보기
    var fileReader = new FileReader();
    fileReader.onload = function(e) {
        profileImage.src = e.target.result;
    };
    fileReader.readAsDataURL(file);

    // 서버로 이미지 전송
    var formData = new FormData();
    formData.append("profile_picture", file);

    fetch(uploadUrl, {
            method: "POST",
            body: formData,
            credentials: "include",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok " + response.statusText);
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                // 이미지 업데이트
                profileImage.src = data.image_url;
            } else {
                // 오류 처리
                alert("Failed to upload the image.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred: " + error.message);
        });
}

// 파일 선택 시 동작하는 이벤트 리스너
profilePictureInput.addEventListener("change", function(event) {
    if (this.files && this.files[0]) {
        uploadImage(this.files[0]);
    }
});

// CSRF 토큰 값을 가져오는 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}