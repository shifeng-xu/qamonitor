from django.shortcuts import render
from jira import JIRA
from django.shortcuts import HttpResponse
import common.jiraspider as jiraspider
from common.models import JiraRole,JiraUser,Component
import requests
import json
import datetime
from django.db import connection
from common.views import check_login

# 连接jira，全局
jira = JIRA("http://jira.doglobal.cn", basic_auth=("xushifeng", "***"))

@check_login
def bugsoffline(request):

    #jira=jiraConnect()
    #jiraspider.getjRoles()
    #jiraspider.getjUsers()
    #projectNameList=getProjectName()
    response_data={}
    #查询得到所有项目，显示到产品下拉列表中
    nameList = []
    for j in jira.projects():
        if j.name != '线上问题':
            nameList.append(j.name)
    #response_data['proList']=','.join(nameList)
    response_data['proList']=nameList


    return render(request, "bugsoffline_new.html", {'response_data':json.dumps(response_data)})

@check_login
def bugsonline(request):
    response_data = {}
    # 查询得到所有项目，显示到产品下拉列表中
    nameList = []
    components = Component.objects.filter(project='XSWT')
    for component in components:
        nameList.append(component.name)
    # for j in jira.projects():
    #     if j.name=='线上问题':
    #         nameList.append(j.name)
    # response_data['proList']=','.join(nameList)
    response_data['proList'] = nameList

    return render(request, "bugsonline.html", {'response_data': json.dumps(response_data)})
    # str=''
    # for item in projectNameList:
    #     str+=item+'\r\n'
    #
    # getAllBugs()
    # return HttpResponse(str.encode('utf-8'))

def jiraConnect():
    # 连接jira
    jira = JIRA("http://jira.doglobal.cn", basic_auth=("xushifeng", "***"))
    return jira

# 获取当前用户所有项目，返回项目列表
def getProjects():
    projectList=[]
    for j in jira.projects():
        list.append(j)
    return projectList

# 获取当前用户所有项目，返回项目名称列表
def getProjectName():
    global jira

    #group = jira.group_members("jira-software-users")
    #for users in group:
    #    print(users)
    nameList=[]
    for j in jira.projects():
        nameList.append(j.name)
    return nameList

#查询某个项目的bug总数
def getAllBugs():
    #search_str='project in (UAC) and status in(ACTIVE) and created >= "-24H"'
    search_str='project = UAC AND issuetype = bug AND status in (Resolved, Closed, verified, integrated, "PM Confirmed", rejected) AND created >= 2019-08-01 AND created <= 2019-09-02 ORDER BY created DESC'
    issues_in_proj = jira.search_issues(search_str,maxResults = 100)
    # 获取issue的名字
    name_list = [issue.key for issue in issues_in_proj]
    print(name_list)
    return name_list

#根据项目、问题类型、活动状态、创建日期、报告人查询，返回结果条数(传入请求)
#DEMO：project = UAC AND issuetype = bug AND status in (Resolved, Closed, verified, integrated, "PM Confirmed", rejected) AND created >= 2019-08-01 AND created <= 2019-09-02  AND assignee in (gaochen) AND reporter in (currentUser()) ORDER BY created DESC
# def getItems(request):
#     #从请求中取筛选条件，未传入的条件为None
#     if request.method=="POST":
#         project =request.POST.get('project').split(',') if request.POST.get('project')!=None else None
#         issuetype = request.POST.get('issuetype').split(',') if request.POST.get('issuetype')!=None else None
#         status = request.POST.get('status').split(',') if request.POST.get('status')!=None else None
#         created = request.POST.get('created').split(',') if request.POST.get('created')!=None else None
#         assignee = request.POST.get('assignee').split(',') if request.POST.get('assignee')!=None else None
#         reporter = request.POST.get('reporter').split(',') if request.POST.get('reporter')!=None else None
#         orderby = request.POST.get('orderby').split(',') if request.POST.get('orderby')!=None else None
#
#     #拼接语句
#     search_str=''
#     if project!=None:
#         search_str+='project in ('+','.join(project)+')  '
#     if issuetype!=None:
#         search_str+='AND issuetype in ('+','.join(issuetype)+') '
#     if status!=None:
#         search_str+='AND status in ('+','.join(status)+') '
#     if created != None:
#         search_str += 'AND created >='+created[0]+' AND  created <='+created[1]+' '
#     if reporter != None:
#         search_str += 'AND reporter in (' + ','.join(reporter) + ') '
#     if assignee != None:
#         search_str += 'AND assignee in (' + ','.join(assignee) + ') '
#     if orderby != None:
#         search_str += 'ORDER BY ' + ','.join(orderby) + ' DESC'
#
#     #执行jira查询
#     result=jira.search_issues(search_str, maxResults=999999)
#     count=len(result)
#     return count

