$('.login').on('click', function () {
    console.log($('.login'))

    fetch('/user/isLogin')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.isLogin) {
                console.log(data);
            } else {
                location.href = '/user/login/';
            }
        });
});

