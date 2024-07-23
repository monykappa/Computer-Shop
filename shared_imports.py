from multiprocessing import AuthenticationError

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.views.generic import ListView
from products.models import *
from django.shortcuts import render, get_object_or_404
from orders.models import *
from userprofile.models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from userprofile.forms import *
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse


from django.shortcuts import render
from products.models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
import random
from products.serializers import *
from rest_framework import generics
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from products.permissions import IsSuperAdmin 

from multiprocessing import AuthenticationError
from django.views.generic import TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.views.generic import ListView
from products.models import *
from django.shortcuts import render, get_object_or_404
from orders.models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from userprofile.models import *
from userprofile.forms import *
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.utils import timezone
import pytz
from django.urls import reverse_lazy
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.serializers import *
from products.permissions import IsSuperAdmin
import logging


from multiprocessing import AuthenticationError
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.views.generic import ListView
from products.models import *
from django.shortcuts import render, get_object_or_404
from orders.models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.pagination import LimitOffsetPagination # type: ignore
from rest_framework.filters import SearchFilter # type: ignore
from products.serializers import *
from home.serializers import *
from home.models import *
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy
from django.db.models import Count
from django.db.models import Sum
from django.db.models import Prefetch

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from delivery.models import *
from orders.models import OrderStatus
from delivery.forms import *
from userprofile.models import *
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Prefetch
import json
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import logout
from products.models import *
from orders.models import *
from datetime import date, timedelta
from django.views.generic import ListView, DetailView
from dashboard.mixins import SuperuserRequiredMixin, UserPermission, DeliveryStaffRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
import io
from bokeh.plotting import figure # type: ignore
from bokeh.embed import components # type: ignore
from plotly.offline import plot # type: ignore
import plotly.graph_objs as go # type: ignore
from userprofile.models import *
from dashboard.forms import *
from advertisements.forms import * 
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from delivery.models import *
from delivery.forms import *
from django.views.generic import FormView, ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from delivery.forms import *
from django.db.models import Prefetch
from advertisements.models import *
# import
from django.db.models import Prefetch
from django.db import transaction
import datetime
# import q
from django.db.models import Q
from django.db.models import Count
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date
# import
from django.views.decorators.http import require_POST
from django.shortcuts import render
# import
from rest_framework import generics
from advertisements.models import *
from advertisements.serializers import AdvertisementSerializer
from django.utils.http import urlencode
from django.db.models.functions import TruncDate
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from plotly.express import bar
import plotly.express as px
import pandas as pd