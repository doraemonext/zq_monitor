# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_migrate

from monitor.models import Category, User, Plugin, Record, RecordQueue


def init_monitor_table(sender, **kwargs):
    category_lecture = Category.objects.create(name='讲座')
    category_notify = Category.objects.create(name='通知')
    category_movie = Category.objects.create(name='电影')

    monitor_user = User.objects.create(nickname='自强抓取邮箱', email='zq_monitor@126.com')
    monitor_user.category.add(category_lecture)
    monitor_user.category.add(category_notify)
    monitor_user.category.add(category_movie)

    Plugin.objects.create(category=category_lecture, name='武大官网', iden='lecture_www_whu_edu_cn', url='http://www.whu.edu.cn/tzgg.htm', status=True)
    Plugin.objects.create(category=category_lecture, name='数学与统计学院', iden='lecture_maths_whu_edu_cn', url='http://maths.whu.edu.cn/kexueyanjiu/xueshujiangzuo/', status=True)
    Plugin.objects.create(category=category_lecture, name='经济与管理学院', iden='lecture_ems_whu_edu_cn', url='http://ems.whu.edu.cn/jrlj/jz/', status=True)
    Plugin.objects.create(category=category_lecture, name='法学院', iden='lecture_fxy_whu_edu_cn', url='http://fxy.whu.edu.cn/archive/category/10007-1', status=True)
    Plugin.objects.create(category=category_lecture, name='化学与分子学院', iden='lecture_chem_whu_edu_cn', url='http://www.chem.whu.edu.cn/kxyj/xsjl.htm', status=True)
    Plugin.objects.create(category=category_lecture, name='资源与环境科学学院', iden='lecture_sres_whu_edu_cn', url='http://sres.whu.edu.cn/list.asp?Class_Fid=5&lg_Type=0&Class_id=34', status=True)
    Plugin.objects.create(category=category_lecture, name='政治与公共管理学院', iden='lecture_pspa_whu_edu_cn', url='http://www.pspa.whu.edu.cn/zhkx/', status=True)
    Plugin.objects.create(category=category_lecture, name='生命科学学院', iden='lecture_bio_whu_edu_cn', url='http://www.bio.whu.edu.cn/news.asp?cid=144', status=True)
    Plugin.objects.create(category=category_lecture, name='遥感信息工程学院1', iden='lecture_rsgis_whu_edu_cn_1', url='http://rsgis.whu.edu.cn/index.php?m=content&c=index&a=lists&catid=123', status=True)
    Plugin.objects.create(category=category_lecture, name='遥感信息工程学院2', iden='lecture_rsgis_whu_edu_cn_2', url='http://rsgis.whu.edu.cn/index.php?m=content&c=index&a=lists&catid=125', status=True)
    Plugin.objects.create(category=category_lecture, name='城市设计学院', iden='lecture_sud_whu_edu_cn', url='http://sud.whu.edu.cn/category/lecture', status=True)
    Plugin.objects.create(category=category_lecture, name='计算机学院', iden='lecture_cs_whu_edu_cn', url='http://cs.whu.edu.cn/a/xueshujiangzuofabu/', status=True)
    Plugin.objects.create(category=category_lecture, name='动力与机械学院', iden='lecture_pmc_whu_edu_cn', url='http://pmc.whu.edu.cn/list/4', status=True)
    Plugin.objects.create(category=category_lecture, name='刑事法研究中心', iden='lecture_crimlaw_whu_edu_cn', url='http://crimlaw.whu.edu.cn/Plus/m_default/Cms/docList.php?Aliases=publish', status=True)
    Plugin.objects.create(category=category_lecture, name='药学院', iden='lecture_pharm_whu_edu_cn', url='http://www.pharm.whu.edu.cn/zxzx.asp?sort=zxzx_xsky', status=True)
    Plugin.objects.create(category=category_lecture, name='外国语言文学院', iden='lecture_fls_whu_edu_cn', url='http://fls.whu.edu.cn/index.php/index/show/tid/103.html', status=True)
    Plugin.objects.create(category=category_lecture, name='基础医学院', iden='lecture_wbm_whu_edu_cn', url='http://wbm.whu.edu.cn/category/cat-xkky/kydt', status=True)
    Plugin.objects.create(category=category_lecture, name='土木建筑工程学院', iden='lecture_civ_whu_edu_cn', url='http://civ.whu.edu.cn/kxyj/xsjl/', status=True)
    Plugin.objects.create(category=category_lecture, name='环境法研究所', iden='lecture_riel_whu_edu_cn', url='http://www.riel.whu.edu.cn/list.asp?cid=13', status=True)
    Plugin.objects.create(category=category_lecture, name='物理科学与技术学院', iden='lecture_physics_whu_edu_cn', url='http://physics.whu.edu.cn/xueshu/', status=True)
    Plugin.objects.create(category=category_lecture, name='哲学学院', iden='lecture_philosophy_whu_edu_cn', url='http://philosophy.whu.edu.cn/04/01/', status=True)
    Plugin.objects.create(category=category_lecture, name='国学院', iden='lecture_guoxue_whu_edu_cn', url='http://guoxue.whu.edu.cn/index.php/news/index/cateid/2', status=True)
    Plugin.objects.create(category=category_lecture, name='新闻与传播学院', iden='lecture_journal_whu_edu_cn', url='http://journal.whu.edu.cn/academic/news/index', status=True)
    Plugin.objects.create(category=category_lecture, name='艺术学系', iden='lecture_art_whu_edu_cn', url='http://art.whu.edu.cn/index/note/', status=True)
    Plugin.objects.create(category=category_lecture, name='历史学院', iden='lecture_history_whu_edu_cn', url='http://www.history.whu.edu.cn/about.asp?type=183', status=True)
    Plugin.objects.create(category=category_lecture, name='社会学系', iden='lecture_shxx_whu_edu_cn', url='http://shxx.whu.edu.cn/site/shxx/ShowClass.jsp?id=1202', status=True)
    Plugin.objects.create(category=category_lecture, name='水利水电学院', iden='lecture_swrh_whu_edu_cn', url='http://swrh.whu.edu.cn/Notices/', status=True)
    Plugin.objects.create(category=category_lecture, name='电子信息学院', iden='lecture_eis_whu_edu_cn', url='http://eis.whu.edu.cn/channels/94.html', status=True)
    Plugin.objects.create(category=category_lecture, name='测绘学院', iden='lecture_sgg_whu_edu_cn', url='http://main.sgg.whu.edu.cn/keyan/kyhd/', status=True)

    Plugin.objects.create(category=category_movie, name='梅操电影', iden='movie_vhost_whu_edu_cn', url='http://vhost.whu.edu.cn/gh/xywh.php?Class_Type=0&Class_ID=42', status=True)

    Plugin.objects.create(category=category_notify, name='武大官网', iden='notify_whu_edu_cn', url='http://www.whu.edu.cn/tzgg.htm', status=True)
    Plugin.objects.create(category=category_notify, name='保卫部', iden='notify_sub_whu_edu_cn', url='http://sub.whu.edu.cn/protect/gzdt/', status=True)
    Plugin.objects.create(category=category_notify, name='考试中心', iden='notify_exam_whu_edu_cn', url='http://exam.whu.edu.cn/News/zhks/', status=True)
    Plugin.objects.create(category=category_notify, name='一站式', iden='notify_yzs_whu_edu_cn', url='http://yzs.whu.edu.cn/article/?s=信息发布', status=True)
    Plugin.objects.create(category=category_notify, name='学工部', iden='notify_xgb_whu_edu_cn', url='http://xgb.whu.edu.cn/list.asp?id=45', status=True)
    Plugin.objects.create(category=category_notify, name='校医院', iden='notify_hospital_whu_edu_cn', url='http://hospital.whu.edu.cn/tiltelist.aspx?Newstype=1', status=True)
    Plugin.objects.create(category=category_notify, name='武装部1', iden='notify_rwb_whu_edu_cn_1', url='http://rwb.whu.edu.cn/list.asp?id=49', status=True)
    Plugin.objects.create(category=category_notify, name='武装部2', iden='notify_rwb_whu_edu_cn_2', url='http://rwb.whu.edu.cn/list.asp?id=45', status=True)
    Plugin.objects.create(category=category_notify, name='网络中心', iden='notify_nic_whu_edu_cn', url='http://nic.whu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=9382', status=True)
    Plugin.objects.create(category=category_notify, name='国际交流部', iden='notify_oir_whu_edu_cn', url='http://oir.whu.edu.cn/list/?33_1.html', status=True)
    Plugin.objects.create(category=category_notify, name='后勤保障部', iden='notify_hqbzb_whu_edu_cn', url='http://hqbzb.whu.edu.cn/tzgg.htm', status=True)
    Plugin.objects.create(category=category_notify, name='实验室与设备管理处', iden='notify_lab_whu_edu_cn', url='http://lab.whu.edu.cn/tzgg/', status=True)


class MonitorAppConfig(AppConfig):
    name = 'monitor'

    def ready(self):
        post_migrate.connect(init_monitor_table, sender=self)
