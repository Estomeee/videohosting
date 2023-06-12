
let urls = ['http://127.0.0.1:8000/page/user/videos']

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