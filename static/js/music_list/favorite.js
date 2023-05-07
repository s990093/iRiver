$('#table-body').on('click', '.love-icon a', function () {
    $(this).find('i').toggleClass('far fas');
    fetch(`/user/isLogin/`)
        .then(response => response.json())
        .then(data => {
            if (data.isLogin) {
                var music_ID = $(this).attr('value');
                const csrftoken = getCookie('csrftoken');
                fetch('/user/get_user_music_list/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },

                    body: JSON.stringify({
                        music_ID: music_ID,
                        method: 'insert'
                    })
                }).then(response => {
                    if (response.ok) {
                        // 保存成功
                        console.log('保存成功');
                    } else {
                        // 保存失败
                        console.log('保存失败');
                    }
                });
                // .then(response => response.json())
                // .then(data => {
                //   alert(data)
                // })
                // .catch(error => console.error(error));
            } else {
                location.href = "/user/login/";
            }
        });
});

$('#table-body').on('click', '.add', function () {
    $(this).find('i').toggleClass('far fas');
    fetch(`/user/isLogin/`)
        .then(response => response.json())
        .then(data => {
            if (data.isLogin) {
                var music_ID = $(this).attr('value');
                const csrftoken = getCookie('csrftoken');
                fetch('/user/get_user_music_list/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        music_ID: music_ID,
                        music_list: 2,
                        method: 'insert'
                    })
                }).then(response => {
                    if (response.ok) {
                        // 保存成功
                        console.log('保存成功');
                    } else {
                        // 保存失败
                        console.log('保存失败');
                    }
                });
                // .then(response => response.json())
                // .then(data => {
                //   alert(data)
                // })
                // .catch(error => console.error(error));
            } else {
                location.href = "/user/login/";
            }
        });
});

