# netbar_resource_recommend

## 文件结构
```
.  
├── engine.py ---推荐引擎  
├── app.py ---推荐模型应用服务  
├── build_app.py ---推荐模型构建服务  
├── start_server.sh ---服务启动脚本  
├── datasets  
│   └── export_gamerun_series.csv ---数据集  
├── model  
│   └── wordVector.txt ---模型持久化文件  
├── static  
│   ├── app.html ---模型应用页面  
│   ├── build_app.html ---模型构建页面  
│   └── index.html ---框架页  
├── templates  
│   └── result.html ---结果渲染页  
├── logs  
└── README.md  
```

## 开启服务
```
sh start_server.sh
```

## 接口说明

- http://[app]/ : demo portal页  
- http://[app]/vec/<resources> : 查询<resource>的特征 ex:http://[app]/vec/英雄联盟  
- http://[app]/ranking : POST:positive、negative、rawdata，对rawdata排序  
- http://[app]/top/<n> : 获取topn推荐，ex:http://[app]/top/10  
- http://[app]/flush/engine : 重新加载推荐模型  
- http://[build_app]/resource/add : 增加用户行为路径数据，更新推荐模型  
- http://[build_app]/build/model : 从数据集文件创建模型  
 
