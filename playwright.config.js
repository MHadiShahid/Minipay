const { defineConfig, devices } = require("@playwright/test");

module.exports = defineConfig({
    testDir: "./tests/ui",

    timeout: 30000,

    expect: {
        timeout: 5000
    },

    fullyParallel: false,

    reporter: "html",

    use: {
        baseURL: "http://127.0.0.1:5500",
        browserName: "chromium",
        headless: true,
        screenshot: "only-on-failure",
        trace: "retain-on-failure"
    },

    projects: [
        {
            name: "chromium",
            use: {
                ...devices["Desktop Chrome"]
            }
        }
    ]
});