# 百度百科爬虫

数据库中有 cropName, data, imgs三个集合
## 大致流程:
1. 把要爬取的关键词写入cropName.txt里, 一行一个关键词.
2. 在当前目录下 cmd    
python ./run.py
3. 如果有需要, 在当前cmd目录下运行
python ./load.py
从数据库中输出到当前目录的data文件夹里

## 运行原理:
1. 把txt内文本存入数据库的 cropName 集合,并把临时的cropsUrl集合清空
2. 根据集合内未爬取的关键词爬取百科网页, 把数据存到data集合内, 并把爬取的url存到cropsUrl集合
3. 运行 selenium. 根据cropsUrl爬取百科星图的关键词, 把新的关键词更新到cropName集合中  
4. 重复步骤2


## 遇到的问题:
- [ ] 图册网页是动态网页, 部分数据爬取不全. 补全网页.
https://baike.baidu.com/pic/%E9%A9%AC%E9%93%83%E8%96%AF/416928?fr=lemma
- [x] 把存储的数据改成 hash 结构. 一个是保障数据在爬取过程中冗余数据不重复, 一个是保障爬完基本数据后, 用传参的形式添加词条, 不会使爬虫再次爬取多余的内容.

## 小结
在github上看到了已经相当完善的百度都百科爬虫https://github.com/BaiduSpider/BaiduSpider/
也看到了通过百度百科构建三元组知识图谱的程序https://github.com/lixiang0/WEB_KG
感觉下次要多参考github

