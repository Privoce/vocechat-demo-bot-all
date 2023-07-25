# VOCECHAT BOT DEMO

> Please choose according to your own language

## Run under Node
- Install the node environment
- Download or git clone, node folder, enter the folder
- Copy `.env.example` to `.env`, fill in the corresponding data
- Execute `npm i` to install dependent packages
- Execute `npm start` to run the project

## Python
- install py
- Download the python folder
- Install the dependency package `pip install flask requests`
- Corresponding place - line 28-29, fill in the corresponding data
- run `main.py`

## Fastapi
- git clone
- cd vocechat-fastapi-simplify
- cp app/core/config.py.simple app/core/config.py
- nano app/core/config.py
- pip install -r requirements.txt
- python main.py

The above address is the address of local operation, fill in the corresponding address on the BOT setting page of voce, `http://127.0.0.1:4080/demo` should be able to communicate
If the server of the website and the webhook are not the same, you can reverse proxy it by yourself



> 请根据自己的语言选择

## Node下运行
- 安装node环境
- 下载或git clone，node文件夹，进入文件夹
- 复制`.env.example`为`.env`，填入对应数据
- 执行`npm i`,安装依赖包
- 执行`npm start`，运行项目

## Python
- 安装好py
- 下载python文件夹
- 安装依赖包`pip install flask requests`
- 相应地方-line 28-29处，填入对应的数据
- 运行`main.py`

## Fastapi
- git clone
- cd vocechat-fastapi-simplify
- cp app/core/config.py.simple app/core/config.py
- nano app/core/config.py
- pip install -r requirements.txt
- python main.py

以上地址都是本地运行的地址，在voce的BOT设置页面填入对应的地址，`http://127.0.0.1:4080/demo`应该能够进行通信了
如果网站和webhook的服务器不是同一台，自行反代即可
