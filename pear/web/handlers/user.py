# coding=utf-8

from flask import Blueprint, request, jsonify

from pear.models.crawler import CrawlerDao
from pear.models.user import UserDao
from pear.web.utils.authorize import authorize
from pear.models.user_log import UserLogDao
from pear.utils.const import Crawler_Status

user_router = Blueprint('user', __name__, url_prefix='/user')


@user_router.route('')
@authorize
def get_user_info():
    u_id = request.cookies.get('u_id')
    user = UserDao.get_by_id(u_id)
    if not user:
        return jsonify(), 401
    UserDao.add_visitor_count(u_id)
    return jsonify(user)


@user_router.route('/activity')
@authorize
def get_user_activity():
    u_id = request.cookies.get('u_id')
    crawlers, crawler_total = CrawlerDao.batch_get_by_status(u_id, page=-1)
    _, done_total = CrawlerDao.batch_get_by_status(u_id, page=-1, status=Crawler_Status.DONE)
    logs, logs_total = UserLogDao.get_by_user(u_id)
    return jsonify(
        crawlers={
            'data': crawlers,
            'crawler_total': crawler_total,
            'done_total': done_total
        },
        actions={
            'data': logs,
            'action_total': logs_total
        }
    )
