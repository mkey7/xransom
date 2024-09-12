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

knight
