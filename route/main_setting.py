from .tool.func import *

def main_setting():
    with get_db_connect() as conn:
        li_list = [
            ['main', get_lang(conn, 'main_setting')],
            ['phrase', get_lang(conn, 'text_setting')],
            ['robot', 'robots.txt'],
            ['external', get_lang(conn, 'ext_api_req_set')],
            ['head', get_lang(conn, 'main_head')],
            ['body/top', get_lang(conn, 'main_body')],
            ['body/bottom', get_lang(conn, 'main_bottom_body')],
            ['sitemap_set', get_lang(conn, 'sitemap_management')],
            ['top_menu', get_lang(conn, 'top_menu_setting')],
            ['skin_set', get_lang(conn, 'main_skin_set_default')],
            ['acl', get_lang(conn, 'main_acl_setting')]
        ]

        li_data = ''.join(['<li><a href="/setting/' + str(li[0]) + '">' + li[1] + '</a></li>' for li in li_list])

        return easy_minify(conn, flask.render_template(skin_check(conn),
            imp = [get_lang(conn, 'setting'), wiki_set(conn), wiki_custom(conn), wiki_css([0, 0])],
            data = '<h2>' + get_lang(conn, 'list') + '</h2><ul class="opennamu_ul">' + li_data + '</ul>',
            menu = [['manager', get_lang(conn, 'return')]]
        ))