$('.login').on('click', function () {
    fetch('/user/isLogin')
        .then(response => response.json())
        .then(data => {
            if (!data.isLogin)
                location.href = '/user/login/';
        });
});

