document.addEventListener("DOMContentLoaded", (event) => {

    // template profiles.html
    const button_show_worker = document.querySelector("#show-worker-profile");
    const button_show_company = document.querySelector("#show-company-profile");
    const div_worker_profile = document.querySelector(".worker-profile");
    const div_company_profile = document.querySelector(".company-profile");
    const countrySelect = document.querySelector(".select-country");

    if (button_show_worker && button_show_company && div_worker_profile && div_company_profile) {
        button_show_worker.addEventListener("click", function () {
            div_company_profile.hidden = true;
            div_worker_profile.hidden = false;
        });

        button_show_company.addEventListener("click", function () {
            div_worker_profile.hidden = true;
            div_company_profile.hidden = false;
        });
    } else {
        console.error("Um ou mais elementos não foram encontrados.");
    }


    populateCoutriesSelect();

    button_company = document.querySelectorAll(".button-company");


    button_company.forEach(button => {
        const button_id = button.id;
        button.addEventListener("click", () => showCompany(button_id))
    })

    var phones = document.querySelectorAll(".phone");
    phones.forEach(phone => {
        phone.addEventListener("input", handlePhone)
    })


    const phone1 = document.querySelectorAll("#phone1");
    const phone2 = document.querySelectorAll("#phone2");

    const save_buttons = document.querySelectorAll(".save-toggle");

    

    save_buttons.forEach(button => {
        button.addEventListener("click", function () {
            const vacancy_id = button.getAttribute("data-id");
            const csrf_token = getCSRFToken();

            fetch(`/save_vacancy/${vacancy_id}`, {
                method: 'POST',
                headers: {
                    "X-CSRFToken": csrf_token,
                    "Content-Type": "application/json"
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'saved') {
                        button.classList.remove('btn-outline-success');
                        button.classList.add('btn-success');
                        button.textContent = 'Desmarcar Vaga';
                    } else {
                        button.classList.remove('btn-success');
                        button.classList.add('btn-outline-success');
                        button.textContent = 'Salvar Vaga';
                    }
                    window.location.reload();
                })
                .catch(error => console.error('Erro:', error));
        })

    });
});

function populateCoutriesSelect() {
    fetch("/get_countries/")
        .then(response => response.json())
        .then(data => {

            const countrySelect = document.querySelector(".select-country");
            data.forEach(country => {
                let option = document.createElement("option");
                option.value = `${country.iso2}:${country.name}:${country.phonecode}`;
                option.text = country.name;
                countrySelect.appendChild(option)
            });
        })
        .catch(error => console.log('Error', error));
}

function populateStates(countryCode) {
    fetch(`/get_states/${countryCode}`)
        .then(response => response.json())
        .then(data => {

            const stateSelect = document.querySelector(".select-state");

            if (data.length === 0) {
                let option = document.createElement("option");
                let countryCodeComplete = document.querySelector(".select-country").value
                let countryCodeSplit = countryCodeComplete.split(":")


                option.value = countryCodeComplete
                option.textContent = countryCodeSplit[1];
                stateSelect.appendChild(option);
            }
            else {
                data.forEach(state => {
                    let option = document.createElement("option");
                    option.value = `${state.iso2}:${state.name}`
                    option.textContent = state.name;
                    stateSelect.appendChild(option);

                });
            }
            stateSelect.disabled = false;
        })
}

var phoneCodeChoice = ""
function populateCities(countryCode, stateCode) {
    fetch(`/get_cities/${countryCode}/${stateCode}`)
        .then(response => response.json())
        .then(data => {
            const citySelect = document.querySelector(".select-city");
            citySelect.innerHTML = "";

            if (data.length === 0) {
                let stateCountryCode = document.querySelector(".select-state").value
                let stateCountryCodeSplit = stateCountryCode.split(":");

                let option = document.createElement("option");

                option.value = stateCountryCodeSplit[1];
                option.text = stateCountryCodeSplit[1];
                citySelect.appendChild(option);
            } else {
                data.forEach(city => {
                    let option = document.createElement('option')
                    option.value = city.name;
                    option.text = city.name;

                    citySelect.appendChild(option);
                })


            }
            citySelect.disabled = false;
        })
};

