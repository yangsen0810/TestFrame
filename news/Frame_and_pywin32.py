from selenium import webdriver
import time


class GetFrame:
    def __init__(self) -> None:
        super().__init__()
        self.driver = webdriver.Chrome()
        self.url = "https://mail.qq.com/"
        self.url2 = "https://music.163.com/"

    def get_url(self):
        self.driver.get(self.url)
        # 切换iframe
        self.driver.switch_to.frame(self.driver.find_element_by_id('login_frame'))
        time.sleep(3)
        print("切换成功")
        passwd = "yangsen19980810"
        inputpwd = f"document.getElementById('p').value='{passwd}'"
        self.driver.execute_script(inputpwd)
        time.sleep(3)
        # 到主页中进行点击
        try:
            # 退出iframe返回到主界面将焦点放到主界面
            self.driver.switch_to.default_content()
            self.driver.find_element_by_link_text("基本版").click()
            print("退出成功")
            time.sleep(3)
        except Exception as e:
            print(e)

    # 切换handle
    def switch_handle(self):
        self.driver.get(url=self.url2)
        # 点击音乐人
        self.driver.find_element_by_xpath('//*[@id="g-topbar"]/div[1]/div/ul/li[5]/span/a'.format("音乐人")).click()
        time.sleep(3)
        # 切换页面到新打开页面
        handls = self.driver.window_handles
        self.driver.switch_to.window(handls[-1])
        time.sleep(3)
        print("成功选择跳转到新页面")
        self.driver.find_element_by_xpath('//*[@id="g-footfix"]/div[1]/div/ul/li[2]/a').click()
        time.sleep(3)
        self.driver.close()
        print("成功退出")
        # 把焦点切换到原始页面
        self.driver.switch_to.window(handls[0])
        print("切换到原始页面")
        self.driver.find_element_by_xpath('//*[@id="g-topbar"]/div[1]/div/ul/li[4]/span/a').click()
        print("会到原始页面点击商城成功")


if __name__ == "__main__":
    gtf = GetFrame()
    gtf.switch_handle()
