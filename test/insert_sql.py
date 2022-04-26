
import pymysql
from faker import Faker
import random
faker = Faker('zh_CN')

db = pymysql.connect(host='localhost',
                     user='root',
                     password='root',
                     database='communitydb')
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询 
sql = 'select tid from msg_article'
cursor.execute(sql)
res = cursor.fetchall()
res = [list(i)[0] for i in res]
# for i in range(300):
#     name = faker.sentence()
#     #msg = faker.text()
#     user_id = random.randint(33, 146)
#     article_id = random.choice(res)
#     #plate_ids = [1,2,3,5,6,7,19,20,24,25,26]
#     #plate_id = plate_ids[random.randint(0,10)]
#     count_comment = 0
#     time = faker.date_time()
#     sql = "insert into msg_comment set content='{}',user_id={},article_id={},status=0,add_time='{}'".format(name, user_id, article_id,time,time)
#     print(sql)
#     cursor.execute(sql)
#     cursor.fetchone()
#     db.commit()


sql = 'select article_id,count(1) from msg_comment group by article_id'
cursor.execute(sql)
res = cursor.fetchall()
res = [list(i) for i in res]
for i in res:
    sql = 'update msg_article set count_comment={} where tid = {}'.format(i[1],i[0])
    cursor.execute(sql)
    cursor.fetchone()
    db.commit()

 
# 关闭数据库连接
db.close()