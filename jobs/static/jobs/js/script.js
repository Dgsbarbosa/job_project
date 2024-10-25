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

});

function populateCoutriesSelect() {
    fetch("/get_countries/")
        .then(response => response.json())
        .then(data => {

            const countrySelect = document.querySelector(".select-country");
            data.forEach(country => {
                let option = document.createElement("option");
                option.value = `${country.iso2}:${country.name}`;
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
