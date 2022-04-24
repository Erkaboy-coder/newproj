from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from topografiya.models import *

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import requests

import re

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
import json


class contractAPI(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        # print(request.data['shartnoma_id'])
        data = requests.get('http://test.cpduzgashkliti.uz/api/contractbyid/' + str(request.data['contract_id']))
        json_data = json.loads(data.content.decode('utf-8'))
        if json_data:
            if json_data['Data']['contract']['ContractNumber'] != None:
                if json_data['Data']['contract']['ContractDate'] != None:
                    import datetime
                    text = json_data['Data']['contract']['ContractDate']
                    res = re.findall(r'\((.*?)\)', text)
                    # print(res[0])
                    time = datetime.datetime.fromtimestamp(int(res[0]) // 1000)
                    date = time.strftime('%d/%m/%Y')
                else:
                    print('No ContractDate')
                    date = ''

                if not PdoWork.objects.filter(contract_id=request.data['contract_id']).first():
                    for i in json_data['Data']['contract']['ContractWorkPayments']:
                        work_type = worksType.objects.filter(id=int(i['WorkTypeId'])).first()
                        if i['SubDivision']['Name'] != None:
                            if not work_type:
                                work = WorkType(name=i['WorkType']['Name'])
                                work.save()
                                print('You have to create it')
                            subdevision = SubDivisions.objects.filter(id=int(i['SubDivision']['Id'])).first()
                            if subdevision:
                                branch = Branch.objects.filter(id=int(json_data['Data']['contract']['BranchId'])).first()
                                work_term = Period.objects.filter(id=int(i['PeriodId'])).first()
                                # timestamp = datetime.datetime.fromtimestamp(int(json_data['Data']['contract']['ContractDate']))

                                if branch:
                                    if work_term:
                                        pdowork = PdoWork(agreement_date=date, object_name=json_data['Data']['contract']['ObjectName'],
                                                          subdevision=subdevision, work_type=work_type, branch=branch,
                                                          work_term=work_term, contract_id=request.data['contract_id'],
                                                          object_number=json_data['Data']['contract']['ContractNumber'],
                                                          object_cost=json_data['Data']['contract']['ContractAmount'],
                                                          customer=json_data['Data']['contract']['Organization']['Name'], customer_info=str('Inn: ' + str(json_data['Data']['contract']['Organization']['Inn']) + ' ' + 'Hisob raqami: ' + str(json_data['Data']['contract']['Organization']['AccountNumber']) + ' ' + 'Tel: ' + str( json_data['Data']['contract']['Organization']['PhoneNumbers'])))
                                        pdowork.save()
                                        return Response({'status': 'Success', 'code': 1})
                                    else:
                                        return Response({'status': 'Error no work term', 'code': 4})
                                else:
                                    return Response({'status': 'Error no branch', 'code': 6})

                            else:
                                return Response({'status': 'Error no subdevison', 'code': 5})
                        else:
                            return Response({'status': 'No Subdivision', 'code': 3})
                else:
                    return Response({'status': 'Data exist', 'code': 2})
            else:
                return Response({'status': 'Warning', 'code': 0})
        else:
            return Response({'status': 'Warning', 'code': 0})

#     profile=Profile.objects.create(
#          first_name=request.data['first_name'],
#         last_name = request.data['last_name']
#     )
# return Response({'post': model_to_dict(profile)})
        return Response(json_data)
#
