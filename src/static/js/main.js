
let urls = ['http://127.0.0.1:8000/page/my_video', 'http://127.0.0.1:8000/page/hstory', 'http://127.0.0.1:8000/page/liked_video' ]

function get_more(){

    let xhr = new XMLHttpRequest();

    let ul = document.querySelector('.main-list_video')
    let offset = ul.childElementCount

    let url = new URL('http://127.0.0.1:8000/page/main/more');
    url.searchParams.set('offset', offset);

    xhr.open("GET", url)
    xhr.send()

    xhr.onload = function() {
        if (xhr.status != 200) { // анализируем HTTP-статус ответа, если статус не 200, то произошла ошибка
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`); // Например, 404: Not Found
        } else { // если всё прошло гладко, выводим результат

            let a = document.querySelector('.main-list_video')
            a.innerHTML += xhr.response
          // вызов функции
          if (xhr.response.length <= 0){
                alert('Видео больше нет')
            }
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
  }