from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

class CertTable(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True, verbose_name='证书信息别名')
    ca_cert = models.TextField(verbose_name='证书')
    ca_secret = models.TextField(verbose_name='密钥')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '证书信息表'
        verbose_name_plural = '证书信息表'

    def __str_(self):
        return f'CA Info {self.name}'

class AccessTable(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True, verbose_name='接入点别名')
    addr = models.CharField(max_length=255, verbose_name='地址 (host:port)')
    ca_info = models.ForeignKey(CertTable, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='证书信息')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '接入点表'
        verbose_name_plural = '接入点表'

    def __str__(self):
        return self.name

class ClientTable(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True, verbose_name='客户端别名')
    addr = models.CharField(max_length=255, verbose_name='地址 (host:port)')
    access_point = models.ManyToManyField(AccessTable, verbose_name='接入点列表')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '客户端表'
        verbose_name_plural = '客户端表'

    def __str__(self):
        return self.name

class ServiceTable(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True, verbose_name='服务别名')
    addr = models.CharField(max_length=255, verbose_name='地址 (host, port)')
    protocol = models.CharField(max_length=10, choices=[('TCP', 'TCP'), ('UDP', 'UDP')], verbose_name='服务类型')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '服务表'
        verbose_name_plural = '服务表'

    def __str__(self):
        return self.name