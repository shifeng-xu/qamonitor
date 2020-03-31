
import requests
from jira import JIRA
from common.models import JiraRole,JiraUser,Component
import json
from django.shortcuts import render

#获取jira数据有两种方式：1.直接调用API，2.通过request登录jira，模拟浏览器请求url获取数据

# 连接jira，全局
jira = JIRA("http://jira.doglobal.cn", basic_auth=("xushifeng", "***"))
#用于登录jira的报文头，包含cookie
header1=''

def jiraLogin():
    url = "http://jira.doglobal.cn/login.jsp"
    payload = {"os_username": "xushifeng",
    "os_password": "***",
    "os_cookie": True,
     "os_destination": "",
    "user_role": "",
     "atl_token": "",
    "login": "登录"}
    re = requests.post(url, data=payload, allow_redirects=False)
    cookieJsessionId = re.headers["Set-Cookie"].split(";")[0]

    url1 = "http://jira.doglobal.cn/"
    re1 = requests.get(url1)

    cookie1 = re1.headers["Set-Cookie"].split(";")
    cookieToken = cookie1[0].replace("lout", "lin")

    #构造查询接口的的cookie：

    cookieSearch = "jira.editor.user.mode=wysiwyg;" + cookieJsessionId + ";" + cookieToken

    #构造header，header里面这两个是必填项，否则会400和404错误
    global header1
    header1 = {"Cookie": cookieSearch,
               "X-Atlassian-Token": "no-check"
               }

    #发送请求
    #url2 = "http://jira.doglobal.cn/rest/api/2/project/10414/role/10002"
    #data1 = {
    #    "startIndex": 0,
    #    "jql": "project = SMPT AND resolution = Unresolved AND creator in (currentUser()) ORDER BY priority DESC, updated DESC",
    #    "layoutKey": "list-view"
    #}
    #re = requests.post(url2, data=data1, headers=header1)

def getJiraUrl(url):
    try:
        jiraLogin()
        global header1
        resp = requests.get(url, headers=header1)
        return resp.text
    except Exception as e:
        print('save error')
        print(e.message)
        return ''

#定时任务：更新项目角色，定时查询jira，并保存到本地数据库，可一天一次

def getjRoles(request):
    try:
        #查询所有的项目
        res=''
        for pro in jira.projects():
            if pro.name!='':#目前先只做uac项目
                roledir=jira.project_roles(pro)
                for key_role,value_list in roledir.items():
                    jirarole = JiraRole()
                    jirarole.jProject=pro.name
                    jirarole.jRole=key_role
                    #value_list也是字典
                    for value_key,value_value in value_list.items():
                        if value_key=='id':
                            jirarole.jRoleId=value_value
                        if value_key=='url':
                            jirarole.jUrl=value_value
                    jirarole.save()

        return 0
    except Exception as e:
        print('save error')
        return -1


#定时任务，更新每个角色的人员信息，定时查询jira，并保存到本地数据库，可一天一次
def getjUsers():
    try:
        jirarole=JiraRole.objects.all()
        for entity in jirarole:
            url=entity.jUrl
            res=getJiraUrl(url)
            juserinfo=json.loads(res)
            actors=juserinfo['actors']
            jRoleId_tmp=juserinfo['id']
            roleName_tmp=juserinfo['name']
            jrole = JiraRole()
            jrole.jRoleId=jRoleId_tmp

            #actors
            for item in actors:
                juid_tmp=item['id']
                juser = JiraUser()
                juser.juid = str(juid_tmp)
                juser.displayName=item['displayName']
                juser.type=item['type']
                juser.name=item['name']
                juser.avatarUrl=item['avatarUrl']
                # 保存JiraUser表，JiraRole_User表
                juser.save()
                jirarole_obj = JiraRole.objects.filter(jRoleId=jRoleId_tmp)
                juser.jRoleId.clear()
                juser.jRoleId.set(jirarole_obj)
                juser.save()

        return 0
    except Exception as e:
        print('save error')
        #print(e.message)
        return -1


def getComponents(request):
    # This code sample uses the 'requests' library:
    # http://docs.python-requests.org
    # import requests
    # from requests.auth import HTTPBasicAuth
    # import json
    #
    # url = "/rest/api/3/project/{projectIdOrKey}/components"
    #
    # auth = HTTPBasicAuth("email@example.com", "<api_token>")
    #
    # headers = {
    #     "Accept": "application/json"
    # }
    #
    # response = requests.request(
    #     "GET",
    #     url,
    #     headers=headers,
    #     auth=auth
    # )
    #
    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    try:
        jiraLogin()
        global header1
        # 获取当前用户所有项目，返回项目列表
        projectIdList = []
        for j in jira.projects():
            projectIdList.append(j.id)
            if(j.name!='线上问题'):
                continue
            url = "http://jira.doglobal.cn/rest/api/2/project/"+str(j.id)+"/components"
            resp = requests.get(url, headers=header1)
            params_json = json.loads(resp.text)
            for item in params_json:
                component=Component()
                component.name=item['name']
                component.project=item['project']
                component.save()
        #return resp.text
        return render(request, "success.html")
    except Exception as e:
        print('save error')
        print(e.message)
        return ''


# 获取当前用户所有项目，返回项目列表
