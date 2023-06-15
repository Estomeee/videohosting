url_upload = 'http://127.0.0.1:8000/auth/login'
let url_main = 'http://127.0.0.1:8000/page/main'

function serializeForm(formNode) {
    var data = new FormData(formNode);
    for (var [key, value] of data) {
    console.log(key, value)
}

}


function handleFormSubmit(event) {
    console.log('dsfsd')
  event.preventDefault()
  var fields = new FormData(form)

  data = serializeForm(form)
  auth(fields)
}

let form = document.getElementById('form')
form.addEventListener('submit', handleFormSubmit)

function auth(data){

    let xhr = new XMLHttpRequest();
    let url = new URL(url_upload);
    url.searchParams.set('title', 'Form');
    url.searchParams.set('description', 'Form');

    xhr.open("POST", url)


    xhr.send(data)

    xhr.onload = function() {
        if (xhr.status == 200 | xhr.status == 204) {
            alert('Успех, на!')
            window.location.href = url_main;

        } else {
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
  }