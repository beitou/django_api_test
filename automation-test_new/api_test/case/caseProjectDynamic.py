import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from api_test.common.api_response import JsonResponse
from api_test.models import CaseProject, CaseProjectDynamic
from api_test.serializers import CaseProjectDynamicSerializer, CaseProjectSerializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class Dynamic(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        添加项目动态
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer！")
        caseProject_id = request.GET.get("caseProject_id")
        if not caseProject_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            pro_data = CaseProject.objects.get(id=caseProject_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = CaseProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        obj = CaseProjectDynamic.objects.filter(caseProject=caseProject_id).order_by("-time")
        paginator = Paginator(obj, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = CaseProjectDynamicSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="999999", msg="成功！")
