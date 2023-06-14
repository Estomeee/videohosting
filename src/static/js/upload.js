url_upload = 'http://127.0.0.1:8000/video/protected-route/load'

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
  upload(fields)
}

let form = document.getElementById('form')
form.addEventListener('submit', handleFormSubmit)

function upload(data){

    let xhr = new XMLHttpRequest();
    let url = new URL(url_upload);
    url.searchParams.set('title', 'Form');
    url.searchParams.set('description', 'Form');

    xhr.open("POST", url)


    xhr.send(data)

    xhr.onload = function() {
        if (xhr.status != 200) {
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            alert('Успех, на!')
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
  }