#根据项目、问题类型、活动状态、创建日期、报告人查询，返回结果条数(手动调用)
def getItems(project,issuetype,status,created,assignee,reporter,orderby):
    #拼接语句
    search_str=''
    if project!=None:
        search_str+='project in ('+','.join(project)+')  '
    if issuetype!=None:
        search_str+='AND issuetype in ('+','.join(issuetype)+') '
    if status!=None:
        search_str+='AND status in ('+','.join(status)+') '
    if created != None:
        search_str += 'AND created >='+created[0]+' AND  created <='+created[1]+' '
    if reporter != None:
        search_str += 'AND reporter in (' + ','.join(reporter) + ') '
    if assignee != None:
        search_str += 'AND assignee in (' + ','.join(assignee) + ') '
    if orderby != None:
        search_str += 'ORDER BY ' + ','.join(orderby) + ' DESC'

    #执行jira查询
    result=jira.search_issues(search_str, maxResults=999999)

    total=len(result)
    resdict=dict(total=total,result=result)
    return resdict

#计算bug修复率-传入请求
def getRepairedRrate(request):
    # 从请求中取筛选条件，未传入的条件为None，查询某项目/某段时间/某个提出人/某个开发/的bug修复率
    if request.method == "POST":
        project = request.POST.get('project').split(',') if request.POST.get('project') != None else None
        created = request.POST.get('created').split(',') if request.POST.get('created') != None else None
        assignee = request.POST.get('assignee').split(',') if request.POST.get('assignee') != None else None
        reporter = request.POST.get('reporter').split(',') if request.POST.get('reporter') != None else None
        orderby = request.POST.get('orderby').split(',') if request.POST.get('orderby') != None else None
    #拼接语句
    strAllBugs=''  #全部bug
    strRepairedBugs=''  #已修复bug
    if project!=None:
        strAllBugs+='project in ('+','.join(project)+')  '
        strRepairedBugs+='project in ('+','.join(project)+')  '

    strAllBugs += 'AND issuetype =bug '
    strRepairedBugs += 'AND issuetype = bug '

    strAllBugs += 'AND status in (active, Reopened, Resolved, Closed, verified, integrated, postponed, "PM Confirmed", rejected, duplicated)  '
    strRepairedBugs += 'AND status in (Resolved, Closed, verified, integrated, "PM Confirmed", rejected) '

    if created != None:
        strAllBugs += 'AND created >='+created[0]+' AND  created <='+created[1]+' '
        strRepairedBugs += 'AND created >='+created[0]+' AND  created <='+created[1]+' '
    if reporter != None:
        strAllBugs += 'AND reporter in (' + ','.join(reporter) + ') '
        strRepairedBugs += 'AND reporter in (' + ','.join(reporter) + ') '
    if assignee != None:
        strAllBugs += 'AND assignee in (' + ','.join(assignee) + ') '
        strRepairedBugs += 'AND assignee in (' + ','.join(assignee) + ') '
    if orderby != None:
        strAllBugs += 'ORDER BY ' + ','.join(orderby) + ' DESC'
        strRepairedBugs += 'ORDER BY ' + ','.join(orderby) + ' DESC'


    #执行jira查询
    resultAll=jira.search_issues(strAllBugs, maxResults=999999)
    countAll=len(resultAll)
    resultRepaired = jira.search_issues(strRepairedBugs, maxResults=999999)
    countRepaired = len(resultRepaired)

    #计算bug修复率
    repairedRrate=round(countRepaired/countAll*100,2)
    return repairedRrate


