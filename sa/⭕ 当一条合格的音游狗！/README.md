### 使用
- 配置环境
  - `pip install -r requirements.txt`
  - or `poetry install`
- 安装 supervisor
- 修改 `daemon.conf` 里的 `SOMEWHERE` 到脚本所在目录
- 移动 `daemon.conf` 到 supervisor 配置目录下
- `supervisorctl reload`
- `supervisorctl update`

### 配置
目录下 `config.toml`，可以增加日志 sink，设置报警阈值，开闭指标模块/报警方法，etc.

### 如何分发程序
用 scp 或 rsync 主动分发

或者在内网设置一个共享目录，其它服务器定时与它同步

### 如何持久化
因为指标模块可以开闭与增删，所以关系数据库什么的 pass

非关系数据库不熟，也 pass

所以直接输出为日志，输出例在 logs 目录下

`run.log` 是一般日志

`stat.log` 里是各个时间点指标 json 格式的数据，也可以很方便地给第三方做分析
