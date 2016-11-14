# bledevices
#### 因为django 1.5.11太老可能需要修改一些地方
总是提示cannot import name Engine, 因为对于django 1.5.11，django.template里没有Engine
要找虚拟环境里chartkick.py里改两个地方， lib/python2.7/site-packages/chartkick/templatetags
```         
#from django.template import Engine
from django.template.loader import BaseLoader
```
in ChartNode.Library()
```
#loader = Loader(Engine())
loader = Loader(BaseLoader())
```
