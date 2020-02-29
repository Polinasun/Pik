from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import FieldError

from django.http import HttpResponse

from rest_framework import status
from rest_framework.views import APIView, Request, Response
from rest_framework.pagination import PageNumberPagination

from logging import Logger
from uuid import UUID
import logging
from sys import stdout

from .serializers import home_Serializer
from .models import Homes
from .models import Bricks

# Create your views here.
DEFAULT_PAGE_LIMIT = settings.DEFAULT_PAGE_LIMIT
def index(request):
    return HttpResponse("Дома")
#Логирование
class BaseView(APIView):
    logger = logging.getLogger(name='views')
    formatter = '{method} : {url} : {content_type} : {msg}'

    def info(self, request: Request, msg: str = None) -> None:
        self.logger.info(
            self.formatter.format(
                method=request.method,
                url=request._request.get_raw_uri(),
                content_type=request.content_type,
                msg=msg
            )
        )

class Home(BaseView):
#GET и POST на дома  
    def get(self, request, h_uuid: UUID):

        self.info(request)

        try:
            home_R = Homes.objects.get(pk = h_uuid)
        except Homes.DoesNotExist as error:
            return Response(status.HTTP_404_NOT_FOUND)
        serializer =home_Serializer(instance = home_R)
        return Response(serializer.data)


    def delete(self, request, h_uuid: UUID):

        self.info(request)

        try:
            home_R = Homes.objects.get(pk = h_uuid)
        except Homes.DoesNotExist as error:
            return Response(status = status.HTTP_404_NOT_FOUND)
        home_R.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    def patch(self, request, h_uuid: UUID):

            self.info(request)

            try:
                home_R = Homes.objects.get(pk = h_uuid)
            except Homes.DoesNotExist as error:
                return Response(status = status.HTTP_404_NOT_FOUND)
            serializer = home_Serializer(instance = home_R, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(data = serializer.data, status = status.HTTP_202_ACCEPTED)
            return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class Homes_all(BaseView):

    def __clear_request_params(self, request: Request) -> dict:
            params = request.query_params.dict()

            if 'page' in params: params.pop('page')

            return params

    def get(self, request):
        self.info(request)
        params = self.__clear_request_params(request)

        try:
            home_R = Homes.objects.filter(**params)

        except FieldError as error:
            return Response(status = status.HTTP_400_BAD_REQUEST )

        paginator = PageNumberPagination()
        paginator.default_limit = DEFAULT_PAGE_LIMIT
        page = paginator.paginate_queryset(home_R, request)

        serializer = home_Serializer(home_R, many = True)
        return Response(data = serializer.data)

    def post(self, request):

        self.info(request)

        serializer = home_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)

        return Response(status = status.HTTP_400_BAD_REQUEST)

