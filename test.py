from playwright.sync_api import sync_playwright

def scrape():
    with sync_playwright() as p:
        # 启动 Chromium 浏览器 (headless: False 可以让你看到浏览器操作过程)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 打开目标网址
        page.goto('https://baidu.com')
        
        # 等待网页加载完成
        page.wait_for_load_state('load')
        
        # 获取网页内容，例如标题
        title = page.title()
        print(f"Page title: {title}")
        
        # 获取页面的 HTML 内容
        content = page.content()
        print(f"Page content: {content[:200]}")  # 打印前200个字符
        
        # 关闭浏览器
        browser.close()

if __name__ == "__main__":
    scrape()
