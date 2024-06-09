# 入门

## 安装

```bash
pip install --upgrade pip
pip install playwright
playwright install
```



## 运行测试

您可以运行单个测试、一组测试或所有测试。测试可以在一个浏览器或多个浏览器上运行。默认情况下，测试以无头方式运行，这意味着在运行测试时不会打开浏览器窗口，并且会在终端中看到结果。如果您愿意，可以使用该`--headed`标志在 headed 模式下运行测试。

- 在 Chromium 上运行测试

  ```bash
  pytest
  ```

- 运行单个测试文件

  ```bash
  pytest test_login.py
  ```

- 运行一组测试文件

  ```bash
  pytest tests/todo-page/ tests/landing-page/
  ```

- 使用函数名运行测试

  ```bash
  pytest -k "test_add_a_todo_item"
  ```




## 录制模式

  ```bash
  playwright codegen
  ```

  

## 跟踪查看器

Playwright Trace Viewer 是一个 GUI 工具，可让您探索记录的 Playwright 测试跟踪，这意味着您可以在测试的每个动作中前后移动，并直观地查看每个动作期间发生的情况。

```python
browser = chromium.launch()
context = browser.new_context()

# Start tracing before creating / navigating a page.
context.tracing.start(screenshots=True, snapshots=True, sources=True)

page.goto("https://playwright.dev")

# Stop tracing and export it into a zip archive.
context.tracing.stop(path = "trace.zip")
```

这将记录跟踪并将其放入名为`trace.zip`.

## 打包文件

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH="0"
playwright install chromium
pyinstaller -F main.py
```



## 发行说明

使用这些新的 API 编写定位器是一种乐趣：

- [page.get_by_text(text, **kwargs)](https://playwright.dev/python/docs/api/class-page#page-get-by-text)按文本内容定位。
- [page.get_by_role(role, **kwargs)](https://playwright.dev/python/docs/api/class-page#page-get-by-role)通过[ARIA 角色](https://www.w3.org/TR/wai-aria-1.2/#roles)、[ARIA 属性](https://www.w3.org/TR/wai-aria-1.2/#aria-attributes)和[可访问名称](https://w3c.github.io/accname/#dfn-accessible-name)来定位。
- [page.get_by_label(text, **kwargs)](https://playwright.dev/python/docs/api/class-page#page-get-by-label)通过关联标签的文本定位表单控件。
- [page.get_by_test_id(test_id)](https://playwright.dev/python/docs/api/class-page#page-get-by-test-id)根据`data-testid`属性定位元素（可以配置其他属性）。
- [page.get_by_placeholder(text, **kwargs)](https://playwright.dev/python/docs/api/class-page#page-get-by-placeholder)通过占位符定位输入。
- [page.get_by_alt_text(text, **kwargs)](https://playwright.dev/python/docs/api/class-page#page-get-by-alt-text)通过替代文本来定位元素，通常是图像。
- [page.get_by_title(text, **kwargs)](https://playwright.dev/python/docs/api/class-page#page-get-by-title)通过标题定位元素。

# 指南

## 动作

### 输入

Playwright 可以与 HTML 输入元素交互，例如文本输入、复选框、单选按钮、选择选项、鼠标单击、键入字符、键和快捷方式以及上传文件和焦点元素。

```py
# Text input
page.get_by_role("textbox").fill("Peter")

# Date input
page.get_by_label("Birth date").fill("2020-02-02")

# Time input
page.get_by_label("Appointment time").fill("13:15")

# Local datetime input
page.get_by_label("Local time").fill("2020-03-02T05:15")
```

### 按键

```py
# Hit Enter
page.get_by_text("Submit").press("Enter")

# Dispatch Control+Right
page.get_by_role("textbox").press("Control+ArrowRight")

# Press $ sign on keyboard
page.get_by_role("textbox").press("$")
```

模拟真实逐个字符地输入字段

```py
# Type character by character
page.locator('#area').type('Hello World!')
```

### 鼠标

```py
# Generic click
page.get_by_role("button").click()

# Double click
page.get_by_text("Item").dblclick()

# Right click
page.get_by_text("Item").click(button="right")

# Shift + click
page.get_by_text("Item").click(modifiers=["Shift"])

# Hover over element
page.get_by_text("Item").hover()

# Click the top left corner
page.get_by_text("Item").click(position={ "x": 0, "y": 0})
```



## 自动等待

Playwright 在执行操作之前对元素执行一系列可操作性检查，以确保这些操作按预期运行。它会自动等待所有相关检查通过，然后才执行请求的操作。如果所需的检查未在给定范围内通过`timeout`，则操作失败并显示`TimeoutError`.



## API测试

### 编写API

[APIRequestContext](https://playwright.dev/python/docs/api/class-apirequestcontext)可以通过网络发送各种 HTTP(S) 请求。



# Debugging Selectors

```powershell
$env:DEBUG="pw:api"
pytest -s
```

```txt
> playwright.$('.auth-form >> text=Log in');

<button>Log in</button>
```



### 剧作家.$$(选择器[)](https://playwright.dev/python/docs/debug-selectors#playwrightselector-1)

与 相同`playwright.$`，但返回所有匹配的元素。

```txt
> playwright.$$('li >> text=John')

> [<li>, <li>, <li>, <li>]
```



# Chrome Extensions

```py
from playwright.sync_api import sync_playwright

path_to_extension = "./my-extension"
user_data_dir = "/tmp/test-user-data-dir"

def run(playwright):
    context = playwright.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        args=[
            f"--disable-extensions-except={path_to_extension}",
            f"--load-extension={path_to_extension}",
        ],
    )
    if len(context.background_pages) == 0:
        background_page = context.wait_for_event('backgroundpage')
    else:
        background_page = context.background_pages[0]

    # Test the background page as you would any other page.
    context.close()


with sync_playwright() as playwright:
    run(playwright)
```











