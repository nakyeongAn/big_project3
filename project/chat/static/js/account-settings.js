// Bootstrap 탭 기능 활성화
$(document).ready(function() {
    $('.nav-tabs a').click(function() {
        $(this).tab('show');
    });
});