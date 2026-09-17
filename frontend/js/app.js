const API_BASE_URL = "http://127.0.0.1:8000";
const API_KEY = "minipay-test-key";

async function apiRequest(path, options = {}) {
    const requestOptions = {
        ...options,
        headers: {
            ...(options.headers || {}),
            "X-API-Key": API_KEY
        }
    };

    const response = await fetch(
        `${API_BASE_URL}${path}`,
        requestOptions
    );

    let data = null;

    try {
        data = await response.json();
    } catch {
        data = null;
    }

    if (!response.ok) {
        const message = data?.detail || `Request failed with status ${response.status}`;
        throw new Error(message);
    }

    return data;
}

function showResult(elementId, message, type = "success") {
    const element = document.getElementById(elementId);

    element.textContent = message;
    element.className = `result ${type}`;
}

function showJsonResult(elementId, data) {
    const element = document.getElementById(elementId);

    element.textContent = JSON.stringify(data, null, 2);
    element.className = "result success";
}

async function checkApiHealth() {
    const statusElement = document.getElementById("api-status");

    try {
        const data = await apiRequest("/health");

        if (data.status === "ok") {
            statusElement.textContent = "API Online";
        } else {
            statusElement.textContent = "Database Unavailable";
        }
    } catch {
        statusElement.textContent = "API Offline";
    }
}

document
    .getElementById("customer-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const customerId = document.getElementById("customer-id").value;

        try {
            const customer = await apiRequest(
                `/api/customers/${customerId}`
            );

            showJsonResult("customer-result", customer);
        } catch (error) {
            showResult("customer-result", error.message, "error");
        }
    });

document
    .getElementById("payment-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const transactionRef =
            document.getElementById("transaction-ref").value;

        const customerId =
            Number(document.getElementById("payment-customer-id").value);

        const amount =
            Number(document.getElementById("payment-amount").value);

        try {
            const payment = await apiRequest("/api/payments", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    transaction_ref: transactionRef,
                    customer_id: customerId,
                    amount: amount
                })
            });

            showJsonResult("payment-result", payment);
        } catch (error) {
            showResult("payment-result", error.message, "error");
        }
    });

document
    .getElementById("payment-lookup-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const paymentId = document.getElementById("payment-id").value;

        try {
            const payment = await apiRequest(
                `/api/payments/${paymentId}`
            );

            showJsonResult("payment-lookup-result", payment);
        } catch (error) {
            showResult("payment-lookup-result", error.message, "error");
        }
    });

document
    .getElementById("customer-payments-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const customerId =
            document.getElementById("payments-customer-id").value;

        try {
            const payments = await apiRequest(
                `/api/customers/${customerId}/payments`
            );

            showJsonResult("payments-result", payments);
        } catch (error) {
            showResult("payments-result", error.message, "error");
        }
    });

checkApiHealth();