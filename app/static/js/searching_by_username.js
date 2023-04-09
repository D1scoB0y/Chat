const search_field = document.getElementById('search-input');
const sr_block = document.getElementById('sr-block');
const cur_user_username = document.getElementById('main-username').value;

const url = '/api/search/';



function getNames(url, search_data) {
    return fetch(url + search_data, {method:'GET'})
}


search_field.oninput = function () {

    if (search_field.value != ''){

        getNames(url, search_field.value)
        .then(responce => responce.json())
        .then(data => {

            console.log(data['data'])
            console.log(data['data'].length)

            if (data['data'].length > 0){

                sr_block.innerHTML = ``;

                var data = data['data'];
            
                data.forEach(el => {
                    sr_block.innerHTML += `<a class='sr-href' href='http://127.0.0.1:5000/create_chat_room/${el}'><div class='search-result'>${el}</div></a>`;
                });

                sr_block.classList.add('sr-visible');

            } else { 
                sr_block.innerHTML = `<div class='search-result'>No matches</div>`;
                sr_block.classList.add('sr-visible');
            }
        });

    } else {
        sr_block.classList.remove('sr-visible');
        sr_block.innerHTML = ``;
    }
}
