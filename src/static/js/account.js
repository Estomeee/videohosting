
let urls = ['http://127.0.0.1:8000/page/account/my_video',
            'http://127.0.0.1:8000/page/account/history',
            'http://127.0.0.1:8000/page/account/liked_video']

function action(num, id){

    let xhr = new XMLHttpRequest();
    let url = new URL(urls[num]);
    url.searchParams.set('offset', 0);
    xhr.open("GET", url)

    xhr.send()

    xhr.onload = function() {
        if (xhr.status != 200) { // анализируем HTTP-статус ответа, если статус не 200, то произошла ошибка
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`); // Например, 404: Not Found
        } else { // если всё прошло гладко, выводим результат

            let bth = document.querySelector('.bth-more');
            bth.setAttribute('name', num);

            let active_bth = document.querySelector('.active');
            active_bth.classList.toggle("active");

            active_bth = document.getElementById(id);
            console.log(id);
            console.log('sdfdsf')
            console.log(active_bth.classList);

            active_bth.classList.toggle("active");

            let ul = document.querySelector('.main-list_video');
            ul.innerHTML = xhr.response;
          // вызов функции
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
  }

function more(await_count, num){

    let ul = document.querySelector('.main-list_video')
    let offset = ul.childElementCount

    let xhr = new XMLHttpRequest();

    let url = new URL(urls[num]);
    url.searchParams.set('offset', offset);

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