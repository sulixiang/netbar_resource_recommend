# netbar_resource_recommend

## 文件结构
.
├── app.py ---推荐模型应用服务  
├── build_app.py ---推荐模型构建服务  
├── datasets  
│   └── export_gamerun_series.csv ---数据集  
├── engine.py ---推荐引擎  
├── logs  
├── model  
│   └── wordVector.txt ---模型持久化文件  
├── README.md  
├── start_server.sh ---服务启动脚本  
├── static  
│   ├── app.html ---模型应用页面  
│   ├── build_app.html ---模型构建页面  
│   └── index.html ---框架页  
└── templates  
    └── result.html ---结果渲染页  

## 用法
```
sh start_server.sh
```
