$(document).ready(function () {
    fetch('/user/isLogin')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.islogin) {
                console.log('ok');
            }
        });
});

