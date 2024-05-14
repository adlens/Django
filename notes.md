## Chapter 1 Django fundamentals

### Preparation

- 安装最新版本 python
- `pip3 install pipenv`
- 最新版本 VSCode
- VSCode Extension: python

### 虚拟环境

- `pipenv install django` 创建一个虚拟环境并在其中安装 django
- `pipenv shell` 启动虚拟环境
- 在 vscode 中`pipenv --venv`找到虚拟环境的位置
- 用 command palette 将`path/bin/python`设置为 interpreter

### 创建新 project

- 直接呼叫`django-admin`会列出所有可以使用的命令
- `django-admin startproject <project-name> .`以当前文件夹为根目录创建一个 project
- 创建完项目以后，该文件夹中的`manage.py`即成为该项目专属的`django-admin`
- `python3 manage.py <command>`来发出命令

### 创建新 app

- 一个 project 中可以有多个 app，每个执行特定的功能。
- `python3 manage.py startapp <appname>`
- 在 project settings.py 中将新建的 app 加入到 installed app 列表中

### views

- 这是一个 request handler，当有 request 进来，views.py 来决定返回什么 response

### Mapping urls to views

- 在 app 的文件夹内添加文件`urls.py`

```python
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
]
```

- 在 project 文件夹的`urls.py`中将新 app 的 urls 导入

```python
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('playground/', include('playground.urls'))
]

```

### Using templates

- 在 app folder 中添加新的文件夹`templates`，在这里保存 html 文件。在 views.py 中返回 render 后的 html 文件`return render(request, 'hello.html')`
- render 还可以接受不同变量，比如`return render(request, 'hello.html', {'name': 'adlens'})`，在 hello.html 中引入`<h1>Hello {{ name }}</h1>`即可渲染你的名字
- template 中还可以使用 if 判断句

```html
{% if name %}
<h1>Hello {{ name }}</h1>
{% else %}
<h1>Hello World</h1>
{% endif %}
```

### Debugging django apps in vscode

- 点进 vscode 的 debug 标志，点击`create a launch.json file`，选择 python 和 django
- `launch.json`中修改`"args": ["runserver", "9000"],`这样将 debug 的 port 和平时运行的 port 分开

### Django debug toolbar

- 参考官方 documentation
- `pipenv install django-debug-toolbar`
- 添加`"debug_toolbar",`到 project settings.py 的 INATALLED_APPS 中。并添加`"debug_toolbar.middleware.DebugToolbarMiddleware"`到 MIDDLEWARE 列表中。最后，添加一个新的设置`INTERNAL_IPS = ["127.0.0.1",]`
- 添加`path("__debug__/", include("debug_toolbar.urls"))`到 project 的 urls.py 中，别忘了`import debug_toolbar`

## Chapter 2 Modelling

### Creating models

- 创建 class，变量=`model.<适合的field>(<attributes>)`
- 搜索 Django field types 确定你需要的数据类型
- django 会自动生成 primary key，但如果你想要设置某一变量为 primary key，可以在定义其 attribute 时加上`primary_key=True`

### Choice Field

- 比如某个数据存储的时候用缩写，但是又想记录它对应的全称

```python
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
```

### DateTimeField

- `auto_now_add`：这个参数用于在模型的实例首次创建时自动设置当前的日期和时间。一旦设置，在后续的保存操作中，这个字段的值不会再自动更新。
- `auto_now`：这个参数用于每次保存模型实例时自动更新当前的日期和时间。无论是在新建还是更新实例时，只要调用了.save()方法，这个字段的值就会被更新为当前的时间。

### Defining one-to-one relationships

- 先定义 parent，再定义 child
- 比如在 Address 的 model 中将其与 customer 链接 `customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)`

- 此处 on_delete，`models.CASCADE`表示如果该顾客信息被删除，address 也被删除。`models.SET_NULL`表示顾客被删除时将 address 保留但设置为 Null。`models.SET_DEFAULT`回到初始设置。`models.PROTECT`表示必须先删除 child(address)才能删除 parent(customer)。

### Defining one-to-many relationships

- 假设一个顾客可以有多个地址，`customer = models.ForeignKey(Customer, on_delete=models.CASCADE)`。类型改成 ForeignKey，去掉 primary_key 选项

### Defining many-to-many relationships

- 比如每个 product 可能有多个 promotion，每种 promotion 也可以应用在多个 product 上
- 在 Product 类中定义`promotions = models.ManyToManyField(Promotion)`

### Resolving circular relationships

```
class Collection(models.Model):
    ...
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

class Product(models.Model):
    ...
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    ...
```

- `on_delete=models.SET_NULL`：这个选项定义了当关联的对象（在你的示例中是 Product）被删除时，外键字段（featured_product）应如何响应。models.SET_NULL 指定当关联的 Product 对象被删除时，featured_product 字段的值将被设置为 null，也就是没有任何关联的对象。为了使用 models.SET_NULL，必须将外键字段的 null 参数设置为 True，这表明该字段允许存储 null 值。
- `related_name='+'`：用于指定从关联对象回到这个对象时使用的名称。例如，如果 Product 模型中有一个指向 Store 的外键，通常可以通过 product.store 访问该 Store 实例，反过来也可以使用 store.product_set 来访问所有关联的 Product 实例。设置 related_name='+' 实际上是告诉 Django，我们不需要反向关系。这意味着从 Product 模型无法通过一个简单的属性访问到关联的 featured_product 对象。这样做通常是为了避免命名冲突或者简化模型间的关系，尤其在不需要使用反向查询时。

