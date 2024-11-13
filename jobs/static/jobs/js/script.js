document.addEventListener("DOMContentLoaded", () => {

    setupShowProfiles();
    setupCountryStateCity();
    setupPhones();
    setupDeleteCompanyButtons();
    setupSaveVacancy();
    setupSelectCountryCompany()

})

// Tools
function closeMessage(element) {
    var alertBox = element.parentElement;
    alertBox.remove();
}

function setupCountryStateCity() {
    const country = document.querySelector("#country");
    const state = document.querySelector("#state");
    const city = document.querySelector("#city");
    const selectState = document.querySelector(".select-state");
    const selectCity = document.querySelector(".select-city");


    if (country) {

        populateCoutriesSelect();
        selectState.disabled = true;
        selectCity.disabled = true;

        country.addEventListener("change", function () {
            const countryCodeComplete = this.value;
            const countryCodeSplit = countryCodeComplete.split(":")
            const countryCode = countryCodeSplit[0]

            selectState.innerHTML = '<option value="">Selecione um Estado</option>';
            selectCity.innerHTML = '<option value="">Aguardando Estado</option>';
            selectCity.disabled = true;

            if (countryCode) {
                populateStates(countryCode);

            } else {
                selectState.disabled = true
                selectCity.disabled = true
            }

            state.addEventListener("change", function () {
                const stateCodeComplete = this.value;
                const stateCodeSplit = stateCodeComplete.split(":");
                const stateCode = stateCodeSplit[0];

                selectCity.innerHTML = '<option value="">Escolha uma Cidade</option>';
                selectCity.disabled = false;

                if (stateCode) {
                    populateCities(countryCode, stateCode);
                }
            })

        })


    }
}


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
};

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
};
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
// Profiles
function setupShowProfiles() {
    const buttonWorker = document.querySelector("#show-worker-profile");
    const buttonCompanies = document.querySelector("#show-company-profile");
    const buttonsShowCompany = document.querySelectorAll(".button-company");
    const workerProfile = document.querySelector(".worker-profile");
    const companyProfile = document.querySelector(".company-profile");

    if (buttonWorker && buttonCompanies && workerProfile && companyProfile) {
        buttonWorker.addEventListener("click", () => toogleProfiles(workerProfile, companyProfile, buttonWorker, buttonCompanies));
        buttonCompanies.addEventListener("click", () => toogleProfiles(companyProfile, workerProfile, buttonCompanies, buttonWorker));
    }

    if (buttonsShowCompany) {
        buttonsShowCompany.forEach(button => {
            const buttonId = button.id;
            button.addEventListener("click", (event) => showCompany(buttonId, event))
        })
    }
}

function toogleProfiles(showDiv, hideDiv, activeButton, inactiveButton) {
    showDiv.hidden = false;
    hideDiv.hidden = true;
    activeButton.classList.replace("btn-outline-primary", "btn-primary");
    inactiveButton.classList.replace("btn-primary", "btn-outline-primary");
}


function showCompany(button_id, event = none) {

    const button = event.target;


    let button_company = document.querySelectorAll(".button-company");


    button_company.forEach(btn => {
        if (btn.classList.contains("btn-success")) {
            btn.classList.replace("btn-success", "btn-outline-success");
        }
    });

    // Altera a classe do botão clicado para 'btn-success'
    if (button.classList.contains("btn-outline-success")) {
        button.classList.replace("btn-outline-success", "btn-success");
    }


    let div_companies = document.querySelectorAll(".company > div");
    let h2_companies = document.querySelectorAll(".company > h2");

    div_companies.forEach(div => div.hidden = true);


    let button_id_split = button_id.split("-");
    let id = `${button_id_split[1]}-${button_id_split[2]}`;

    h2_companies.forEach(h2 => h2.hidden = false);
    company = document.querySelector(`#${id}`);
    company.hidden = false;
    company.scrollIntoView({ behavior: "smooth", block: "center" });

}

// Phones

function setupPhones() {
    const phone1 = document.querySelector("#phone1");
    const phone2 = document.querySelector("#phone2");
    const phones = document.querySelectorAll(".phone");
    const addPhone1 = document.querySelector("#add-phone1");
    const addPhone2 = document.querySelector("#add-phone2");
    const country = document.querySelector("#country");
    let countryCode = "";

    if (country) {
        country.addEventListener("change", function (event) {
            const countryComplete = this.value;
            const countrySplit = countryComplete.split(":");

            countryCode = countrySplit[2];

            phoneCountryCode(countryCode, phone1);
            phoneCountryCode(countryCode, phone2);


        });
        addPhone1.addEventListener("change", function (event) {

        if (this.checked) {

            phone1.hidden = false;
            if (countryCode) {
                phoneCodeChoice = phoneCountryCode(countryCode, phone1);
            } else {
                phoneCodeChoice = phoneCountryCode("00", phone1);
            }

        } else {
            phone1.hidden = true;

            phone1.value = "";
        }

    })

    addPhone2.addEventListener("change", function (event) {
        if (this.checked) {

            phone2.hidden = false;
            if (countryCode) {

                phoneCodeChoice = phoneCountryCode(countryCode, phone2);
            } else {
                phoneCodeChoice = phoneCountryCode("00", phone2);
            }


        } else {
            phone2.hidden = true;
            phone2.value = "";

        }

    })

    phones.forEach(phone => {
        phone.addEventListener("input", (event) => handlePhone(event, countryCode));
    });
    }






}

