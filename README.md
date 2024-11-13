
注：
    遵循每个爬虫一个单独的工程，否则可能会影响其他爬虫的正常运行
    目录结构 
        spider-core
            --project
                --core
                --database
                --job
                    --pse
                    --air
                --logs
                --mod
                --util

需要修改：
    requirements.txt
    
生成实体类：
    sqlacodegen mysql://root:Xizheng123\!@192.168.110.157:3306/dc_env_pse?charset=utf8 --tables t_pse_monitor_gas > PseMonitorGasHour.py
安装环境包：
    pip install -r requirements.txt
在终端中打印出每个安装的每个第三方库以及相应版本：
    pip freeze
将这些内容写入文本文件中：
    pip freeze > requirements.txt




