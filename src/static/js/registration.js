function handleFormSubmit(event) {
  event.preventDefault()
  var fields = new FormData(form)
  fields.append("name", "string")
  fields.append("is_active", "true")
  fields.append("is_superuser", "false")
  fields.append("is_verified", "false")
  registr(fields)
}

let form = document.getElementById('form')
form.addEventListener('submit', handleFormSubmit)

function registr(data){

    let xhr = new XMLHttpRequest();
    let url = new URL(url_reg);


    xhr.open("POST", url)
    xhr.setRequestHeader("Content-Type", "application/json")

    console.log(JSON.stringify(Object.fromEntries(data)))

    xhr.send(JSON.stringify(Object.fromEntries(data)))

    xhr.onload = function() {
        if (xhr.status == 200 | xhr.status == 201) {
            alert('Регистриация прошла успешно')
            history.go(-1)

        } else {
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        }
      };

      xhr.onerror = function() {
        alert("Попробуйте позже");
      };
  }