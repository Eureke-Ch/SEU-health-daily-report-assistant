# SEU-health-daily-report-assistant
 东南大学全校师生每日健康申报打卡助手
 直接下载压缩包，解压后打开bin文件夹，其中health-daily-report.exe是主文件，ChromeDriver.exe是Chrome浏览器的驱动，start_process_hidden.vbs文件是帮助在windows后台隐藏状态运行的脚本，stop_process.bat是帮助结束相关进程的脚本
 * 需求：最新的Chrome浏览器（Chrome89），如果不是最新版本的Chrome浏览器，需要下载对应版本的Chrome驱动，替换ChromeDriver.exe文件；

# 第一次使用需要提供一卡通号和密码
双击health-daily-report.exe文件，按照提示输入相关信息，程序会自动保存在loginData.json文件中，以后便不需要再次提供；用户信息是保存在本地的，不存在任何泄露的风险；

# 后续使用
双击start_process_hidden.vbs脚本文件，程序便自动在windows后台运行，默认是每天10点进行健康申报；若不在需要该程序，双击stop_process.bat脚本结束相关进程即可；