#一个接口，返回某个项目在某段时间内，总bug修复率、按qa分类修复率、按rd分类修复率
#传入参数为项目+日期
def getRepairedRrateByGroupBK(request):
    #先查询该时间段内所有的bug，
    # 根据项目、问题类型、活动状态、创建日期、报告人查询，返回结果条数(手动调用)
    #def getItems(project, issuetype, status, created, assignee, reporter, orderby)

    try:
        responseData={}
        if request.method == "POST":
            project = request.POST.get('project').split(',') if request.POST.get('project') != None else None
            created = request.POST.get('created').split(' - ') if request.POST.get('created') != None else None
        else:
            project=['UAC']
            created=['2019-01-01','2019-01-30']

        # 认为是"已修复"的状态
        fixStatus = ['Resolved', 'Closed', 'verified', 'integrated', '\"PM Confirmed\"', 'rejected','duplicated']
        #未修复状态
        unFixStatus=['active', 'Reopened', 'postponed' ]
        # 所有状态
        #allStatus=['Resolved', 'Closed', 'verified', 'integrated', '\"PM Confirmed\"', 'rejected','active', 'Reopened', 'postponed', 'duplicated' ]
        #曲线图数据-每天新提的bug量，截止到当天未关闭的bug量
        bugsAllByDay={}
        bugsUnFixByDay={}
        # 把时间范围拆开
        startDate = created[0]
        endDate = created[1]
        date_start = datetime.datetime.strptime(startDate, '%Y-%m-%d').date()
        date_end = datetime.datetime.strptime(endDate, '%Y-%m-%d').date()
        date_end_next=str(date_end+datetime.timedelta(days=1)) #多加一天，否则无法查到最后一天当天的数据
        created[1]=date_end_next
        for i in range((date_end - date_start).days + 1):
            day1 = str(date_start + datetime.timedelta(days=i))
            day2 = str(date_start + datetime.timedelta(days=i+1))
            #print(day)
            # 当天创建的bug数量
            bugsAllByDayItem = getItems(project, ['bug'], None, [day1,day2], None, None, ['created'])
            bugsAllByDay_single = bugsAllByDayItem['total']
            bugsAllByDay[day1] =bugsAllByDay_single

            #截止到当天未关闭的bug量
            bugsUnFixByDayItem = getItems(project, ['bug'], unFixStatus, [day1,day2], None, None, ['created'])
            bugsUnFixByDay_single = bugsUnFixByDayItem['total']
            bugsUnFixByDay[day1]=bugsUnFixByDay_single
        responseData['bugsAllByDay']=bugsAllByDay
        responseData['bugsUnFixByDay']=bugsUnFixByDay


        # 计算总bug修复率
        resdictTotal=getItems(project,['bug'],None,created,None,None,['created'])
        bugsTotal=resdictTotal['total']
        repairedTotal = getItems(project, ['bug'], fixStatus, created, None, None, ['created'])
        bugsRepaired = repairedTotal['total']
        repairedRateTotal=round(bugsRepaired/bugsTotal*100,2) if bugsTotal>0 else 0
        responseData['repairedRateTotal'] = repairedRateTotal

        #计算按qa分组的bug修复率，并统计每个qa此时间段的bug总数
        #获取该项目下的所有qa
        qaRepairedRateDict={} #qa修复率字典，key=姓名，value=bug修复率
        qaAllBugsDict={} #每个qa此时间段的bug总数
        qaUser_object=JiraUser.objects.filter(jRoleId=JiraRole.objects.get(jRole='qa',jProject=project[0]))
        cursor = connection.cursor()
        cursor.execute('select * from app01_book')

        ret = cursor.fetchall()
        for qaUser in qaUser_object:
            qaList = []
            qaList.append(qaUser.name)
            resdictTotal_qa = getItems(project, ['bug'], None, created, None, qaList, ['created'])
            bugsTotal_qa = resdictTotal_qa['total']
            repairedTotal_qa = getItems(project, ['bug'], fixStatus, created, None, qaList, ['created'])#reporter=qa列表
            bugsRepaired_qa = repairedTotal_qa['total']
            rate_qa =round(bugsRepaired_qa / bugsTotal_qa*100, 2) if bugsTotal_qa>0  else 0
            qaRepairedRateDict[qaUser.name]=rate_qa
            qaAllBugsDict[qaUser.name]=bugsTotal_qa
        responseData['qaRepairedRateDict'] = qaRepairedRateDict
        responseData['qaAllBugsDict'] = qaAllBugsDict

        #return qaRepairedRateDict

        # 计算按rd分组的bug修复率
        # 获取该项目下的所有qa
        # rdRepairedRateDict = {}  # rd修复率字典，key=姓名，value=bug修复率
        # rdAllBugsDict = {}  # 每个qa此时间段的bug总数
        # rdUser_object = JiraUser.objects.filter(jRoleId=JiraRole.objects.get(jRole='rd', jProject=project[0]))
        # for rdUser in rdUser_object:
        #     rdList = []
        #     rdList.append(rdUser.name)
        #     resdictTotal_rd = getItems(project, ['bug'], None, created, rdList, None, ['created'])
        #     bugsTotal_rd = resdictTotal_rd['total']
        #     repairedTotal_rd = getItems(project, ['bug'], fixStatus, created, rdList, None,['created'])  # reporter=qa列表
        #     bugsRepaired_rd = repairedTotal_rd['total']
        #     rate_rd = round(bugsRepaired_rd / bugsTotal_rd * 100, 2) if bugsTotal_rd > 0 else 0
        #     rdRepairedRateDict[rdUser.name] = rate_rd
        #     rdAllBugsDict[rdUser.name] = bugsTotal_rd
        # responseData['rdRepairedRateDict'] = rdRepairedRateDict
        # responseData['rdAllBugsDict'] = rdAllBugsDict


        # 柱状图，按qa人的维度统计每个qa的所有状态bug数

        # 获取该项目下的所有qa
        qaRepairedRateDict = {}  # qa修复率字典，key=姓名，value=bug修复率
        qaAllBugsDict = {}  # 每个qa此时间段的bug总数
        qaBugStatusDict={}  #按qa人的维度统计每个qa的所有状态bug数
        qaAllBugsDict_new = {} #按qa人的维度统计每个qa的总bug数
        qaFixBugsDict_new={}    #按qa人的维度统计每个qa的已修复bug数
        qaFixBugsRateDict_new={}    #按qa人的维度统计每个qa的修复率
        qaUser_object = JiraUser.objects.filter(jRoleId=JiraRole.objects.get(jRole='qa', jProject=project[0]))
        qaList = []
        for qaUser in qaUser_object:
            qaList.append(qaUser.name)
            qaAllBugsDict_new[qaUser.name]=0  #初始化
            qaFixBugsDict_new[qaUser.name]=0  #初始化
            qaFixBugsRateDict_new[qaUser.name]=0  #初始化
        statusNumByQa=getStatusNumByPerson(created,project,qaList)
        # for key,value in statusNumByPerson.items():
        #     if(key in fixStatus): #属于已修复
        responseData['statusNumByQa']=statusNumByQa
        responseData['qaList']=qaList

        #方案二：qalist不从数据库取，而是直接从jira拉取到的bug中取，没有提过bug的不显示

        #操作statusNumByQa计算每个qa的bug总数、修复率，这样避免多次查询jira
        #{active = [[人1, num1], [人2, num2]], closed = [[人1, num1], [人2, num2]}


        for key in statusNumByQa:
            person_num_list=statusNumByQa[key]
            for item in person_num_list:
                person=item[0]
                num=item[1]
                qaAllBugsDict_new[person] += num
                if key in fixStatus:
                    qaFixBugsDict_new[person]+=num

        #计算修复率
        for key in qaAllBugsDict_new:
            allnum=qaAllBugsDict_new[key]
            fixnum=qaFixBugsDict_new[key]
            qaFixBugsRateDict_new[key]=(allnum-fixnum)/allnum*100 if allnum!=0 else 0

        responseData['rdRepairedRateDict'] = qaFixBugsRateDict_new
        responseData['rdAllBugsDict'] = qaAllBugsDict_new




        #当前日期时间段内，每种状态的bug所占的比例
        bugStatusDict={}
        #['active', 'Reopened', 'postponed', 'duplicated']
        activeItems=getItems(project,['bug'],['active'],created,None,None,['created'])
        activeCount=activeItems['total']
        reopenedItems = getItems(project, ['bug'], ['Reopened'], created, None, None, ['created'])
        reopenedCount = reopenedItems['total']
        postponedItems = getItems(project, ['bug'], ['postponed'], created, None, None, ['created'])
        postponedCount = postponedItems['total']
        duplicatedItems = getItems(project, ['bug'], ['duplicated'], created, None, None, ['created'])
        duplicatedCount = duplicatedItems['total']

        #['Resolved', 'Closed', 'verified', 'integrated', '\"PM Confirmed\"', 'rejected']
        resolvedItems = getItems(project, ['bug'], ['Resolved'], created, None, None, ['created'])
        resolvedCount = resolvedItems['total']
        closedItems = getItems(project, ['bug'], ['Closed'], created, None, None, ['created'])
        closedCount = closedItems['total']
        verifiedItems = getItems(project, ['bug'], ['verified'], created, None, None, ['created'])
        verifiedCount = verifiedItems['total']
        integratedItems = getItems(project, ['bug'], ['integrated'], created, None, None, ['created'])
        integratedCount = integratedItems['total']
        pmConfirmedItems = getItems(project, ['bug'], ['\"PM Confirmed\"'], created, None, None, ['created'])
        pmConfirmedCount = pmConfirmedItems['total']
        rejectedItems = getItems(project, ['bug'], ['rejected'], created, None, None, ['created'])
        rejectedCount = rejectedItems['total']

        bugStatusDict['active']=activeCount
        bugStatusDict['Reopened']=reopenedCount
        bugStatusDict['postponed']=postponedCount
        bugStatusDict['duplicated']=duplicatedCount
        bugStatusDict['Resolved']=resolvedCount
        bugStatusDict['Closed']=closedCount
        bugStatusDict['verified']=verifiedCount
        bugStatusDict['integrated']=integratedCount
        bugStatusDict['\"PM Confirmed\"']=pmConfirmedCount
        bugStatusDict['rejected']=rejectedCount
        responseData['bugStatusDict'] = bugStatusDict




        strres=json.dumps(responseData)
        #HttpResponse(json.dumps(responseData, ensure_ascii=False), content_type="application/json,charset=utf-8")
        #HttpResponse(json.dumps(responseData), content_type="application/json")
        return HttpResponse(json.dumps(responseData), content_type="application/json")
    except Exception as e:
        #print('save error')
        #print(e.message)
        return -1


