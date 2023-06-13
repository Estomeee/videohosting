
let urls = ['http://127.0.0.1:8000/page/user/videos']
url_sub = 'http://127.0.0.1:8000/interactions/protected-route/subscribe'
url_unsub = 'http://127.0.0.1:8000/interactions/protected-route/unsubscribe'

function more(await_count, num){
    //Получаем кол-во отображённых видео - offset
    let ul = document.querySelector('.main-list_video')
    let offset = ul.childElementCount
    //Получаем id_user
    id_user = document.location.href.split('=').slice(-1)

    let xhr = new XMLHttpRequest();

    let url = new URL(urls[num]);
    url.searchParams.set('offset', offset);
    url.searchParams.set('id_user', id_user);

    xhr.open("GET", url)
    xhr.send()

    xhr.onload = function() {
        if (xhr.status != 200) { // анализируем HTTP-статус ответа, если статус не 200, то произошла ошибка
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`); // Например, 404: Not Found
        } else { // если всё прошло гладко, выводим результат

            let a = document.querySelector('.main-list_video')
            a.innerHTML += xhr.response
            if (xhr.response.length <= 0){
                alert('Видео больше нет')
            }
          // вызов функции
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
    }

function unsubscribe(id_maker) {
    sub_request(id_maker, url_unsub, 'Подписаться',`subscribe(${id_maker});`, '.bth-unsub', -1 )
}

function subscribe(id_maker) {
    sub_request(id_maker, url_sub, 'Отписаться',`unsubscribe(${id_maker});`, '.bth-sub', 1 )
}

function sub_request(id_maker, url_, text_bth, onclick, selector, num) {
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

            count_subs = document.getElementById('count_subs')
            count_subs.innerHTML = Number(count_subs.innerHTML) + num
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
}