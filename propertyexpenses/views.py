from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from proplandtent.models import Property, TenancyLease, Units, UserRegistry, Role, RefreshTokenRegistry
from .models import Invoices
from django.middleware import csrf
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse
from proplandtent.decorators import is_authorized, is_admin, is_landlord, is_tenant
from proplandtent.oauth2 import create_tokens, return_accesstoken_from_refresh
from django.conf import settings
from facilitymanager.settings import ACCESS_TOKEN_LIFETIME, ALGORITHM, REFRESH_TOKEN_LIFETIME
from datetime import datetime, date
import pandas as pd
import traceback
import requests
import os
import csv
import json
# Create your views here.


