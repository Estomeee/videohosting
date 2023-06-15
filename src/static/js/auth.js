function handleFormSubmit(event) {
  event.preventDefault()
  var fields = new FormData(form)

  auth(fields)
}

let form = document.getElementById('form')
form.addEventListener('submit', handleFormSubmit)

function auth(data){

    let xhr = new XMLHttpRequest();
    let url = new URL(url_login);
    url.searchParams.set('title', 'Form');
    url.searchParams.set('description', 'Form');

    xhr.open("POST", url)


    xhr.send(data)

    xhr.onload = function() {
        if (xhr.status == 200 | xhr.status == 204) {
            alert('Авторизация прошла успешно')
            window.location.href = url_main;

        } else {
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
  }