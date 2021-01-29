##漫画爬虫  
一个简单的爬虫，依托于selenium的webdriver，实现对漫画图片的爬取。  
适用于：有妖气漫画（页漫） 
  
##环境:  
windows10  
python3.9  
chrome88  
  
##python依赖  
`pip install selenium`   
`pip install requests`  
`pip install bs4`  
  
##初始化：  
编辑并修改get_cookie.py中的url变量，设置为访问漫画目录的url  
`python get_cookie.py`  
运行后40秒内完成登录，将在目录下生成cookie.txt  
  
##运行：  
编辑并修改main.py  
folder_path:图片文件存储地址  
web_link：漫画目录网址  
`python main.py`  
下载成功：正常jpg文件  
下载失败：4字节文件  
如有中断，重新运行即可，脚本会自动定位到先前终止位置  
  
##结束  
运行过程中产生的chromedriver和chrome进程无法自动终止  
使用cmd终止:  
`taskkill /im chromedriver.exe /F`  
`taskkill /im chrome.exe /F`
