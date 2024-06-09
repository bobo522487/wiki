import asyncio
from playwright.async_api import async_playwright

RESOURCE_LIMIT = 5
POLLING_TIME = 6000  # seconds
MAX_RETRIES = 99999999
PASSWORD = "KtFkHtX#&=26"


async def main():
    path_to_extension = (
        r"C:\ChromeData\user1\Extensions\bfnaelmomeimhlpmgjnjophhpkkoljpa\24.0.1_0"
    )
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=r"C:\ChromeData\user1",
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=False,
            slow_mo=2000,
            args=[
                f"--disable-extensions-except={path_to_extension}",
                f"--load-extension={path_to_extension}",
                "--hide-scrollbars",
                "--disable-blink-features=AutomationControlled",
            ],
        )
        page = await browser.new_page()
        try:
            print("Logging into StarAtlas...")
            await staratlas_login(page)
            i = 1
            while i <= MAX_RETRIES:  # Limit loop iterations
                print(f"Starting round #{i} mining...")
                await mine_resources(browser, page, PASSWORD)
                i += 1
                await asyncio.sleep(POLLING_TIME)
        except Exception as e:
            print(e)
        finally:
            await browser.close()
            await main()


async def staratlas_login(page):
    await page.goto("https://play.staratlas.com")
    await page.wait_for_load_state("networkidle")
    await page.click('//*[@id="Menu/Faction Fleet"]')
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(20)


async def mine_resources(browser, page, passwd):
    resource_dict = {}  # Initialize empty dictionary
    for i in range(1, 4):  # 3支舰队
        resource_list = []
        for j in range(1, 5):
            resource_list.append(
                await page.text_content(
                    f"//div[{i}]/div[2]/div[2]/div[2]/div[{j}]/div/div[1]/label[2]"
                )
            )
        resource_list = [item.replace("%", "") for item in resource_list]
        name = await page.text_content(
            f"//div[2]/div[{i}]/div[2]/div[1]/div[1]/div[2]/p"
        )
        resource_dict.update({name: resource_list})
        for index, resource in enumerate(resource_list):
            if int(resource) < RESOURCE_LIMIT:
                await page.click(
                    f"//div/div[{i}]/div[2]/div/div/button"
                )  # MANAGE FLEET
                supply_btn_selector = "//div[2]/div/div/div/div[2]/div/div/button"
                await page.click(supply_btn_selector)
                await asyncio.sleep(10)
                new_page = await switch_to_page(browser, title="Phantom Wallet")
                await new_page.fill(
                    'input[name="password"]', passwd
                )  # Type the password
                await new_page.click('button[type="submit"]')  # Unlock
                await asyncio.sleep(5)
                await new_page.click('button[type="submit"]')  # Confirm
                await asyncio.sleep(10)
                await new_page.close()
                await asyncio.sleep(5)
                await page.mouse.click(10, 10)  # 关闭X
                await asyncio.sleep(5)
                break  # Break out of inner loop after mining
    print(resource_dict)


async def switch_to_page(browser, title=None, url=None):
    """Switch to the page with the specified title or URL."""
    for item_page in browser.pages:
        if title:
            if title in await item_page.title():
                await item_page.bring_to_front()
                return item_page
        elif url:
            if url in await item_page.url:
                await item_page.bring_to_front()
                return item_page
    else:
        print("Couldn't find the specified title or URL.")
    return browser.pages[0]


if __name__ == "__main__":
    asyncio.run(main())
