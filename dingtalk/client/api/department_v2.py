# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dingtalk.client.api.base import DingTalkBaseAPI


class DepartmentV2(DingTalkBaseAPI):

    def get(self, _id, lang='zh_CN'):
        """
        获取部门详情 (官方未更新，无v2版本新接口)

        详情请参考
        https://ding-doc.dingtalk.com/document/app/queries-department-details

        :param _id: 部门id
        :param lang: 通讯录语言(默认zh_CN，未来会支持en_US)
        :return: 部门列表数据。以部门的order字段从小到大排列
        """
        return self._get(
            '/department/get',
            {'id': _id, 'lang': lang}
        )

    def list(self, dept_id=1, language='zh_CN'):
        """
        获取部门列表（不支持查询多级子部门）

        详情请参考
        https://ding-doc.dingtalk.com/document/app/obtain-the-department-list-v2

        :param dept_id: 父部门id(如果不传，默认部门为根部门，根部门ID为1)
        :param language: 通讯录语言(默认zh_CN)
        :return: 部门列表
        """
        return self._post(
            '/topapi/v2/department/listsub',
            {'dept_id': dept_id, 'language': language},
            result_processor=lambda x: x.get('result', {})
        )

    def iter_depts(self, dept_id=None, fetch_child=True, language='zh_CN'):
        """
        获取部门列表（支持查询多级部门）

        详情请参考
        https://ding-doc.dingtalk.com/document/app/obtain-the-department-list-v2

        :param dept_id: 父部门id(如果不传，默认部门为从根部门开始返回)
        :param fetch_child: 多级查询
        :param language: 通讯录语言(默认zh_CN)
        :return: 部门列表
        """
        if not dept_id:
            dept_info = self.get(1, language)
            dept_info.update({
                'dept_id': dept_info['id'],
            })
            dept_id = dept_info.pop('id')
            yield dept_info

        dept_data = self.list(dept_id, language)
        for dept_info in dept_data:
            yield dept_info

            if fetch_child:
                for dept_info in self.iter_depts(dept_info.get('dept_id'), fetch_child, language):
                    yield dept_info
