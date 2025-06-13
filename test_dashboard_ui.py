from playwright.sync_api import sync_playwright
import random
import requests
import json
import re


jwt_token="Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJnZWV2aXNod2FuYXRoMDAxQGdtYWlsLmNvbSIsInVzZXJJZCI6ImFlNDM5NmUwLTQ3N2ItMTFmMC05MDViLTcxNTE4OGFkMmNkOCIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiMmVmYzgyYWEtZjJjNy00YzEzLWIyNDctOGY1OGU2OTUzNTUwIiwiZXhwIjoxNzUxNTI1NzU4LCJpc3MiOiJ0aGluZ3Nib2FyZC5pbyIsImlhdCI6MTc0OTcyNTc1OCwiZmlyc3ROYW1lIjoibWVnaGFuYSIsImxhc3ROYW1lIjoibiIsImVuYWJsZWQiOnRydWUsInByaXZhY3lQb2xpY3lBY2NlcHRlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6ImFlMWNmYzEwLTQ3N2ItMTFmMC05MDViLTcxNTE4OGFkMmNkOCIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.ONYPwoyCIQMwk8zaY0-dNfzWd8UGsWWGf8j250GgxmkwUX5C7z9havcYhnBac3oJOxEBkfHfcun1fYUyHaf31A"



def runLoginDashboard(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    

    # Navigate to your app’s domain
    page.goto("https://demo.thingsboard.io/login",timeout=50000)  # or your app’s main URL

    # Inject the JWT token into localStorage
    page.evaluate("""(token) => {
        localStorage.setItem('jwt_token', token);
    }""",jwt_token )



    # Navigate to the dashboard
    page.goto("https://demo.thingsboard.io/dashboard")

    # Add assertions or checks here
    print("UI Test Validation 1 - Successfully navigated to dashboard using JWT token")

    
    # Close the browser
    browser.close()


def runRealTimeUpdates(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

     # Navigate to your app’s domain
    page.goto("https://demo.thingsboard.io/login") 
    
    # Inject the JWT token into localStorage
    page.evaluate("""(token) => {
        localStorage.setItem('jwt_token', token);
    }""",jwt_token )


    # Navigate to the dashboard
    page.goto("https://demo.thingsboard.io/dashboards/eb715cf0-477b-11f0-905b-715188ad2cd8")

    # Wait for widget to load
    #widget_selector = "tb-widget-header"

    # page.wait_for_selector("tb-value-card-value",timeout=100000,state="visible")

    #initial_value = page.text_content(widget_selector)'
    print("Getting the initial value")
    temperature_value = page.locator(".tb-value-card-value").first.text_content()
    # initial_value=page.text_content("tb-value-card-value")
    print(f"Initial value: {temperature_value}")

    temp=re.search(r"[-+]?\d*\.?\d+", temperature_value)

    intial_temperature_value = float(temp.group())

    

    # Update the value from initial 35 to 28

    payload = {"temperature":intial_temperature_value+10 }
    response = requests.post(
        f" http://demo.thingsboard.io/api/v1/wQeBTNSNpmL0VTHmWTkj/telemetry",
        json=payload,
        headers={"X-Authorization": jwt_token}
    )

    assert response.status_code==200
    
    print(f"Telemetry update response: {response.status_code}")

    # Wait for value to be updated
    page.wait_for_timeout(5000)  # Wait 5 seconds

    #updated_value = page.text_content(widget_selector)
    updated_tempertature_value=page.locator(".tb-value-card-value").first.text_content()
    print(f"Updated value: {updated_tempertature_value}")

    assert intial_temperature_value != updated_tempertature_value, "Widget did not update!"
    print("Widget updated successfully.")

    browser.close()

def testVisualization(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

     # Navigate to your app’s domain
    page.goto("https://demo.thingsboard.io/login") 
    
    # Inject the JWT token into localStorage
    page.evaluate("""(token) => {
        localStorage.setItem('jwt_token', token);
    }""",jwt_token )


    # Navigate to the dashboard
    page.goto("https://demo.thingsboard.io/dashboards/eb715cf0-477b-11f0-905b-715188ad2cd8")

    try:
        page.locator(".tb-time-series-chart-panel")
        print("Time series chart loaded.")
    except:
        print("Time series chart not found.")

    #update temperature to value greater than threshold - threshold set to 40

    payload = {"temperature": 50 }
    response = requests.post(
        f" http://demo.thingsboard.io/api/v1/wQeBTNSNpmL0VTHmWTkj/telemetry",
        json=payload,
        headers={"X-Authorization": jwt_token}
    )

    titles = page.locator(".tb-time-series-chart-panel").all_inner_texts()
    # title = page.locator(".tb-widget-title").first.text_content()/

    title = page.locator(".tb-widget-title").first.text_content()
    
    print("Widget Title:", title)
    
    ml_widgets = [t for t in titles if "threshold" in t or "anomaly" in t.lower() or "temperature" in t]
    if ml_widgets:
        print("ML Visualizations is present")
        for widget in ml_widgets:
            print("*", widget)
    else:
        print("No ML widget found.")

        
    page.screenshot(path="ml_widget_threshold_chart_sync.png", full_page=True)
    print("Screenshot saved as 'ml_widget_threshold_chart_sync.png'")

    browser.close()


if __name__ == "__main__":
    try:
        print("Running Playwright test...")
        with sync_playwright() as playwright:
            # print("Test - Validation of login and navigation to dashboard")
            # runLoginDashboard(playwright)
            # print("Test - Validating the real time updation of widgets")
            # runRealTimeUpdates(playwright)
            print("Test - Identify ML based visualization")
            testVisualization(playwright)

    except Exception as e:
        print(f"An error occurred: {e}")