##########################################################
def getRepairedRrateByGrouptmp(request):
    #先查询该时间段内所有的bug，
    # 根据项目、问题类型、活动状态、创建日期、报告人查询，返回结果条数(手动调用)
    #def getItems(project, issuetype, status, created, assignee, reporter, orderby)

    try:
        responseData={}
        if request.method == "POST":
            project = request.POST.get('project').split(',') if request.POST.get('project') != None else None
            created = request.POST.get('created').split(' - ') if request.POST.get('created') != None else None
        else:
            project=['UAC']
            created=['2019-01-01','2019-01-30']

        # 认为是"已修复"的状态
        fixStatus = ['Resolved', 'Closed', 'verified', 'integrated', '\"PM Confirmed\"', 'rejected','duplicated']
        #未修复状态
        unFixStatus=['active', 'Reopened', 'postponed' ]
        # 所有状态
        #allStatus=['Resolved', 'Closed', 'verified', 'integrated', '\"PM Confirmed\"', 'rejected','active', 'Reopened', 'postponed', 'duplicated' ]
        #曲线图数据-每天新提的bug量，截止到当天未关闭的bug量
        """bugsAllByDay={}
        bugsUnFixByDay={}
        # 把时间范围拆开
        startDate = created[0]
        endDate = created[1]
        date_start = datetime.datetime.strptime(startDate, '%Y-%m-%d').date()
        date_end = datetime.datetime.strptime(endDate, '%Y-%m-%d').date()
        date_end_next=str(date_end+datetime.timedelta(days=1)) #多加一天，否则无法查到最后一天当天的数据
        created[1]=date_end_next
        for i in range((date_end - date_start).days + 1):
            day1 = str(date_start + datetime.timedelta(days=i))
            day2 = str(date_start + datetime.timedelta(days=i+1))
            #print(day)
            # 当天创建的bug数量
            bugsAllByDayItem = getItems(project, ['bug'], None, [day1,day2], None, None, ['created'])
            bugsAllByDay_single = bugsAllByDayItem['total']
            bugsAllByDay[day1] =bugsAllByDay_single

            #截止到当天未关闭的bug量
            bugsUnFixByDayItem = getItems(project, ['bug'], unFixStatus, [day1,day2], None, None, ['created'])
            bugsUnFixByDay_single = bugsUnFixByDayItem['total']
            bugsUnFixByDay[day1]=bugsUnFixByDay_single
        responseData['bugsAllByDay']=bugsAllByDay
        responseData['bugsUnFixByDay']=bugsUnFixByDay"""


        # 计算每个项目的bug修复率
        repairedRateByProject={}
        for pro in project:
            resdictTotal=getItems(project,['bug'],None,created,None,None,['created'])
            bugsTotal=resdictTotal['total']
            repairedTotal = getItems([pro], ['bug'], fixStatus, created, None, None, ['created'])
            bugsRepaired = repairedTotal['total']
            repairedRateTotal=round(bugsRepaired/bugsTotal*100,2) if bugsTotal>0 else 0
            repairedRateByProject[pro] = repairedRateTotal
        responseData['repairedRateByProject'] = repairedRateByProject

        #获取该项目下的所有qa
        strtmp='('
        for i in range(len(project)-1):
            strtmp+='\''+project[i]+'\','
        strtmp+='\''+project[len(project)-1]+'\')'

        cursor = connection.cursor()
        sql="select distinct u.name from common_jirarole r left join common_jirauser_jRoleId c on r.jRoleId=c.jirarole_id left join common_jirauser u on c.jirauser_id=u.juid where r.jProject in "+strtmp +" and r.jRole='qa'"   #"and r.jRole='qa'"
        cursor.execute(sql)
        qaUser_object = cursor.fetchall()
        """for qaUser in qaUser_object:
                qaList = []
                qaList.append(qaUser[0])
                resdictTotal_qa = getItems(project, ['bug'], None, created, None, qaList, ['created'])
                bugsTotal_qa = resdictTotal_qa['total']
                repairedTotal_qa = getItems(project, ['bug'], fixStatus, created, None, qaList, ['created'])#reporter=qa列表
                bugsRepaired_qa = repairedTotal_qa['total']
                rate_qa =round(bugsRepaired_qa / bugsTotal_qa*100, 2) if bugsTotal_qa>0  else 0
                qaRepairedRateDict[qaUser[0]]=rate_qa
                qaAllBugsDict[qaUser[0]]=bugsTotal_qa
            responseData['qaRepairedRateDict'] = qaRepairedRateDict
            responseData['qaAllBugsDict'] = qaAllBugsDict"""

        # 柱状图，按qa人的维度统计每个qa的所有状态bug数
        qaAllBugsDict_new = {} #按qa人的维度统计每个qa的总bug数
        qaFixBugsDict_new={}    #按qa人的维度统计每个qa的已修复bug数
        qaFixBugsRateDict_new={}    #按qa人的维度统计每个qa的修复率
        qaList = []
        for qaUser in qaUser_object:
            qaList.append(qaUser[0])
            qaAllBugsDict_new[qaUser[0]]=0  #初始化
            qaFixBugsDict_new[qaUser[0]]=0  #初始化
            qaFixBugsRateDict_new[qaUser[0]]=0  #初始化
        statusNumByQa=getStatusNumByPerson(created,project,qaList)
        responseData['statusNumByQa']=statusNumByQa
        responseData['qaList']=qaList

        statusNumByProject = getStatusNumByProject(created, project)
        responseData['statusNumByProject'] = statusNumByProject
        responseData['projectList'] = project

        #操作statusNumByQa计算每个qa的bug总数、修复率，这样避免多次查询jira
        #{active = [[人1, num1], [人2, num2]], closed = [[人1, num1], [人2, num2]}
        for key in statusNumByQa:
            person_num_list=statusNumByQa[key]
            for item in person_num_list:
                person=item[0]
                num=item[1]
                qaAllBugsDict_new[person] += num
                if key in fixStatus:
                    qaFixBugsDict_new[person]+=num

        #计算修复率
        for key in qaAllBugsDict_new:
            allnum=qaAllBugsDict_new[key]
            fixnum=qaFixBugsDict_new[key]
            qaFixBugsRateDict_new[key]=fixnum/allnum*100 if allnum!=0 else 0

        responseData['qaRepairedRateDict'] = qaFixBugsRateDict_new
        responseData['qaAllBugsDict'] = qaAllBugsDict_new




        #当前日期时间段内，每种状态的bug所占的比例
        """bugStatusDict={}
        #['active', 'Reopened', 'postponed', 'duplicated']
        activeItems=getItems(project,['bug'],['active'],created,None,None,['created'])
        activeCount=activeItems['total']
        reopenedItems = getItems(project, ['bug'], ['Reopened'], created, None, None, ['created'])
        reopenedCount = reopenedItems['total']
        postponedItems = getItems(project, ['bug'], ['postponed'], created, None, None, ['created'])
        postponedCount = postponedItems['total']
        duplicatedItems = getItems(project, ['bug'], ['duplicated'], created, None, None, ['created'])
        duplicatedCount = duplicatedItems['total']

        #['Resolved', 'Closed', 'verified', 'integrated', '\"PM Confirmed\"', 'rejected']
        resolvedItems = getItems(project, ['bug'], ['Resolved'], created, None, None, ['created'])
        resolvedCount = resolvedItems['total']
        closedItems = getItems(project, ['bug'], ['Closed'], created, None, None, ['created'])
        closedCount = closedItems['total']
        verifiedItems = getItems(project, ['bug'], ['verified'], created, None, None, ['created'])
        verifiedCount = verifiedItems['total']
        integratedItems = getItems(project, ['bug'], ['integrated'], created, None, None, ['created'])
        integratedCount = integratedItems['total']
        pmConfirmedItems = getItems(project, ['bug'], ['\"PM Confirmed\"'], created, None, None, ['created'])
        pmConfirmedCount = pmConfirmedItems['total']
        rejectedItems = getItems(project, ['bug'], ['rejected'], created, None, None, ['created'])
        rejectedCount = rejectedItems['total']

        bugStatusDict['active']=activeCount
        bugStatusDict['Reopened']=reopenedCount
        bugStatusDict['postponed']=postponedCount
        bugStatusDict['duplicated']=duplicatedCount
        bugStatusDict['Resolved']=resolvedCount
        bugStatusDict['Closed']=closedCount
        bugStatusDict['verified']=verifiedCount
        bugStatusDict['integrated']=integratedCount
        bugStatusDict['\"PM Confirmed\"']=pmConfirmedCount
        bugStatusDict['rejected']=rejectedCount
        responseData['bugStatusDict'] = bugStatusDict"""


        strres=json.dumps(responseData)
        return HttpResponse(json.dumps(responseData), content_type="application/json")
    except Exception as e:
        #print('save error')
        #print(e.message)
        return -1

