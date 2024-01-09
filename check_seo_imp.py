from distutils.log import error
from operator import contains, truediv
from queue import Empty
from select import select
from tkinter.tix import Tree
from xml import dom
import requests
from lxml import html
import sys
import email.utils as eut
import validators
from validators import ValidationFailure
from urllib.parse import urlparse
from collections import Counter
import re
from urllib.parse import parse_qs
import copy


class InPageSeoAudit:

    def __init__(self, url_):
        self.url = url_
        self.resp = requests.get(self.url)
        self.urls = []
        self.internal_links = []
        self.external_links = []
        if self.resp.ok:
            print("HTML fetched successfully!")
            self.element_tree = html.fromstring(self.resp.text)
            self.get_links()
        else:
            print("Could not fetch HTML! {}".format(self.resp.status_code))
            print(self.resp.text)

    def get_links(self):
        try:
            tree_urls = self.element_tree.xpath('//a/@href')
            for url in tree_urls:
                self.urls.append(url)

            # get all the internal and external links
            domain = urlparse(self.url).netloc
            self.internal_links.append(self.url)
            for url in self.urls:
                if domain == urlparse(url).netloc:
                    self.internal_links.append(url)
                elif "http" in url or "www." in url:
                    self.external_links.append(url)
        except Exception as e:
            print(e)

    ######################### CODE VALIDATION #########################

    def page_has_tags_with_style_attr(self):
        page_has_tags_with_style_attr = False
        try:
            tree_style = self.element_tree.xpath('//*/@style')
            if len(tree_style) > 0:
                page_has_tags_with_style_attr = True
        except Exception as e:
            print(e)
        finally:
            print("page_has_tags_with_style_attr: ",
                  page_has_tags_with_style_attr)
            return page_has_tags_with_style_attr

    def headings_hierarchy_broken(self):
        headings_hierarchy_broken = False
        try:
            tree_h = self.element_tree.xpath('//h1|//h2|//h3|//h4|//h5|//h6')
            headings_list = []
            for h in tree_h:
                headings_list.append(h.tag)
            # check if headings are sorted or not
            sorted_headings_list = copy.deepcopy(headings_list)
            sorted_headings_list.sort()
            if headings_list != sorted_headings_list:
                headings_hierarchy_broken = True
            # check if any heading is missing
            headings_dict = {}
            for heading in headings_list:
                headings_dict[int(heading[1])] = None
            num_headings = len((headings_dict).keys())
            ideal_headings_list = [1, 2, 3, 4, 5, 6]
            headings_list = [*headings_dict]
            if headings_list != ideal_headings_list[:num_headings]:
                headings_hierarchy_broken = True
        except Exception as e:
            print(e)
        finally:
            print("headings_hierarchy_broken: ",
                  headings_hierarchy_broken)
            return headings_hierarchy_broken

    ######################### PAGE SPEED #########################

    def avoid_excessive_dom_size(self):
        avoid_excessive_dom_size = True
        try:
            total_nodes = len(self.element_tree.xpath(".//*"))
            if total_nodes < 1500:
                avoid_excessive_dom_size = False
        except Exception as e:
            print(e)
        finally:
            print("avoid_excessive_dom_size: ", avoid_excessive_dom_size)
            return avoid_excessive_dom_size

    def add_dimensions_to_images(self):
        add_dimensions_to_images = False
        try:
            tree_img = self.element_tree.xpath('//img')
            for img in tree_img:
                if (img.get('height') == None or img.get('height') == "") or (img.get('width') == None or img.get('width') == ""):
                    add_dimensions_to_images = True
                    break
        except Exception as e:
            print(e)
        finally:
            print("add_dimensions_to_images: ", add_dimensions_to_images)
            return add_dimensions_to_images

    ######################### INTERNAL #########################

    def long_urls(self):
        long_urls = False
        for url in self.internal_links:
            if len(url) > 115:
                long_urls = True
                break
        print("long_urls: ", long_urls)
        return long_urls

    def url_has_uppercase(self):
        url_has_uppercase = False
        break_flag = False
        try:
            for url in self.internal_links:
                for char in url:
                    if char.isupper():
                        url_has_uppercase = True
                        break_flag = True
                        break
                if break_flag:
                    break
        except Exception as e:
            print(e)
        finally:
            print("url_has_uppercase: ", url_has_uppercase)
            return url_has_uppercase

    def url_has_non_ascii(self):
        url_has_non_ascii = False
        break_flag = False
        try:
            for url in self.internal_links:
                for char in url:
                    if ord(char) < 0 or ord(char) > 127:
                        url_has_non_ascii = True
                        break_flag = True
                        break
                if break_flag:
                    break
        except Exception as e:
            print(e)
        finally:
            print("url_has_non_ascii: ", url_has_non_ascii)
            return url_has_non_ascii

    ######################### DUPLICATES #########################

    def multiple_h1(self):
        multiple_h1 = False
        try:
            tree_h1 = self.element_tree.xpath('//h1')
            if len(tree_h1) > 1:
                multiple_h1 = True
        except Exception as e:
            print(e)
        finally:
            print("multiple_h1: ", multiple_h1)
            return multiple_h1

    ######################### CONTENT RELEVANCE #########################

    def duplicate_descriptions(self):
        duplicate_descriptions = False
        try:
            tree_desc = self.element_tree.xpath('//meta[@name="description"]')
            if len(tree_desc) > 1:
                duplicate_descriptions = True
        except Exception as e:
            print(e)
        finally:
            print("duplicate_descriptions: ", duplicate_descriptions)
            return duplicate_descriptions

    def is_alt_text_missing(self):
        is_alt_text_missing = False
        try:
            tree_image = self.element_tree.xpath('//img')
            for image in tree_image:
                if (image.get('alt') == None or image.get('alt') == "") and (image.get('role') == None or image.get('role') != "presentation"):
                    is_alt_text_missing = True
        except Exception as e:
            print(e)
        finally:
            print("is_alt_text_missing: ", is_alt_text_missing)
            return is_alt_text_missing

    def is_h1_tag_missing(self):
        is_h1_tag_missing = True
        try:
            tree_title_element = self.element_tree.xpath('//h1')
            if len(tree_title_element) > 0:
                is_h1_tag_missing = False
        except Exception as e:
            print(e)
        finally:
            print("is_h1_tag_missing:", is_h1_tag_missing)
            return is_h1_tag_missing

    def is_p_tag_missing(self):
        is_p_tag_missing = True
        try:
            tree_title_element = self.element_tree.xpath('//p')
            if len(tree_title_element) > 0:
                is_p_tag_missing = False
        except Exception as e:
            print(e)
        finally:
            print("is_p_tag_missing:", is_p_tag_missing)
            return is_p_tag_missing

    def importance_elements_missing(self):
        importance_elements_missing = True
        try:
            tree_imp_element = self.element_tree.xpath('//strong')
            print("tree_imp_element: ", tree_imp_element)
            if len(tree_imp_element) > 0:
                importance_elements_missing = False
        except Exception as e:
            print(e)
        finally:
            print("importance_elements_missing: ", importance_elements_missing)
            return importance_elements_missing

    ######################### INDEXABILITY #########################

    def h1_has_other_tags_inside(self):
        h1_has_other_tags_inside = False
        try:
            tree_h1 = self.element_tree.xpath('//h1')
            for h1 in tree_h1:
                if len(h1.getchildren()) > 0:
                    h1_has_other_tags_inside = True
                    break
        except Exception as e:
            print(e)
        finally:
            print("h1_has_other_tags_inside: ", h1_has_other_tags_inside)
            return h1_has_other_tags_inside

    ######################### LINKS #########################

    def outgoing_malformed_links(self):
        outgoing_malformed_links = False
        try:
            for url in self.internal_links:
                result = validators.url(url)
                if isinstance(result, ValidationFailure):
                    outgoing_malformed_links = True
                    break
        except Exception as e:
            print(e)
        finally:
            print("outgoing_malformed_links: ", outgoing_malformed_links)
            return outgoing_malformed_links

    def anchored_image_no_alt_text(self):
        anchored_image_no_alt_text = False
        break_flag = False
        try:
            tree_a = self.element_tree.xpath('//a')
            domain = urlparse(self.url).netloc
            tree_a_with_img = []
            for a in tree_a:
                if domain in a.get('href'):
                    tree_a_with_img.append(a)

            for a in tree_a_with_img:
                children = a.getchildren()
                for child in children:
                    if child.tag == 'img':
                        if child.get('alt') == "" or child.get('alt') == None:
                            anchored_image_no_alt_text = True
                            break_flag = True
                            break
                if break_flag:
                    break
        except Exception as e:
            print(e)
        finally:
            print("anchored_image_no_alt_text: ", anchored_image_no_alt_text)
            return anchored_image_no_alt_text

    def page_has_more_than_100_internal_links(self):
        page_has_more_than_100_internal_links = False
        try:
            if len(self.internal_links) > 101:
                page_has_more_than_100_internal_links = True
        except Exception as e:
            print(e)
        finally:
            print("page_has_more_than_100_internal_links: ",
                  page_has_more_than_100_internal_links)
            return page_has_more_than_100_internal_links


if __name__ == "__main__":
    url = sys.argv[1]
    check = InPageSeoAudit(url)
    check.page_has_tags_with_style_attr()
    check.headings_hierarchy_broken()
    check.avoid_excessive_dom_size()
    check.add_dimensions_to_images()
    check.long_urls()
    check.url_has_uppercase()
    check.url_has_non_ascii()
    check.multiple_h1()
    check.duplicate_descriptions()
    check.is_alt_text_missing()
    check.is_h1_tag_missing()
    check.is_p_tag_missing()
    check.importance_elements_missing()
    check.h1_has_other_tags_inside()
    check.outgoing_malformed_links()
    check.anchored_image_no_alt_text()
    check.page_has_more_than_100_internal_links()
