from django.db import models
from db.base_model import BaseModel
from utils.get_hash import get_hash

# Create your models here.
class PassportManger(models.Manager):
    def add_one_passport(self, username, password, email):
        '''添加一个账户信息'''
        passport = self.create(username=username, password=get_hash(password), email=email)
        # 3.返回passport
        return passport

class Passport(BaseModel):
    '''用户模型类'''
    username = models.CharField(max_length=20, verbose_name='用户名称')
    password = models.CharField(max_length=40, verbose_name='用户密码')
    email = models.EmailField(verbose_name='用户邮箱')
    is_active = models.BooleanField(default=False, verbose_name='激活状态')

    objects = PassportManger()

    class Meta:
        db_table = 's_user_account'