##########################################

#输入参数：时间、项目、人
#输出参数：[[状态1,num]，[状态2,num]]
# def getStatusNumByPerson(created,project,person):
#     result=[]
#     allStatus=['Resolved', 'Closed', 'verified', 'integrated', '\"PM Confirmed\"', 'rejected','active', 'Reopened', 'postponed', 'duplicated' ]
#     for status in allStatus:
#         items=getItems(project, ['bug'], [status], created, None, None, ['created'])
#         count=items['total']
#         result.append([status,count])
#     return result

# 为方便前端作图，返回值的格式应为如下字典：
# {active=[[人1,num1],[人2,num2]],closed=[[人1,num1],[人2,num2]}
# 输入参数：时间、项目、人
def getStatusNumByPerson(created,project,personList):
    result={}
    allStatus = ['Resolved', 'Closed', 'verified', 'integrated', '\"PM Confirmed\"', 'rejected', 'active', 'Reopened',
                 'postponed', 'duplicated']
    for status in allStatus:
        person_num_List=[]
        for person in personList:
            items=getItems(project, ['bug'], [status], created, None, [person], ['created'])
            person_num_List.append([person,items['total']])
        result[status]=person_num_List
    return result

# 输入参数：时间、项目、人
def getStatusNumByProject(created,projectList):
    result={}
    allStatus = ['Resolved', 'Closed', 'verified', 'integrated', '\"PM Confirmed\"', 'rejected', 'active', 'Reopened',
                 'postponed', 'duplicated']
    for status in allStatus:
        project_num_List=[]
        for project in projectList:
            items=getItems([project], ['bug'], [status], created, None, None, ['created'])
            project_num_List.append([project,items['total']])
        result[status]=project_num_List
    return result





