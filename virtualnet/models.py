from django.db import models
import django.core.exceptions as exs

# Create your models here.
class Lab(models.Model):
    title = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.title

class NodeType(models.IntegerChoices):
    CLOUD = 0, 'CLOUD'
    VIRTUALMACHINE = 1, 'VIRTUAL MACHINE'

class Node(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=100, null=False)
    posX = models.FloatField(null=False, default=0.0)
    posY = models.FloatField(null=False, default=0.0)
    scaleW = models.FloatField(null=False, default=50.0)
    scaleH = models.FloatField(null=False, default=50.0)
    iconPath = models.CharField(max_length=120, null=False, default="router-svgrepo-com.svg")
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, null=False)
    type = models.IntegerField(choices=NodeType.choices, default=NodeType.CLOUD, null=False)

    def __str__(self):
        return self.title

class Reference(models.Model):
    domain = models.CharField(max_length=255, null=True, unique=True)
    storage = models.CharField(max_length=255, null=True)

class VirtualMachine(models.Model):
    node = models.OneToOneField(Node, on_delete=models.CASCADE, null=False, blank=True)
    domain = models.CharField(max_length=100, null=False, unique=True)
    reference = models.ForeignKey(Reference, on_delete=models.DO_NOTHING, null=False)
    isExist = models.BooleanField(default=False, null=False)
    ramMB = models.IntegerField(default=256, null=False)
    cpus = models.IntegerField(default=1, null=False)
    interfaces = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.node.title   

class Interface(models.Model):
    vm = models.OneToOneField(VirtualMachine, on_delete=models.CASCADE, null=False)
    ethid = models.IntegerField(default=0, null=False)

class Bridge(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nodeA = models.ForeignKey(Node, on_delete=models.CASCADE, null=False, related_name="nodeA")
    nodeB = models.ForeignKey(Node, on_delete=models.CASCADE, null=False, related_name="nodeB")
    ethA = models.IntegerField(default=0, null=True)
    ethB = models.IntegerField(default=0, null=True)
    interfaceA = models.OneToOneField(Interface, on_delete=models.CASCADE, null=True, related_name="intA")
    interfaceB = models.OneToOneField(Interface, on_delete=models.CASCADE, null=True, related_name="intB")

    def getNetName(self):
        return str(self.id).zfill(14)
    
    def clean(self) -> None:
        if self.nodeA.lab != self.nodeB.lab:
            raise exs.ValidationError("Nodes must attend to the same lab!")
        return super().clean()

    def __str__(self):
        return f'Node 1: {self.nodeA.title}; Node 2: {self.nodeB.title}'