function phoneCountryCode(phoneCode, phoneElement) {

    let cleaned = phoneCode.split('-')[0].replace(/[^0-9]/g, "");
    phoneElement.value = `+${cleaned}`;


}

function phoneCountryCodeCleaned(phoneCode) {

    var cleaned = phoneCode.replace(/-.*$/, "").replace(/[^0-9]/g, "");

    return cleaned
}

function handlePhone(event, countryCode) {
    let input = event.target;
    input.value = phoneMask(input.value, countryCode)


}

function phoneMask(value, countryCode) {
    if (!value) return "";



    let phoneCodeSplit = countryCode;

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

function setupDeleteCompanyButtons() {
    const deleteButtons = document.querySelectorAll(".delete-company");
    deleteButtons.forEach(button =>
        button.addEventListener("click", deleteCompany));

}

function deleteCompany(event) {
    const companyId = event.target.dataset.id;
    const companyName = event.target.dataset.name;

    const confirm1 = prompt(`\nDeseja excluir a empresa ${companyName}?\n\nSuas vagas serão excluidas. \n\nDigite: \ndelete ${companyName.toLowerCase()}`);


    if (confirm1 === `delete ${companyName.toLowerCase()}`) {
        const confirm2 = confirm("\nNão é possivel reverter essa opção. Continuar?");
        if (confirm2 === true) {
            const csrfToken = getCSRFToken();
            fetch(`/delete_company/${companyId}`, {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json"
                }
            })
                .then(response => {
                    console.log(response);
                    return response.json();
                })
                .then(data => {

                    // alert(`A empresa ${companyName} foi excluida com sucesso.`);
                    window.location.reload();


                })
                .catch(error => {
                    window.location.reload();
                })

        } else {
            event.preventDefault();
        }


    }
    else if (confirm1 === null) {

        event.preventDefault();
    } else {

        const errorConfirm = confirm("\nPara deletar a empresa digite o texto corretamente.\nClique em 'OK' para continuar ou Cancelar.");
        if (errorConfirm === true) {
            deleteCompany(event);
        } else {
            event.preventDefault();
        }
    }

}

function activeVacancy(event) {
    const button = event.target;
    const vacancy_id = button.getAttribute('data-id');
    const csrf_token = getCSRFToken();

    fetch(`/active_vacancy/${vacancy_id}`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrf_token,
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(data => {
            window.location.reload();
        })
}

function setupSaveVacancy() {
    const save_buttons = document.querySelectorAll(".save-toggle");
    save_buttons.forEach(button => {
        button.addEventListener("click", (event) => SaveVacancy(event));
    })
}

async function SaveVacancy(event) {
    const vacancyButton = event.target
    const vacancy_id = vacancyButton.getAttribute("data-id");
    const csrf_token = getCSRFToken();

    try{
        const response = await fetch(`/save_vacancy/${vacancy_id}`, {
            method: 'POST',
            headers: {
                "X-CSRFToken": csrf_token,
                "Content-Type": "application/json"
            }
        });

        if (!response.ok){
            throw new Error(`Erro de rede ${response.status}`)
        }

        const data = await response.json();
        

        if (data.status === 'saved') {
            vacancyButton.classList.remove('btn-outline-success');
            vacancyButton.classList.add('btn-success');
            vacancyButton.textContent = 'Desmarcar Vaga';
        } else {
            vacancyButton.classList.remove('btn-success');
            vacancyButton.classList.add('btn-outline-success');
            vacancyButton.textContent = 'Salvar Vaga';
        }
        

        window.location.reload();

    }catch (error) {
        console.error('Erro:', error);
    }
    
}

function setupSelectCountryCompany(){
    const select_company = document.querySelector("#company");
    if (select_company) {
        select_company.addEventListener("click", () => {

            select_company.addEventListener("change", (event) => selectCountryCompany(event));
        });
    }

}

function selectCountryCompany(event) { 
    const select_company = event.target;
    const selectedOption = select_company.options[select_company.selectedIndex];

    const country = selectedOption.dataset.country;
    const [countryCode, countryName, countryPhoneCode] = country.split(":");

    const state = selectedOption.dataset.state;
    const [stateCode, stateName] = state.split(":");
    const city = selectedOption.dataset.city;

    const select_country = document.querySelector("#country");
    const option_country = document.createElement("option");
    option_country.value = country;
    option_country.innerHTML = countryName;
    option_country.selected = true;
    select_country.appendChild(option_country);

    const select_state = document.querySelector("#state");
    const option_state = document.createElement("option");
    option_state.value = state;
    option_state.innerHTML = stateName;
    option_state.selected = true;
    select_state.appendChild(option_state);

    const select_city = document.querySelector("#city");
    const option_city = document.createElement("option");
    option_city.value = city;
    option_city.innerHTML = city;
    option_city.selected = true;
    select_city.appendChild(option_city);
 }