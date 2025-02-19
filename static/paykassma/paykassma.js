(function FleioStripe() {
    "use strict";
    document.addEventListener("DOMContentLoaded", function () {
        showPaykassma();
    });

    async function showPaykassma() {
        var paymentSystems = JSON.parse(document.body.getAttribute('data-js-vars'));
        var invoice_amount = Number(document.getElementById('invoice_amount').value.split(" ")[0])
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
            }
            currencySelect.appendChild(option);
        });

        currencySelect.addEventListener("change", async function () {
            let selectedCurrencyId = this.value;
            let selectedCurrency = paymentSystems?.payments.find(item => item.currency_id === selectedCurrencyId);
            
            if (selectedCurrency) {
                await updateCurrencyRate(selectedCurrency.currency_id, invoice_amount);
            }
        });
        let defaultCurrencyId = currencySelect.value;
        let defaultCurrency = paymentSystems?.payments.find(item => item.currency_id === defaultCurrencyId);
        
        if (defaultCurrency) {
            await updateCurrencyRate(defaultCurrency.currency_id, invoice_amount);
        }
    }

    async function updateCurrencyRate(currencyCode, amount) {
        try {
            let response = await fetch("https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/eur.json");
            let data = await response.json();

            if (data.eur && data.eur[currencyCode.toLowerCase()]) {
                let rate = data.eur[currencyCode.toLowerCase()];
                console.log(amount * rate)
                document.getElementById("converted_value").value = parseFloat(amount * rate).toFixed(2);
            } else {
                document.getElementById("converted_value").value = "Exchange rate not available.";
            }
        } catch (error) {
            console.error("Error fetching currency rates:", error);
            document.getElementById("converted_value").textContent = "Error fetching rates.";
        }
    }
})();