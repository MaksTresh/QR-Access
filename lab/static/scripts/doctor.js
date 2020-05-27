function makeSalt(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    for (let i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

$('#generateBtn').click(function () {
    const salt = makeSalt(10);
    let data = {
        lastname: $('#lastname').val(),
        firstname: $('#firstname').val(),
        patronymic: $('#patronymic').val(),
        birthday: $('#date_birthday').val(),
        salt: salt
    }

    let qr_data = '';

    $.ajax({
        type: "POST",
        url: "/get_qr_data",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(qr_data){
            $('#sid').val('asd');
            $('.qrcodeCanvas').qrcode({
                text: platform_url+'check?data=' + encodeURIComponent(btoa(unescape(encodeURIComponent(JSON.stringify(qr_data))))),
                width: 300,
                height: 300
            });

            $('#sid').val(qr_data.sid);
            $('#salt').val(qr_data.salt);

            const canvas = document.querySelector('canvas');
            const dataURL = canvas.toDataURL("image/jpeg");
            let link = document.createElement("a");
            document.body.appendChild(link);
            link.href = dataURL;
            link.download = data.lastname + ' ' + data.firstname + ' ' + data.patronymic + '.jpg';
            link.click();
            document.body.removeChild(link);
        },
        failure: function(errMsg) {
            alert(errMsg);
        }
    });
    $('#sendDataBtn button').prop('disabled', false);
    $('#generateBtn button').prop('disabled', true);
});

$("#test_system").change(function() {
    const system_id = $('#test_system').val();
    $('#author_system').val(system_id);
    $('#certificate').val(system_id);
});

(function() {
    window.addEventListener('load', function() {
        const forms = document.getElementsByClassName('needs-validation');
        const validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

$('.date').datepicker({
    language: "ru"
});