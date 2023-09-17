# Apple 香港刷库存脚本

每5秒轮询一次接口，检测到有库存之后会播送语音提醒（只测试过mac），并记录在available.log中

## 使用指南

1. 安装Python并配置环境
2. 将目标型号代码配置到config.json
3. 运行脚本，等待提醒
4. 目前蓝色256Pro一直是有货状态，可以测试一下语音提醒是否生效

## 环境

Python
安装依赖包

`pip3 install requests`

`pip3 install loguru`

`pip3 install urllib3`

## iPhone代码

|  型号   | 128G  |  256G  |  512G  |  1TB  |
|  ----  |  ----  |  ----  |  ----  | ---- |
|  15 Pro 蓝色  | MTQ73ZA/A | MTQC3ZA/A | MTQG3ZA/A | MTQL3ZA/A |
|  15 Pro 原色  | MTQ63ZA/A | MTQA3ZA/A | MTQF3ZA/A | MTQK3ZA/A |
|  15 Pro 白色  | MTQ53ZA/A | MTQ93ZA/A | MTQE3ZA/A | MTQJ3ZA/A |
|  15 Pro 黑色  | MTQ43ZA/A | MTQ83ZA/A | MTQD3ZA/A | MTQH3ZA/A |
|  15 Pro Max 蓝色  | \ | MU2R3ZA/A | MU2W3ZA/A | MU613ZA/A |
|  15 Pro Max 原色  | \ | MU2Q3ZA/A | MU2V3ZA/A | MU603ZA/A |
|  15 Pro Max 白色  | \ | MU2P3ZA/A | MU2U3ZA/A | MU2Y3ZA/A |
|  15 Pro Max 黑色  | \ | MU2N3ZA/A | MU2T3ZA/A | MU2X3ZA/A |
