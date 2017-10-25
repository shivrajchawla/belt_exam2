''' # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from time import strftime,localtime
from ..loginandregistration.models import User
from django.db import models

class Friend(models.Model):
    user =  '''
