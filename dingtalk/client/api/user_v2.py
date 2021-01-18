# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dingtalk.client.api.base import DingTalkBaseAPI


class UserV2(DingTalkBaseAPI):
    def get_user_count(self, only_active):
        """
        获取企业员工人数
        
        详情请参考
        https://ding-doc.dingtalk.com/document/app/obtain-the-number-of-employees-v2

        :param only_active: 是否包含未激活钉钉的人员数量
        :return: 企业员工数量
        """
        return self._post(
            '/topapi/user/count',
            {'only_active': only_active},
            result_processor=lambda x: x.get('result', {'count': 0})['count']
        )
        
    def list(self, dept_id, cursor=0, size=100, order='modify_desc', contain_access_limit=True, language='zh_CN'):
        """
        获取部门成员（详情）
        
        详情请参考
        https://ding-doc.dingtalk.com/document/app/queries-the-complete-information-of-a-department-user

        :param dept_id: 获取的部门id
        :param cursor: 偏移量
        :param size: 表分页大小，最大100
        :param order_field: 排序规则
                      entry_asc     代表按照进入部门的时间升序
                      entry_desc    代表按照进入部门的时间降序
                      modify_asc    代表按照部门信息修改时间升序
                      modify_desc   代表按照部门信息修改时间降序
                      custom        代表用户定义排序
        :param contain_access_limit 是否返回访问受限的员工
        :param language: 通讯录语言(默认zh_CN另外支持en_US)
        :return: result节点内容
        """
        return self._post(
            '/topapi/v2/user/list',
            {
                'dept_id': dept_id,
                'cursor': cursor,
                'size': size,
                'order': order,
                'contain_access_limit': contain_access_limit,
                'language': language
            },
            result_processor=lambda x: x.get('result', {})
        )
        
    def iter_users(self, dept_id, first_cursor=0, order='modify_desc', contain_access_limit=True, language='zh_CN'):
        """
        获取部门成员（详情）
        
        详情请参考
        https://ding-doc.dingtalk.com/document/app/queries-the-complete-information-of-a-department-user

        :return: 返回一个迭代器，可以用for进行循环，得到部门成员详情
        """
        while True:
            user_data = self.list(dept_id, first_cursor, 100, order, contain_access_limit, language)
            first_cursor = user_data.get('next_cursor')
            for user_info in user_data["list"]:
                yield user_info
            if not first_cursor:
                return