import json

from django.shortcuts import HttpResponse

DATA = {}


def upload(requests):
    """
    上传客户端id和分数
    return: 上传状态和上传信息
    """
    client_id = requests.GET.get('client_id')
    grade = requests.GET.get('grade')
    try:
        if not grade or not client_id:
            raise ValueError
        grade = int(grade)
        client_id = int(client_id)
        if grade < 1 or grade > 10000000:
            raise ValueError
    except Exception:
        return HttpResponse(json.dumps({"status": 0, "data": {}}),
                            content_type='application/json')
    DATA[client_id] = grade

    result = {
        "status": 1,
        "data": {client_id: DATA[client_id]}
    }
    return HttpResponse(json.dumps(result), content_type='application/json')


def query_top(requests):
    """查询当前客户端排行榜"""
    ret = {'status': 0, "data": []}

    client_id = requests.GET.get('client_id')
    try:
        if not client_id:
            raise ValueError
        client_id = int(client_id)
    except Exception:
        return HttpResponse(json.dumps(ret), content_type='application/json')
    data = sorted(DATA.items(),  key=lambda d: d[1], reverse=True)
    result = []
    cur_client_id = {}
    for i, v in enumerate(data):
        if i < 10:
            result.append({
                'no': i + 1,
                'client_id': v[0],
                'grade': v[1]
            })
        if v[0] == client_id:
            cur_client_id['no'] = i + 1
            cur_client_id['client_id'] = client_id
            cur_client_id['grade'] = v[1]
    # 当前客户端是否在top10中
    in_flag = False
    for j in result:
        if j['client_id'] == client_id:
            in_flag = True
    # 不在的添加到末尾
    if not in_flag:
        result.append(cur_client_id)

    ret.update({'status': 1, "data": result})
    return HttpResponse(json.dumps(ret), content_type='application/json')