### Generic Relationships

- 在 Django 中，Generic Relationships（通用关系）允许一个模型与多个其他模型建立关联，而不是只与一个特定模型关联。这种机制通过使用 Django 的内容类型框架（content types framework）来实现，它能够让一个模型引用 Django 项目中的任何模型实例。

- 在一些情况下，你可能需要让一个模型能够关联到多种不同的模型。例如，考虑一个评论系统，你希望用户可以对博客帖子、图片或其他用户进行评论。在这种情况下，你需要一个评论模型，它可以关联到多种不同的对象。

- Django 通过以下三个主要组件实现通用关系：

1. **ContentType**：这是一个 Django 模型，它为项目中的每个模型类维护一个记录。它可以让你引用任何其他模型。

2. **GenericForeignKey**：这是一个特殊的外键，它不是直接指向一个特定的模型，而是结合使用 `ContentType` 和模型实例的 ID 来引用任何对象。

3. **GenericRelation**：这个字段不是必须的，但它允许反向查询从关联对象回到含有 GenericForeignKey 的对象。

- 假设你有一个 `Comment` 模型，它可以关联到不同类型的对象，比如 `Book` 和 `Movie`：

```python
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()

class Book(models.Model):
    title = models.CharField(max_length=100)

class Movie(models.Model):
    title = models.CharField(max_length=100)
```

- 在这个例子中，`Comment` 可以关联到任何模型。你只需要为 `Comment` 模型添加 `content_type` 和 `object_id` 字段，并通过 `GenericForeignKey` 定义 `content_object` 属性。
- 实例:

```python
# 创建一个书本和作者
book = Book.objects.create(title="Django for Professionals")
author = Author.objects.create(name="William S. Vincent")

# 标记书本
tag1 = TaggedItem.objects.create(tag='django', content_object=book)

# 标记作者
tag2 = TaggedItem.objects.create(tag='expert', content_object=author)

# 查询使用特定标签的书本
django_books = TaggedItem.objects.filter(tag='django', content_type=ContentType.objects.get_for_model(Book))
```

## Chapter 3 Database

### Creating migrations

- `python manage.py makemigrations` 对 model 做出改变后都要运行，它会变成一串记录就像 git log 一样
- `Command + t`快速查找 workspace 中的某个 class，method，variables 等等

### Running migrations

- `python manage.py migrate`
- vscode 默认使用 sqlite3，是一个非常简易的 database。我们之后会使用 mysql
- 先安装 sqlite 插件 -> command palette -> sqlite: open database -> 选择相应 database，可以在 explorer 下端找到 sqlite explorer。右键即可 show table

### Customizing Database Schema

- 搜索`django model metadata`
- 它位于某个 model 的 class 内部

```python
    class Meta:
        db_table = "store_customers" # 将表命名为store_customer
        indexes = [models.Index(fields=["last_name", "first_name"])] # 将姓名结合并生成一个索引
```

### Reverting migrations

- 找到你想回到的 migration 序号`python manage.py migrate store 0003`，手动删除不想要的那些 migration 和 code
- 如果有 git 作为版本控制，`git reset --hard HEAD~1`

### Installing MySQL and Connecting to MySql

- 下载 MySQL Community Server 并安装
- 下载 DataGrip，选择 database 为 mysql，user 为 root，密码为 mysql 的密码
- 右键 localhost，选择 new->query console,可以在其中输入 SQL 命令
- `CREATE DATABASE storefront`

### Using MySQL in Django

- `pipenv install mysqlclient`
- `mysql -u root -p` 输入 mysql 的密码
- 退出 mysql 为 ctrl + D
- 在 settings.py 的 DATABASES 中作出如下修改

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "storefront",
        "HOST": "localhost",
        "USER": "root",
        "PASSWORD": "password"
    }
}
```

- 再运行`python manage.py migrate`

### Running custom SQL

- 在 django 中使用 sql 语言更新数据库
- 创建一个新的空的 migration`python manage.py makemigrations store --empty`
- 打开新创建的文件进行编辑，并运行 migrate

```python
    operations = [
        migrations.RunSQL(
            """
            INSERT INTO store_collection (title)
                          VALUES ('collection1')
            """, # 运行migrate的时候执行
            """
            DELETE FROM store_collection
            WHERE title='collection1'
            """, # revert migrate的时候执行
        )
    ]
```

- revert migrate `python manage.py migrate store <前一个编号>`

### Generating Dummy Data

-`mockaroo.com`将生成的数据存成 sql 文件拽进 datagrip 中，选择正确的 schema，全选并运行

## Chapter 4 Django ORM

### Managers and QuerySets

- views.py 文件

```python
def say_hello(request):
    query_set = Product.objects.all() # 创建一个query，但不会被马上evaluate
    # list(query_set)
    # query_set[0]
    for product in query_set: # 这三行都能唤醒query
        print(product) # 可以用toolbar在网页上查看sql信息，已经获取了所有的product信息
    return render(request, "hello.html", {"name": "Mosh"})
```