#新思路：先拉取一次，把所有的tiems拉取过来，在内存中分类，而不是借用jira计算

#根据项目、问题类型、活动状态、创建日期、报告人查询，返回items结果集(手动调用)
def getItemsAll(project,issuetype,status,created,assignee,reporter,orderby):
    #拼接语句
    search_str=''
    if project!=None:
        search_str+='project in ('+','.join(project)+')  '
    if issuetype!=None:
        search_str+='AND issuetype in ('+','.join(issuetype)+') '
    if status!=None:
        search_str+='AND status in ('+','.join(status)+') '
    if created != None:
        search_str += 'AND created >='+created[0]+' AND  created <='+created[1]+' '
    if reporter != None:
        search_str += 'AND reporter in (' + ','.join(reporter) + ') '
    if assignee != None:
        search_str += 'AND assignee in (' + ','.join(assignee) + ') '
    if orderby != None:
        search_str += 'ORDER BY ' + ','.join(orderby) + ' DESC'

    #执行jira查询
    result=jira.search_issues(search_str, maxResults=999999)
    return result

def getRepairedRrateByGroup_bk(request):
    try:
        responseData={}
        if request.method == "POST":
            project = request.POST.get('project').split(',') if request.POST.get('project') != None else None
            created = request.POST.get('created').split(' - ') if request.POST.get('created') != None else None
        else:
            project=['UAC']
            created=['2019-01-01','2019-01-30']

        # 认为是"已修复"的状态
        fixStatus = ['resolved', 'closed', 'verified', 'integrated', '\"PM Confirmed\"', 'rejected','duplicated']
        #未修复状态
        unFixStatus=['active', 'Reopened', 'postponed' ]
        # 所有状态
        allStatus = ['resolved', 'closed', 'verified', 'integrated', '\"PM Confirmed\"', 'rejected', 'active',
                     'Reopened',
                     'postponed', 'duplicated','total']
        # 计算每个项目的bug修复率
        #{project1=
        repairedRateByProject = {}
        repairedRateByQa = {}

        statusNumByProject={}
        statusNumByQa={}
        qalistnew=[]

        for status in allStatus:
            statusNumByProject[status]={}
            statusNumByQa[status] = {}
            for pro in project:
                statusNumByProject[status][pro] = 0  # 先初始化

        allItems = getItemsAll(project, ['bug'], None, created, None, None, ['created'])
        for pro in project:
            #{active={"uac"=10,"dap"=20}}
            bugCount=0
            repairedCount=0
            for items in allItems:
                fields=items.fields
                qa=fields.reporter.name
                rd=fields.assignee.name
                status=fields.status.name
                proname=fields.project.name
                #statusNumByProject[status][pro]+=1
                if pro==proname:
                    bugCount+=1
                    statusNumByProject[status][pro] += 1
                    if status in fixStatus:
                        repairedCount+=1
                if qa not in qalistnew:
                    qalistnew.append(qa)
            repairedRateByProject[pro]=round(repairedCount/bugCount*100 if bugCount!=0 else 0)
            statusNumByProject['total'][pro]=bugCount

        for status in allStatus:
            for qa in qalistnew:
                statusNumByQa[status][qa] = 0  # 先初始化
        for qa in qalistnew:
            bugCount = 0
            repairedCount = 0
            for items in allItems:
                fields=items.fields
                qaname=fields.reporter.name
                status=fields.status.name
                #statusNumByQa[status][qa]+=1
                if qa==qaname:
                    bugCount += 1
                    statusNumByQa[status][qa] += 1
                    if status in fixStatus:
                        repairedCount += 1
            repairedRateByQa[qa] = round(repairedCount / bugCount * 100 if bugCount != 0 else 0)
            statusNumByQa['total'][qa] = bugCount

        responseData['projectList'] = project
        responseData['statusNumByProject'] = statusNumByProject
        responseData['repairedRateByProject'] = repairedRateByProject

        responseData['statusNumByQa'] = statusNumByQa
        responseData['qaRepairedRateDict'] = repairedRateByQa
        responseData['qaList'] = qalistnew

        strres = json.dumps(responseData)
        return HttpResponse(json.dumps(responseData), content_type="application/json")


    except Exception as e:
        #print('save error')
        #print(e.message)
        return -1

