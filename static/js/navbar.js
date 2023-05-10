$('.login').on('click', function () {
    fetch('/user/isLogin')
        .then(response => response.json())
        .then(data => {
            if (!data.isLogin)
                location.href = '/user/login/';
        });
});

$('document').ready(function () {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    console.log(urlParams.get('query'))
    $('#query').val(urlParams.get('query'));
});