document.querySelector(".select-country").addEventListener("change", function () {

    const countryCodeComplete = this.value;
    const countryCodeSplit = countryCodeComplete.split(":")
    const countryCode = countryCodeSplit[0]

    document.querySelector(".select-state").innerHTML = '<option value="">Selecione um Estado</option>';
    document.querySelector(".select-city").innerHTML = '<option value="">Aguardando Estado</option>';
    document.querySelector(".select-city").disabled = true;
    if (countryCode) {

        populateStates(countryCode);

        document.querySelector(".select-city").disabled = true;

        phoneCodeChoice = phoneCountryCode(countryCodeSplit[2])



    } else {
        document.querySelector(".select-state").disabled = true;

        document.querySelector(".select-city").disabled = true;

    }


})



document.querySelector(".select-state").addEventListener("change", function () {

    const countryCodeComplete = document.querySelector(".select-country").value;
    const countryCodeSplit = countryCodeComplete.split(":")
    const countryCode = countryCodeSplit[0]

    const stateCodeComplete = this.value;
    const stateCodeSplit = stateCodeComplete.split(":");
    const stateCode = stateCodeSplit[0]
    const selectCity = document.querySelector(".select-city");

    selectCity.innerHTML = '<option value="">Escolha uma Cidade</option>';


    if (stateCode && stateCode) {
        populateCities(countryCode, stateCode)

    }


})


function closeMessage(element) {
    var alertBox = element.parentElement;
    alertBox.remove();
}

function showCompany(button_id) {

    let div_companies = document.querySelectorAll(".company > div");
    let h2_companies = document.querySelectorAll(".company > h2");

    div_companies.forEach(div => div.hidden = true);


    let button_id_split = button_id.split("-");
    let id = `${button_id_split[1]}-${button_id_split[2]}`;

    h2_companies.forEach(h2 => h2.hidden = false);
    company = document.querySelector(`#${id}`);
    company.hidden = false;


}


function phoneCountryCode(phoneCode) {
    var phones = document.querySelectorAll(".phone");

    phones.forEach(phone => {
        var cleaned = phoneCode.replace(/-.*$/, "").replace(/[^0-9]/g, "");
        phone.value = `+${cleaned}`;


    })
}

function phoneCountryCodeCleaned(phoneCode) {

    var cleaned = phoneCode.replace(/-.*$/, "").replace(/[^0-9]/g, "");

    return cleaned
}
const handlePhone = (event) => {

    let input = event.target;
    input.value = phoneMask(input.value)
}

const phoneMask = (value) => {
    if (!value) return "";
    let phoneCode = document.querySelector(".select-country").value;

    // Extrai o código do país
    let phoneCodeSplit = phoneCountryCodeCleaned(phoneCode.split(":")[2]);

    // Remove todos os caracteres não numéricos do valor
    value = value.replace(/\D/g, '');

    // Adiciona o código de país se ele não estiver presente no início
    if (!value.startsWith(phoneCodeSplit)) {
        value = `${phoneCodeSplit}${value}`;
    }

    // Formatação inicial: +ddi(ddd)
    value = `+${value}`;
    value = value.replace(new RegExp(`(\\+${phoneCodeSplit})(\\d{2})(\\d)`), "$1($2) $3");

    // Limitar ao formato de 8 ou 9 dígitos finais
    if (value.match(/\d{9}$/)) {
        // Formato com 9 dígitos (9 9999-9999)
        value = value.replace(/(\d{1})(\d{4})(\d{4})$/, "$1 $2-$3");
    } else {
        // Formato com 8 dígitos (9999-9999)
        value = value.replace(/(\d{4})(\d{4})$/, "$1-$2");
    }

    // Limite o comprimento para evitar qualquer caractere extra
    if (value.length > `+${phoneCodeSplit} (00) 0 0000-0000`.length) {
        value = value.slice(0, `+${phoneCodeSplit} (00) 0 0000-0000`.length);
    }

    return value;
}


document.querySelector("#add-phone1").addEventListener("change", function (event) {

    if (this.checked) {

        phone1.hidden = false;

    } else {
        phone1.hidden = true;

    }

})

document.querySelector("#add-phone2").addEventListener("change", function (event) {
    if (this.checked) {

        phone2.hidden = false;

    } else {
        phone2.hidden = true;

    }

})

function getCSRFToken() {
    let csrfToken = null;
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            csrfToken = value;
            break;
        }
    }
    return csrfToken;

}