from django.db import models

# Create your models here.

class Maincategory(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=28)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=28)
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=28)

    def __str__(self):
        return self.name

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    maincategory=models.ForeignKey(Maincategory, on_delete=models.CASCADE)
    subcategory=models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand, on_delete=models.CASCADE)
    color=models.CharField(max_length=20)
    size=models.CharField(max_length=20)
    stock=models.CharField(max_length=20,default="In Stock",null=True)
    description=models.TextField()
    baseprice=models.IntegerField()
    discount=models.IntegerField(default=0,null=True,blank=True)
    finalprice=models.IntegerField()
    pic1=models.ImageField(upload_to="upload",default="",null=True)
    pic2=models.ImageField(upload_to="upload",default="",null=True)
    pic3=models.ImageField(upload_to="upload",default="",null=True)
    pic4=models.ImageField(upload_to="upload",default="",null=True)

    def __str__(self):
        return self.name

class Buyer(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    phone=models.CharField(max_length=15)
    addressline1=models.CharField(max_length=150)
    addressline2=models.CharField(max_length=150)
    addressline3=models.CharField(max_length=150)
    pin=models.CharField(max_length=10)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    otp=models.IntegerField(default=-000000)
    pic=models.ImageField(upload_to="upload",default="",null=True)

    def __str__(self):
        return str(self.id)+"   "+str(self.username)

class Wishlist(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.str(id)+"  "+self.user.username+'  '+self.product.name

class Checkout(models.Model):
    status_choices=((0,"Order Placed"),(1,'Not Packed'),(2,'Packed'),(3,'Ready to Ship'),(4,'Shipped'),(5,'Out For Delivery'),(6,'Delivered'),(7,'Cancelled'))
    payment_choices=((0,'Pending'),(1,'Done'))
    mode_choices=((0,'COD'),(1,'Net Banking'))
    id=models.AutoField(primary_key=True)
    total=models.IntegerField(default=0)
    user=models.ForeignKey(Buyer,on_delete=models.CASCADE)
    shipping=models.IntegerField()
    final=models.IntegerField()
    rppid=models.CharField(max_length=30,default='',null=True,blank=True)
    date=models.DateTimeField(auto_now=True)
    mode=models.IntegerField(choices=mode_choices,default=0)
    payment=models.IntegerField(choices=payment_choices,default=0)
    status=models.IntegerField(choices=status_choices,default=0)

    def __str__(self):
        return str(self.id)+"  "+(self.user.username)
 
class CheckoutProducts(models.Model):
    id=models.AutoField(primary_key=True)
    checkout=models.ForeignKey(Checkout,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)
    total=models.IntegerField()

    def __str__(self):
        return str(self.id)+"  "+str(self.checkout.id)

class Contact(models.Model):
    contactStatus=((0,"Active"),(1,"Done"))
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    subject=models.CharField(max_length=150)
    message=models.TextField()
    status=models.IntegerField(choices=contactStatus,default=0)
    date=models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)+"  "+self.name+"  "+self.subject 