#按分组计算线下bug的修复率
def getRepairedRrateByGroupOffline(request):
    try:
        allSelect=False
        if request.method == "POST":
            project = request.POST.get('project').split(',') if request.POST.get('project') != None else None
            created = request.POST.get('created').split(' - ') if request.POST.get('created') != None else None
        else:
            project = ['UAC']
            created = ['2019-01-01', '2019-01-30']

        #listPro=list(project)
        if "全选" in project:
            project.remove('全选')
            allSelect = True
        rejson = offlinecalc(project, created,allSelect)
        if rejson!='':
            return HttpResponse(rejson, content_type="application/json")
        else:
            return -1
    except Exception as e:
        return -1

#按分组计算线上bug的修复率
def getRepairedRrateByGroupOnline(request):
    try:
        allSelect = False
        if request.method == "POST":
            project = request.POST.get('project').split(',') if request.POST.get('project') != None else None
            created = request.POST.get('created').split(' - ') if request.POST.get('created') != None else None
        else:
            project = ['UAC']
            created = ['2019-01-01', '2019-01-30']
        if "全选" in project:
            project.remove('全选')
            allSelect = True
        rejson = onlinecalc(project, created,allSelect)
        if rejson!='':
            return HttpResponse(rejson, content_type="application/json")
        else:
            return -1
    except Exception as e:
        return -1

