# 电影网站
## 使用flask为后台,数据库是MYSQL


## 使用条件
###①使用虚拟环境
 * python3
 * python3-pip: sudo apt install python3-pip
 * virtualenv: sudo pip3 install virtualenv
 * mysql-server: sudo apt install mysql-server
 * 激活虚拟环境: sudo ./env/bin/activate
 ###②使用anaconda为环境
 
 * 运行 sudo apt-get install mysql-server
 * 接着是 sudo apt-get install libmysqlclient-dev python3-dev
 * 运行pip install -r requirements.txt安装必要的库
 * pip install mysql-connector-python-rf
 
##运行
###
 
 1. 导入数据库db.sql: mysql -uroot -p -- < /path/to/prject/folder/db.sql
 2 然后运行python dataset.py导入电影的数据,电影的数据是我之前的一个项目爬的豆瓣的，具体的可以访问https://github.com/zhaodi-Wen/DouBanMovie
 5. 运行 "python app.py" 
 6. ctrl+c 退出

##设计
 * 运行app.py 进图界面后，点击register ,写入个人信息,目前使用英文
 * 然后进入页面,点击页面中的Movie可以看到所有电影,点击高亮的Movie 会按照名字排序,Score会按照分数排序
 * 使用超级用户登录 在注册页面  
    First Name: Super<br>
    Last Name: User<br>
    Email: \<anything\><br>
    Gender: \<anything\><br>

## 超级用户的功能
The staff who work at a theatre must be able to:

    Movies  
        添加删除电影,电影
    Genres:
        修改电影的种类
    Rooms:
        更改放映厅的容量
    Showings
        更改电影放映的时间，删除或者增加
    Customer
        查看购票的记录 
    Attend
        查看观看电影的消费者的记录，包括评分的记录
Part 2: 一般用户的功能
        注册包括First Name,Last Name,Email 和Password


    查看影院的全部电影信息
    
    查看影院放映的电影的信息
    
    查询通过时间限制和种类来查询某一部电影的反映时间
    
    给电影评分
    
    编辑自己的电影的种类
    
    编辑自己的账户信息
    
    
    

Vulnerable
    一个简单的Demo