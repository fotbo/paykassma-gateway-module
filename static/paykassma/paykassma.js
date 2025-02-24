(function FleioStripe() {
    "use strict";
    document.addEventListener("DOMContentLoaded", function () {
        showPaykassma();
    });

    function showPaykassma() {
        var paymentSystems = JSON.parse(document.body.getAttribute('data-js-vars'));
        var invoice_amount = Number(document.getElementById('invoice_amount').value.split(" ")[0]);
        var exchangeRates = JSON.parse(document.body.getAttribute('data-currensies-rate')); // Оновлено отримання курсів валют
        var currencySelect = document.getElementById("currency");
    
        if (!currencySelect) {
            console.error("Select element not found!");
            return;
        }
    
        currencySelect.innerHTML = '';
        paymentSystems?.payments.forEach(item => {
            let option = document.createElement("option");
            option.value = item.currency_id;
            option.textContent = item.currency_name;
            if (item.currency_name === "Rupee") {
                option.selected = true;
                updateCurrencyRate(item.currency_id, invoice_amount, exchangeRates);
            }
            currencySelect.appendChild(option);
        });
    
        currencySelect.addEventListener("change", async function () {
            let selectedCurrency = currencySelect.value;
            if (selectedCurrency) {
                updateCurrencyRate(selectedCurrency, invoice_amount, exchangeRates);
            }
        });
    
        let defaultCurrency = currencySelect.value;
        if (defaultCurrency) {
            updateCurrencyRate(defaultCurrency, invoice_amount, exchangeRates);
        }
    }
    
    function updateCurrencyRate(currencyId, amount, rates) {
        var convertedValue = amount * (rates[currencyId] || 1);
        convertedValue += convertedValue * 0.1;
        document.getElementById('converted_value').value = convertedValue.toFixed(2);
    }
})();