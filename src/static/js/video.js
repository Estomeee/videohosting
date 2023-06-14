
let urls = ['http://127.0.0.1:8000/page/video_page/comments'] //fdgdfgdfg
url_sub = 'http://127.0.0.1:8000/interactions/protected-route/subscribe'
url_unsub = 'http://127.0.0.1:8000/interactions/protected-route/unsubscribe'
url_put_like = "http://127.0.0.1:8000/interactions/protected-route/put_like"
url_remove_like = "http://127.0.0.1:8000/interactions/protected-route/remove_like"
url_add_com = 'http://127.0.0.1:8000/interactions/protected-route/comment/add'
url_remove_com = 'http://127.0.0.1:8000/interactions/protected-route/comment/remove'

function add_comment(){

    textarea = document.getElementById('text_comment');
    text = textarea.value;
    id_video = document.location.href.split('=').slice(-1);
    var data = JSON.stringify({"text": text});

    let xhr = new XMLHttpRequest();
    let url = new URL(url_add_com);

    url.searchParams.set('id_video', id_video);


    xhr.open("POST", url)
    xhr.setRequestHeader("Content-Type", "application/json")

    xhr.send(data)

    xhr.onload = function() {
        if (xhr.status != 200) {
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            get_comment()
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
  }

function remove_comment(id_comment){

    let xhr = new XMLHttpRequest();
    let url = new URL(url_remove_com);

    url.searchParams.set('id_comment', id_comment);


    xhr.open("GET", url)
    xhr.send()

    xhr.onload = function() {
        if (xhr.status != 200) {
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            let comm = document.getElementById(id_comment)
            comm.remove()
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
  }


function remove_like(id_video) {
    like_request(id_video, url_remove_like, 'Поставить лайк', `put_like('${id_video}');`, -1)
}

function put_like(id_video) {
    like_request(id_video, url_put_like, 'Убрать лайк', `remove_like('${id_video}');`, 1)

}

function like_request(id_video, url_, text_bth, onclick, num) {
    let xhr = new XMLHttpRequest();

    let url = new URL(url_);
    url.searchParams.set('id_video', id_video);

    xhr.open("GET", url)
    xhr.send()

    xhr.onload = function() {
        if (xhr.status == 100) { //Насчёт номера ошибки ещё подумаем
            alert(`Подписка уже оформлена ${xhr.status}: ${xhr.statusText}`);
            }
        else if (xhr.status != 200) {
            alert(`Ошибка ${xhr.status}: ${xhr.response}`);
        }
        else {
            let count_likes = document.getElementById('count_likes')
            count = count_likes.innerHTML
            console.log(typeof(num))
            count_likes.innerHTML = Number(count) + num
            let bth = document.querySelector('.bth-like');
            bth.setAttribute("onclick", onclick)
            bth.innerHTML = text_bth;
            bth.classList.toggle("bth-remove_like");
            bth.classList.toggle("bth-put_like");
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
}


function unsubscribe(id_maker) {
    sub_request(id_maker, url_unsub, 'Подписаться',`subscribe(${id_maker});`, '.bth-unsub' )
}

function subscribe(id_maker) {
    sub_request(id_maker, url_sub, 'Отписаться',`unsubscribe(${id_maker});`, '.bth-sub' )
}

function sub_request(id_maker, url_, text_bth, onclick, selector) {
    let xhr = new XMLHttpRequest();

    let url = new URL(url_);
    url.searchParams.set('id_maker', id_maker);

    xhr.open("GET", url)
    xhr.send()

    xhr.onload = function() {
        if (xhr.status == 100) { //Насчёт номера ошибки ещё подумаем
            alert(`Подписка уже оформлена ${xhr.status}: ${xhr.statusText}`);
            }
        else if (xhr.status != 200) {
            alert(`Ошибка ${xhr.status}: ${xhr.response}`);
        }
        else {
            let bth = document.querySelector(selector);
            bth.setAttribute("onclick", onclick)
            bth.innerHTML = text_bth;
            bth.classList.toggle("bth-unsub");
            bth.classList.toggle("bth-sub");
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
}

function get_comment(){
    let ul = document.querySelector('.main-comments-list_comm')

    id_video = document.location.href.split('=').slice(-1)


    let xhr = new XMLHttpRequest();

    let url = new URL(urls[0]);
    url.searchParams.set('is_one', true);
    url.searchParams.set('offset', 0);
    url.searchParams.set('id_video', id_video);

    xhr.open("GET", url)
    xhr.send()

    xhr.onload = function() {
        if (xhr.status != 200) { // анализируем HTTP-статус ответа, если статус не 200, то произошла ошибка
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`); // Например, 404: Not Found
        } else { // если всё прошло гладко, выводим результат

            let a = document.querySelector('.main-comments-list_comm')
            a.innerHTML = xhr.response + a.innerHTML
            document.getElementById('text_comment').value = ''
            if (xhr.response.length <= 0){
                alert('Комментариев больше нет')
            }
          // вызов функции
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
}

function more(){

    let ul = document.querySelector('.main-comments-list_comm')
    let offset = ul.childElementCount

    id_video = document.location.href.split('=').slice(-1)


    let xhr = new XMLHttpRequest();

    let url = new URL(urls[0]);
    url.searchParams.set('is_one', false);
    url.searchParams.set('offset', offset);
    url.searchParams.set('id_video', id_video);

    xhr.open("GET", url)
    xhr.send()

    xhr.onload = function() {
        if (xhr.status != 200) { // анализируем HTTP-статус ответа, если статус не 200, то произошла ошибка
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`); // Например, 404: Not Found
        } else { // если всё прошло гладко, выводим результат

            let a = document.querySelector('.main-comments-list_comm')
            a.innerHTML += xhr.response
            if (xhr.response.length <= 0){
                alert('Комментариев больше нет')
            }
          // вызов функции
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
    }