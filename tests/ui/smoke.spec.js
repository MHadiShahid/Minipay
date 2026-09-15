const { test, expect } = require("@playwright/test");

test.describe("MiniPay Support Console", () => {

    test.beforeEach(async ({ page }) => {
        await page.goto("/");
        await expect(page.getByTestId("api-status")).toHaveText("API Online");
    });

    test("loads the support console", async ({ page }) => {
        await expect(page).toHaveTitle("MiniPay Support Console");
        await expect(
            page.getByRole("heading", { name: "MiniPay Support Console" })
        ).toBeVisible();
    });

    test("looks up an existing customer", async ({ page }) => {
        await page.getByTestId("customer-id").fill("1");
        await page.getByTestId("customer-search").click();

        const result = page.getByTestId("customer-result");

        await expect(result).toBeVisible();
        await expect(result).toContainText('"id": 1');
    });

    test("returns an error for an unknown customer", async ({ page }) => {
        await page.getByTestId("customer-id").fill("999999");
        await page.getByTestId("customer-search").click();

        const result = page.getByTestId("customer-result");

        await expect(result).toBeVisible();
        await expect(result).toHaveClass(/error/);
        await expect(result).toContainText("Customer not found");
    });

    test("creates a payment", async ({ page }) => {
        const transactionRef = `UI-TEST-${Date.now()}`;

        await page.getByTestId("transaction-ref").fill(transactionRef);
        await page.getByTestId("payment-customer-id").fill("1");
        await page.getByTestId("payment-amount").fill("100");
        await page.getByTestId("create-payment").click();

        const result = page.getByTestId("payment-result");

        await expect(result).toBeVisible();
        await expect(result).toContainText(transactionRef);
        await expect(result).toContainText("PROCESSING");
    });

    test("looks up an existing payment", async ({ page }) => {
        await page.getByTestId("payment-id").fill("50006");
        await page.getByTestId("payment-search").click();

        const result = page.getByTestId("payment-lookup-result");

        await expect(result).toBeVisible();
        await expect(result).toContainText('"id": 50006');
    });

    test("shows an error for an unknown payment", async ({ page }) => {
        await page.getByTestId("payment-id").fill("999999");
        await page.getByTestId("payment-search").click();

        const result = page.getByTestId("payment-lookup-result");

        await expect(result).toBeVisible();
        await expect(result).toHaveClass(/error/);
        await expect(result).toContainText("Payment not found");
    });

    test("loads customer payment history", async ({ page }) => {
        await page.getByTestId("payments-customer-id").fill("1");
        await page.getByTestId("payments-search").click();

        const result = page.getByTestId("payments-result");

        await expect(result).toBeVisible();
        await expect(result).toContainText("transaction_ref");
    });
});