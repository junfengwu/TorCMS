# -*- coding:utf-8 -*-

import tornado.web
import tornado.escape

import  config
from torlite.core import tools
from torlite.core.base_handler import BaseHandler
from torlite.model.mpost import MPost
from torlite.model.mcatalog import MCatalog
from torlite.model.mspec import SpesubModel
from torlite.model.mpost2catalog import MPost2Catalog


class CatHandler(BaseHandler):
    def initialize(self):

        self.mpost = MPost()
        self.mcat = MCatalog()
        self.cats = self.mcat.query_all()
        self.mspec = SpesubModel()
        self.specs = self.mspec.get_all()
        self.mpost2catalog = MPost2Catalog()

    def get(self, input=''):
        if len(input) > 0:
            ip_arr = input.split(r'/')
        if input == '':
            pass
        elif len(ip_arr) == 1 :
            self.view_cat_new(input)
        elif len(ip_arr) == 2:
            self.view_cat_new(ip_arr[0], ip_arr[1])
        else:
            self.render('/html/404.html')

    def view_cat_new(self, cat_slug, cur_p = ''):
        if cur_p == '':
            current = 1
        else:
            current = int(cur_p)

        cat_rec = self.mcat.get_by_slug(cat_slug)

        num_of_cat = self.mpost2catalog.get_num_by_cat(cat_rec.uid)
        page_num = int(num_of_cat / config.page_num ) + 1

        cat_name = cat_rec.name
        kwd = {
             'cat_name': cat_name,
             'cat_slug': cat_slug,
             'unescape':  tornado.escape.xhtml_unescape,
             'pager': tools.gen_pager(cat_slug, page_num, current),
             'title': cat_name,
        }
        # for x in self.cats:
        #     if x.slug == cat_slug:
        #         search_str = ',{0},'.format(x.id_cat)
        dbdata = self.mpost2catalog.query_slug_by_pager(cat_slug,current)
            # .query_cat_by_pager(search_str, current)


        # infos = self.mpost2catalog.query_slug_by_pager(cat_slug)
        infos = dbdata
        self.render('tplite/catalog/list.html', infos=infos, kwd=kwd)

        # self.render('tplite/post/all2.html',
        #             kwd = kwd,
        #             view=dbdata,
        #             rand_recs = self.get_random(),)
        #             # format_date = tools.format_date)

    def view_cat(self, cat_slug, cur_p=''):
        if cur_p == '':
            current = 1
        else:
            current = int(cur_p)

        cat_rec = self.mcat.get_by_slug(cat_slug)
        num_of_cat = self.mpost.get_num_by_cat(cat_rec.id_cat)
        page_num = int(num_of_cat / config.page_num ) + 1

        cat_name = cat_rec.name
        kwd = {
            'cat_name': cat_name,
            'cat_slug': cat_slug,
            'unescape':  tornado.escape.xhtml_unescape,
            'pager': tools.gen_pager(cat_slug, page_num, current),
            'title': cat_name,
        }
        for x in self.cats:
            if x.slug == cat_slug:
                search_str = ',{0},'.format(x.id_cat)
        dbdata = self.mpost.query_cat_by_pager(search_str, current)
        self.render('tplite/post/all.html',
                    kwd = kwd,
                    view=dbdata,
                    rand_recs = self.get_random(),
                    format_date = tools.format_date)



    def get_random(self):
        return self.mpost.query_random()