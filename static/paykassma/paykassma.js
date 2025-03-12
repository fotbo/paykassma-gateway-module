(function FleioStripe() {
    "use strict";
    document.addEventListener("DOMContentLoaded", function () {
        showPaykassma();
    });

    function showPaykassma() {
        var paymentSystems = JSON.parse(document.body.getAttribute('data-js-vars'));
        var invoice_amount = Number(document.querySelector('#invoice_amount').innerHTML.split(" ")[0]);
        var exchangeRates = JSON.parse(document.body.getAttribute('data-currensies-rate')); // Оновлено отримання курсів валют
        var currencySelect = document.querySelector(".dropdown__select");

        const selected_label = document.querySelector('.dropdown__filter-selected')

        const currencyIpnut = document.querySelector("#currency_input");

    
        if (!currencySelect) {
            console.error("Select element not found!");
            return;
        }
    
        currencySelect.innerHTML = '';
        paymentSystems?.payments.forEach(item => {
            let option = document.createElement("li");
            option.classList.add('dropdown__select-option')
            option.setAttribute('role', 'option')
            option.value = item.currency_id;
            option.textContent = item.currency_name;
            if (item.currency_name === "Rupee") {
                selected_label.textContent = option.textContent
                currencyIpnut.value = item.currency_id
                updateCurrencyRate(item.currency_id, invoice_amount, exchangeRates);
            }
            
            option.addEventListener('click', () => {
                selected_label.textContent = option.textContent
                currencyIpnut.value = item.currency_id
                updateCurrencyRate(item.currency_id, invoice_amount, exchangeRates);
            })

            currencySelect.appendChild(option);
        });
    }
    
    function updateCurrencyRate(currencyId, amount, rates) {
        const convertedValueInput = document.querySelector("#converted_value_input");

        var convertedValue = amount * (rates[currencyId] || 1);
        convertedValue += convertedValue * 0.1;
        
        convertedValueInput.value = convertedValue.toFixed(2)
        document.getElementById('converted_value').innerHTML = convertedValue.toFixed(2);
    }
})();