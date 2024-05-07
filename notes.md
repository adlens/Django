# Django fundamentals

## Preparation

- 安装最新版本 python
- `pip3 install pipenv`
- 最新版本 VSCode
- VSCode Extension: python

## Creating first django project

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

### Data modelling
