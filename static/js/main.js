$(".like-question").on('click', function(ev){
    const request = new Request(
        'http://127.0.0.1:8000/like/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken' : csrftoken,
                'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'

            },
            body: 'question_id=' + $(this).data('id')
        }
    )

    fetch(request).then(
        response => response.json().then(
            (response) => {
                const old_count_likes = $(this).text(); 
                $(this).text(response.count_likes);
                const new_count_likes = $(this).text();
                if (new_count_likes > old_count_likes)
                {
                    $(this).addClass("like-up");
                }
                else
                {
                    $(this).removeClass("like-up");
                }
            }
        )
    );
})


$(".like-answer").on('click', function(ev){
    const request = new Request(
        'http://127.0.0.1:8000/like_answer/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken' : csrftoken,
                'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'

            },
            body: 'answer_id=' + $(this).data('id')
        }
    )

    fetch(request).then(
        response => response.json().then(
            (response) => {
                const old_count_likes = $(this).text(); 
                $(this).text(response.count_likes_answer);
                const new_count_likes = $(this).text();
                if (new_count_likes > old_count_likes)
                {
                    $(this).addClass("like-up");
                }
                else
                {
                    $(this).removeClass("like-up");
                }
            }
        )
    );
})