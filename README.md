# xransom

勒索组织爬虫项目

## 使用说明
### 部署方法
推荐使用dockerfile实现部署
```
docker build --network host -t xran .
docker run -it --network host --name ran1 -v /path/to/project:/home/ransomwatch xran
```

## TODO：
[ x ] 爬虫模块- playwright
[ x ] 解析模块- bs4
[   ] 传输模块- mq
[   ] 更新勒索组织

## 网站解析进度

完成mallox

## 项目结构
- scrape.py
    - 实现爬虫功能
    - 实现数据存储功能
- ransomwatch.py
    - 创建爬虫对象
    - 设置爬虫代理
    - 对parsers文件夹下存储的勒索组织解析进行提取
        - 爬取所有解析文件对应的勒索组织的网站
- parsers.py
    - 勒索组织网站解析方法
    - 一个文件对应一个勒索组织的网站解析方法
- 1.py
    - ransomwatch的一次性版
    - 可指定需要爬取的勒索组织名称
- 数据文件
    - posts.json:提取到的勒索攻击事件
    - pages.json:爬下来的勒索组织网页
    - sites.json:勒索组织站点信息
    - users.json:勒索组织相关信息
    - screenshots:爬下来的网站截图
