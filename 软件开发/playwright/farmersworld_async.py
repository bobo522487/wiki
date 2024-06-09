#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：exe -> staratlas
@Author ：Electric_Wave
@Date   ：2022/11/18 21:51
@Desc   ：
=================================================='''
TOOLS = 12
MEMMBER = 6

# TOOLS = 10
# MEMMBER = 5
import asyncio
import logging
from playwright.async_api import async_playwright
import getpass
import time

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='log.txt',
        filemode='w')

#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

__USER_DATE_DIR_PATH__ = f"C:\\Users\\{getpass.getuser()}\\AppData\Local\Google\Chrome\\User Data"
__EXECUTABLE_PATH__ = f"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir = __USER_DATE_DIR_PATH__,
            executable_path = __EXECUTABLE_PATH__,
            accept_downloads=True,
            headless=False,
            bypass_csp=True,
            slow_mo=10,
            args =['--disable-blink-features=AutomationControlled'],
    )
    page = await browser.new_page()
    try:
        login(page=page)
        i = 1
        while True:
            time_start = time.time()
            logging.info('----------%s-----------', i)
            mining(page=page)
            exchange(page=page)
            time_end = time.time()
            totallytime = round(time_end - time_start, 2)
            logging.info('totally time: %s s', totallytime)
            i += 1
            page.wait_for_timeout(3000)
        page.close()
        browser.close()
    except Exception as e:
        logging.debug(e)
    finally:
        page.close()
        browser.close()
        run( playwright )

async def login(page):
    await page.goto("https://play.farmersworld.io/")
    await page.wait_for_timeout(5000)
    await page.get_by_role("button", name="Login").click()
    await page.wait_for_timeout(1000)
    with page.expect_popup() as popup_info:
        await page.get_by_role("button", name="wax-cloud-wallet Wax Wallet Account").click()
        await page.wait_for_timeout(9000)
    while ( not page.get_by_role("img", name="Map") ):
        login(page)

def mining(page):
    page.get_by_role("img", name="Map").click()
    page.locator(".map-container-bg").first.click()
    for i in range(1, TOOLS+1):
        page.locator(f'//section/div/section/img[{i}]').click()
        # 修理工具
        repair_min, repair_max = page.text_content('//div[@class="content"]').split('/ ')
        tool_name = page.text_content('//section/div/div/div[2]/div[1]/div[1]/div[2]')
        flag = page.text_content('//button/div')

        logging.info('%d %s %s/%s %s', i, tool_name, repair_min, repair_max, flag)
        if int(repair_min) < (int(repair_max) / 2):
            logging.info('开始修理工具...')
            page.get_by_role("button", name="Repair").click()
            page.wait_for_timeout(10000)
        # 工具挖矿
        if flag == 'Mine':
            logging.info('开始挖矿...')
            page.get_by_role("button", name="Mine").click()
            page.wait_for_timeout(5000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)
        elif flag == 'No Energy':
            energy(page=page)
        else:
            page.wait_for_timeout(5000)
        page.wait_for_timeout(2000)

    # 会员金币
    for j in range(TOOLS+1, TOOLS + MEMMBER +1):
        page.locator(f'//section/div/section/img[{j}]').click()
        tool_name = page.text_content('//section/div/div/div[2]/div[1]/div[1]/div[2]')
        flag = page.text_content('//button/div')
        logging.info('%d %s %s', j, tool_name, flag)
        if flag == 'Claim':
            try:
                page.get_by_role("button", name="Claim").click()
                page.wait_for_timeout(5000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(3000)
            except Exception as e:
                print(e)
        elif flag == 'No Energy':
            energy(page=page)
        else:
            page.wait_for_timeout(5000)

def energy(page):
    logging.info('开始恢复能量...')
    page.get_by_role("img", name="plus").click()
    page.press("input[type=\"number\"]", '9')
    page.wait_for_timeout(1000)
    page.press("input[type=\"number\"]", '9')
    page.wait_for_timeout(1000)
    page.press("input[type=\"number\"]", '9')
    page.wait_for_timeout(1000)
    page.press("input[type=\"number\"]", '9')
    page.wait_for_timeout(1000)
    # page.press("input[type=\"number\"]", 'Enter')
    page.locator("button:has-text(\"Exchange\")").click()
    page.wait_for_timeout(20000)

def exchange(page):
    page.click('//*[@id="root"]/div/div/div[1]/section[2]/div[4]/img')
    page.wait_for_timeout(3000)
    page.click('//*[@id="root"]/div/div/div[1]/div[1]/section/div/div[1]/div[2]')
    page.wait_for_timeout(3000)
    fee = page.text_content('//div[@class="withdraw-tax-tag"]')[-2:-1]
    gold = page.text_content('//section/div/div[2]/div[2]/div[1]/div[1]/div[2]/div')
    wood = page.text_content('//section/div/div[2]/div[2]/div[1]/div[1]/div[3]/div')
    meat = page.text_content('//section/div/div[2]/div[2]/div[1]/div[1]/div[4]/div')
    logging.info('fee:%s gold:%s wood:%s meat:%s' , fee, gold, wood, meat)

    if fee == '5':
        if float(gold)>10000 and float(wood)>10000 and float(meat)>10000:
            logging.info('开始Withdraw...')
            gold = str(float(gold)-500)
            wood = str(float(wood)-500)
            meat = str(float(meat)-500)
            page.locator('//section/div/div[2]/div[2]/div[1]/div[2]/div[2]/input').fill(gold)
            page.locator('//section/div/div[2]/div[2]/div[1]/div[2]/div[3]/input').fill(wood)
            page.locator('//section/div/div[2]/div[2]/div[1]/div[2]/div[4]/input').fill(meat)
            page.get_by_role("button", name="Withdraw").click()

asyncio.run(main())
