from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import requests
from .models import DepositOptions, DepositProducts
from .serializers import DepositOptionsSerializer, DepositProductsSerializer, ProductOptionSerializer
from rest_framework import status
from django.db.models import Max





# Create your views here.
@api_view(['GET'])
def save_deposit_products(request):
    api_key = settings.API_KEY
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()

    for li in response.get('result')['baseList']:
        fin_prdt_cd= li['fin_prdt_cd']
        kor_co_nm= li['kor_co_nm']
        fin_prdt_nm= li['fin_prdt_nm']
        etc_note= li['etc_note']
        join_deny = li['join_deny']
        join_member = li['join_member']
        join_way = li['join_way']
        spcl_cnd = li['spcl_cnd']
    
        if DepositProducts.objects.filter(
            fin_prdt_cd=fin_prdt_cd,
            kor_co_nm=kor_co_nm,
            fin_prdt_nm=fin_prdt_nm,
            etc_note=etc_note,
            join_deny=join_deny,
            join_member=join_member,
            join_way=join_way,
            spcl_cnd=spcl_cnd):

            continue
    
        save_data = {
            'fin_prdt_cd':fin_prdt_cd,
            'kor_co_nm':kor_co_nm,
            'fin_prdt_nm':fin_prdt_nm,
            'etc_note':etc_note,
            'join_deny':join_deny,
            'join_member':join_member,
            'join_way':join_way,
            'spcl_cnd':spcl_cnd
        }
        serializer = DepositProductsSerializer(data = save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for li in response.get('result')['optionList']:

        fin_prdt_cd = li['fin_prdt_cd']
        intr_rate_type_nm = li['intr_rate_type_nm']
        intr_rate = li['intr_rate']
        intr_rate2 = li['intr_rate2']
        save_trm = li['save_trm']
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        print(fin_prdt_cd, intr_rate_type_nm, intr_rate, intr_rate2, save_trm, product)

        # 비어있는 필드에 대한 기본값 설정
        intr_rate_type_nm = li.get('intr_rate_type_nm', '-1')
        intr_rate = li.get('intr_rate', -1.0) if li.get('intr_rate') is not None else -1.0
        intr_rate2 = li.get('intr_rate2', -1.0) if li.get('intr_rate2') is not None else -1.0
        save_trm = li.get('save_trm', -1) if li.get('save_trm') is not None else -1


        if DepositOptions.objects.filter(
            fin_prdt_cd=fin_prdt_cd,
            intr_rate_type_nm=intr_rate_type_nm,
            intr_rate=intr_rate,
            intr_rate2=intr_rate2,
            save_trm=save_trm,
            product=product
        ):
            continue

        save_data = {
            'fin_prdt_cd':fin_prdt_cd,
            'intr_rate_type_nm':intr_rate_type_nm,
            'intr_rate':intr_rate,
            'intr_rate2':intr_rate2,
            'save_trm':save_trm,
        }
        serializer = DepositOptionsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product)
        
    return Response(response)



@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        products = DepositProducts.objects.all()
        serializers = DepositProductsSerializer(products, many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        serializers = DepositProductsSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response({ 'message': '이미 있는 데이터이거나, 데이터가 잘못 입력되었습니다.' }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def deposit_products_options(request, fin_prdt_cd):
    options = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializers = DepositOptionsSerializer(options, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def top_rate(request):
    if request.method == 'GET':
        top_rate = DepositOptions.objects.aggregate(intr_rate2=Max('intr_rate2'))
        # queryset이 아닌. '컬럼명'만 들어있는 dictionary 형태로 반환된다.
        # top_rate['intr_rate2'] 으로 사용하면 됨.
        option = DepositOptions.objects.get(intr_rate2=top_rate['intr_rate2'])
        product = DepositProducts.objects.filter(pk=option.product_id)
        serializer = ProductOptionSerializer(product, many=True)
        return Response(serializer.data)

