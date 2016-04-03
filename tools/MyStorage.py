# -*- coding: utf-8 -*-
from os import environ
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import time,os,uuid,random,unicodedata,StringIO
from django.core.files.base import ContentFile
debug = settings.DEBUG
if not debug:
    import sae
    import sae.storage

class SaeAndNotSaeStorage(FileSystemStorage):
    """
    这是一个支持sae和本地django的FileStorage基类
    修改存储文件的路径和基本url
    """
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(SaeAndNotSaeStorage, self).__init__(location, base_url)

    # def get_valid_name(self, name):
    #     """
    #     这个方法用于验证文件名,我这里的处理方法是去掉中文，我没有找到支持中文名的方法，欢迎补充
    #     """
    #     #name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
    #     #处理中文文件名sae不支持
    #     if not debug:
    #         try:
    #             if 1:
    #                 #去掉中文
    #                 name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
    #             else:
    #                 for k in name:
    #                     if self.is_chinese(k):
    #                         name = "wszw%s"%random.randint(0,100)
    #         except Exception,e:
    #             name = "%s.jpg"%type(name)
    #     #end
    #     return super(SaeAndNotSaeStorage, self).get_valid_name(name)

    @property
    def maxsize(self):
        return 10*1024*1024#文件2M--sae限制只能传2M,单个文件，据说是10M,其实只有2M

    @property
    def filetypes(self):
        return []

    # def makename(self,name):  
    #     #取一个不重复的名字，sae会把重名覆盖
    #     oname = os.path.basename(name)
    #     path = os.path.dirname(name)
    #     #首先判断是否需要重命名---也就是说不想改名字的就加这个前缀
    #     if oname.find("_mine_")==0:
    #         oname = oname.replace("_mine_","")
    #         name = os.path.join(path, oname)
    #         return name
    #     #end---首先判断是否需要重命名
    #     try:
    #         fname, hk = oname.split(".")
    #     except Exception,e:
    #         fname, hk = oname, ''
    #     if hk:
    #         rname  = "%s_%s.%s"%(random.randint(0,10000), fname,hk)
    #     else:
    #         rname  = "%s_%s"%(random.randint(0,10000), fname)
    #     name = os.path.join(path, rname)
    #     #end
    #     return name

    def _save(self, name, content):
        """
        可以判断上传哪些文件
        """
        # hz = name.split(".")[-1]
        # #类型判断
        # if self.filetypes!='*':
        #     if hz.lower() not in self.filetypes:
        #         pass
        # #end
        # name = self.makename(name)
        # #大小判断
        # if content.size > self.maxsize:
        #     pass
        # contentsize=content.size
        if not debug:
            s = sae.storage.Client()
            ob = sae.storage.Object(content.read())
            url =s.put('resources', name, ob)
            return name
        else:
            return super(SaeAndNotSaeStorage, self)._save(name, content)

    def delete(self,name):
        """sae的存储空间很宝贵，所有我们在删除图片数据库记录的时候也需要删除图片
        """
        if not debug:
            s = sae.storage.Client()
            s.delete('resources', name)
        else:
            return super(SaeAndNotSaeStorage, self).delete(name)

class FileStorage(SaeAndNotSaeStorage):
    @property
    def maxsize(self):
        return 10*1024*1024

    @property
    def filetypes(self):
        return "*"