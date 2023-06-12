
let urls = ['http://127.0.0.1:8000/page/video_page/comments']

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

function more(){

    let ul = document.querySelector('.main-comments-list_comm')
    let offset = ul.childElementCount

    id_video = document.location.href.split('=').slice(-1)


    let xhr = new XMLHttpRequest();

    let url = new URL(urls[0]);
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