#计算线下修复率的具体方法
def offlinecalc(project,created,allSelect):
    responseData = {}
    try:
        # 认为是"已修复"的状态
        fixStatus = ['resolved', 'closed', 'verified', 'integrated', 'PM Confirmed', 'rejected', 'duplicated']
        # 未修复状态
        unFixStatus = ['active', 'reopened', 'postponed']
        # 所有状态
        allStatus = ['resolved', 'closed', 'verified', 'integrated', 'PM Confirmed', 'rejected', 'active',
                     'reopened',
                     'postponed', 'duplicated', 'total']
        # 计算每个项目的bug修复率
        # {project1=
        repairedRateByProject = {}
        repairedRateByQa = {}

        statusNumByProject = {}
        statusNumByQa = {}
        qalistnew = []
        pronamelist = []



        allItems = getItemsAll(project, ['bug'], None, created, None, None, ['created'])

        for items in allItems:
            fields = items.fields
            proname = fields.project.name
            if proname not in pronamelist:
                pronamelist.append(proname)  #有数据的项目

        for status in allStatus:
            statusNumByProject[status] = {}
            statusNumByQa[status] = {}
            if allSelect==False:
                pronamelist.clear()
                pronamelist=project[:]   #如果不是全选，就显示每个项目。否则只显示有数据的项目
            #for pro in project:    #显示每个选中的项目
            for pro in pronamelist:
                statusNumByProject[status][pro] = 0  # 先初始化

        #for pro in project:  #显示每个选中的项目
        for pro in pronamelist:
            # {active={"uac"=10,"dap"=20}}
            bugCount = 0
            repairedCount = 0
            for items in allItems:
                fields = items.fields
                qa = fields.reporter.name
                rd = fields.assignee.name
                status = fields.status.name
                proname = fields.project.name
                # statusNumByProject[status][pro]+=1
                if pro == proname:
                    bugCount += 1
                    statusNumByProject[status][pro] += 1
                    if status in fixStatus:
                        repairedCount += 1
                if qa not in qalistnew:
                    qalistnew.append(qa)
            repairedRateByProject[pro] = round(repairedCount / bugCount * 100 if bugCount != 0 else 0)
            statusNumByProject['total'][pro] = bugCount

        for status in allStatus:
            for qa in qalistnew:
                statusNumByQa[status][qa] = 0  # 先初始化
        for qa in qalistnew:
            bugCount = 0
            repairedCount = 0
            for items in allItems:
                fields = items.fields
                qaname = fields.reporter.name
                status = fields.status.name
                # statusNumByQa[status][qa]+=1
                if qa == qaname:
                    bugCount += 1
                    statusNumByQa[status][qa] += 1
                    if status in fixStatus:
                        repairedCount += 1
            repairedRateByQa[qa] = round(repairedCount / bugCount * 100 if bugCount != 0 else 0)
            statusNumByQa['total'][qa] = bugCount

        responseData['projectList'] = project
        responseData['statusNumByProject'] = statusNumByProject
        responseData['repairedRateByProject'] = repairedRateByProject

        responseData['statusNumByQa'] = statusNumByQa
        responseData['qaRepairedRateDict'] = repairedRateByQa
        responseData['qaList'] = qalistnew

        return json.dumps(responseData)

        #return HttpResponse(json.dumps(responseData), content_type="application/json")

    except Exception as e:
        return ''

#计算线上修复率的具体方法
def onlinecalc(project,created,allSelect):
    responseData = {}
    try:
        # 认为是"已修复"的状态
        fixStatus = ['resolved', 'closed', 'verified', 'integrated', 'PM Confirmed', 'rejected', 'duplicated']
        # 未修复状态
        unFixStatus = ['active', 'reopened', 'postponed']
        # 所有状态
        allStatus = ['resolved', 'closed', 'verified', 'integrated', 'PM Confirmed', 'rejected', 'active',
                     'reopened',
                     'postponed', 'duplicated', 'total']
        # 计算每个项目的bug修复率
        repairedRateByProject = {}
        repairedRateByQa = {}

        statusNumByProject = {}
        statusNumByQa = {}
        qalistnew = []

        pronamelist=[]#线上问题的项目（模块）列表

        allItems = getItemsAll(['XSWT'], ['bug'], None, created, None, None, ['created'])
        #allItems = getItemsAll(project, ['bug'], None, created, None, None, ['created'])


        for items in allItems:
            fields = items.fields
            proname = fields.components[0].name
            if proname not in pronamelist:
                pronamelist.append(proname)

        for status in allStatus:
            statusNumByProject[status] = {}
            statusNumByQa[status] = {}
            if allSelect==False:
                pronamelist.clear()
                pronamelist=project[:]   #如果不是全选，就显示每个项目。否则只显示有数据的项目
            for pro in pronamelist:         #project：全部显示
                statusNumByProject[status][pro] = 0  # 先初始化

        #如果全部显示，项目太多，仅显示有线上bug的
        for pro in pronamelist:       #for pro in pronamelist:  全部显示
            # {active={"uac"=10,"dap"=20}}
            bugCount = 0
            repairedCount = 0
            for items in allItems:
                fields = items.fields
                qa = fields.reporter.name
                rd = fields.assignee.name
                status = fields.status.name
                #proname = fields.project.name
                proname=fields.components[0].name
                # statusNumByProject[status][pro]+=1
                if pro == proname:
                    bugCount += 1
                    statusNumByProject[status][pro] += 1
                    if status in fixStatus:
                        repairedCount += 1
                if qa not in qalistnew:
                    qalistnew.append(qa)
            repairedRateByProject[pro] = round(repairedCount / bugCount * 100 if bugCount != 0 else 0)
            statusNumByProject['total'][pro] = bugCount

        for status in allStatus:
            for qa in qalistnew:
                statusNumByQa[status][qa] = 0  # 先初始化
        for qa in qalistnew:
            bugCount = 0
            repairedCount = 0
            for items in allItems:
                fields = items.fields
                qaname = fields.reporter.name
                status = fields.status.name
                # statusNumByQa[status][qa]+=1
                if qa == qaname:
                    bugCount += 1
                    statusNumByQa[status][qa] += 1
                    if status in fixStatus:
                        repairedCount += 1
            repairedRateByQa[qa] = round(repairedCount / bugCount * 100 if bugCount != 0 else 0)
            statusNumByQa['total'][qa] = bugCount

        responseData['projectList'] = project
        responseData['statusNumByProject'] = statusNumByProject
        responseData['repairedRateByProject'] = repairedRateByProject

        responseData['statusNumByQa'] = statusNumByQa
        responseData['qaRepairedRateDict'] = repairedRateByQa
        responseData['qaList'] = qalistnew

        return json.dumps(responseData)

        #return HttpResponse(json.dumps(responseData), content_type="application/json")

    except Exception as e:
        return ''