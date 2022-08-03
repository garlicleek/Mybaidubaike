# 百度百科爬虫
数据在data.rar里

## 大致流程:

1. 把要爬取的关键词写入cropName.txt里, 一行一个关键词.
2. 在当前目录下在当前cmd目录下运行  
python ./run.py
3. 如果有需要, 在当前cmd目录下运行
python ./load.py
从数据库中输出到当前目录的data文件夹里

## 运行原理:

1. 把txt内文本存入数据库的 cropName 集合,并把临时的cropsUrl集合清空
2. 根据集合内未爬取的关键词爬取百科网页, 把数据存到data集合内, 并把爬取的url存到cropsUrl集合
3. 运行 selenium. 根据cropsUrl爬取百科星图的关键词, 把新的关键词更新到cropName集合中  
4. 重复步骤2

## mongoDB

数据库 crop 中有 cropName, data, imgs三个集合, 分别存储 爬取记录, 文本数据 和 图片数据

## TODO:

- [x] 图册网页是动态网页, 部分数据爬取不全. 补全网页.
https://baike.baidu.com/pic/%E9%A9%AC%E9%93%83%E8%96%AF/416928?fr=lemma
- [x] 用mongoDB存储数据
- [x] 完成load.py, 从mongodb生成格式化数据
- [x] 在爬虫平台完成测试
- [x] 测试github上的方案https://github.com/BaiduSpider/BaiduSpider/; https://github.com/lixiang0/WEB_KG

## 小结
1. 关于动态网页: 百度百科图片不是通过json文件存储url的, 我也不知道他的图片名是怎么得到的, 我只能用selenium解决这个问题, 如有大佬,请指正.  
2. 在github上看到了已经相当完善的百度都百科爬虫https://github.com/BaiduSpider/BaiduSpider/ ;也看到了通过百度百科构建三元组知识图谱的程序https://github.com/lixiang0/WEB_KG .经过检验, 百度百科爬虫中的图片不适合本项目. 百度百科构建三元组也是没有必要的, 因为再华东农大的项目里已经涵括了关系抽取的功能

