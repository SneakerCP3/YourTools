# YourTools
Simple tool to make work more efficient, a DIY tool based on uTools http://www.u.tools/ .

## Technical Concept
pynpt: Monitor keyboard

tkinter: gui window

## Installation：
1. 将utool_conf.ini文件放在D盘根目录下
2. 双击tool_window.exe打开即可
3. 开机自启(optional)：https://blog.csdn.net/RobVisual_Servo/article/details/120599052 

   ​    


## Configuration(optional)：
- 打开utool_conf.ini，在对应的section下面添加指令
- section说明：
  [website]    	 打开一个或多个网页，不同网页换行区分
  [local_file] 	   打开一个或多个本地文件或文件夹，不同文件或文件夹换行区分
  [query]		   需要根据用户的输入打开自定义界面(不要更改)
  [cmd]		    打开系统指令，目前只集成了关机命令(最好不要更改，有些系统指令会阻塞程序)

    
## Use：

- Alt+Space或Space+Alt  ： 唤醒工具窗口

- ESC： 清空窗口内容或隐藏工具窗口

- 鼠标悬停在输入框  ： 显示命令提示

- Enter :  根据窗口输入的命令执行，命令下发成功后窗口会自动隐藏

- Delete+Delete  ： 彻底退出程序

- 工具窗口右上角关闭按钮    ： 彻底退出程序



## BulitIn instructions：

- etime  ：打开etime网页

- daily ：打开Arche看板，ERL看板，DS看板

- cn002 ：打开红网Terminal Server网页

- kanban：打开Arche看板

- b_ ：使用Bing进行搜索,b_后面加需要搜索的关键字

- bd_ ：使用百度进行搜索,bd_后面加需要搜索的关键字

- h_   ：打开HMI看板中的某个workitem, h_后面加需要打开的workitem ID

- t_    ：打开TIA看板中的某个workitem, t_后面加需要打开的workitem ID

- shutdown   : 关机
