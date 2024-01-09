from operator import truediv
from select import select
import requests
from lxml import html
import sys
import email.utils as eut
import validators
from validators import ValidationFailure
from urllib.parse import urlparse


class InPageSeoAudit:

    #################            CONTENT RELEVANCE           ########################
    def __init__(self, url_):
        self.url = url_
        self.resp = requests.get(self.url)
        if self.resp.ok:
            print("HTML fetched successfully!")
            self.element_tree = html.fromstring(self.resp.text)
        else:
            print("Could not fetch HTML! {}".format(self.resp.status_code))
            print(self.resp.text)

    def is_h1_tag_missing(self):
        is_h1_tag_missing = True
        try:
            tree_title_element = self.element_tree.xpath('//h1')[0]
            if tree_title_element != "" or tree_title_element is not None:
                is_h1_tag_missing = False
        except Exception as e:
            print(e)
        finally:
            print("is_h1_tag_missing:", is_h1_tag_missing)
            return is_h1_tag_missing

    def duplicate_h1(self):
        duplicate_h1 = False
        try:
            tree_title_element = self.element_tree.xpath('//h1')
            if len(tree_title_element) > 1:
                for i in range(len(tree_title_element)):
                    for j in range(i+1, len(tree_title_element)):
                        if tree_title_element[i].text_content() == tree_title_element[j].text_content() and i != j:
                            duplicate_h1 = True
                            break
        except Exception as e:
            print(e)
        finally:
            print("duplicate_h1:", duplicate_h1)
            return duplicate_h1

    def is_h2_tag_missing(self):
        is_h2_tag_missing = True
        try:
            tree_title_element = self.element_tree.xpath('//h1')[0]
            if tree_title_element != "" or tree_title_element is not None:
                is_h2_tag_missing = False
        except Exception as e:
            print(e)
        finally:
            print("is_h2_tag_missing:", is_h2_tag_missing)
            return is_h2_tag_missing

    def is_title_tag_missing(self):
        is_title_tag_missing = True
        try:
            tree_title_element = self.element_tree.xpath('//title')[0]
            if tree_title_element != "" or tree_title_element is not None:
                is_title_tag_missing = False
        except Exception as e:
            print(e)
        finally:
            print("is_title_tag_missing:", is_title_tag_missing)
            return is_title_tag_missing

    def is_p_tag_missing(self):
        is_p_tag_missing = True
        try:
            tree_title_element = self.element_tree.xpath('//p')[0]
            if tree_title_element != "" or tree_title_element is not None:
                is_p_tag_missing = False
        except Exception as e:
            print(e)
        finally:
            print("is_p_tag_missing:", is_p_tag_missing)
            return is_p_tag_missing

    def images_present(self):
        images_present = False
        try:
            tree_image = self.element_tree.xpath('count(//img)')
            if tree_image > 0:
                images_present = True
        except Exception as e:
            print(e)
        finally:
            print("images_present: ", images_present)
            return images_present

    def pdf_present(self):
        pdf_present = False
        try:
            tree_image = self.element_tree.xpath(
                'count(//object[@type="application/pdf"])')
            if tree_image > 0:
                pdf_present = True
        except Exception as e:
            print(e)
        finally:
            print("pdf_present: ", pdf_present)
            return pdf_present

    def page_code_has_less_than_500_symbols(self):
        page_code_has_less_than_500_symbols = False
        try:
            # symbol_count = self.resp.text.count('&')
            symbol_count = self.resp.text.count(';')
            if symbol_count > 500:
                page_code_has_less_than_500_symbols = True
        except Exception as e:
            print(e)
        finally:
            print("page_code_has_less_than_500_symbols: ",
                  page_code_has_less_than_500_symbols)
            return page_code_has_less_than_500_symbols

    def is_alt_text_missing(self):
        is_alt_text_missing = False
        try:
            tree_image = self.element_tree.xpath('count(//img)')
            tree_alt = self.element_tree.xpath('count(//img/@alt)')
            if tree_alt != tree_image:
                is_alt_text_missing = True
        except Exception as e:
            print(e)
        finally:
            print("is_alt_text_missing: ", is_alt_text_missing)
            return is_alt_text_missing

    def is_description_missing(self):
        is_description_missing = True
        try:
            tree_desc = self.element_tree.xpath('//meta/@name')[0]
            print(tree_desc)
            if tree_desc == "description":
                is_description_missing = False
        except Exception as e:
            print(e)
        finally:
            print("is_description_missing: ", is_description_missing)
            return is_description_missing

    def is_description_empty(self):
        if self.is_description_missing():
            return True

        is_description_empty = True
        try:
            tree_desc = self.element_tree.xpath(
                '//meta[@name="description"]/@content')[0]
            if tree_desc != "" or tree_desc is not None:
                is_description_empty = False
        except Exception as e:
            print(e)
        finally:
            print("is_description_empty: ", is_description_empty)
            return is_description_empty

    def is_h1_empty(self):
        if self.is_h1_tag_missing():
            return True

        is_h1_empty = True
        try:
            tree_title_element = self.element_tree.xpath(
                '//h1')[0].text_content()
            if tree_title_element != "":
                is_h1_empty = False
        except Exception as e:
            print(e)
        finally:
            print("is_h1_empty: ", is_h1_empty)
            return is_h1_empty

    def is_title_empty(self):
        if self.is_title_tag_missing():
            return True

        is_title_empty = True
        try:
            tree_title_element = self.element_tree.xpath(
                '//title')[0].text_content()
            if tree_title_element != "":
                is_title_empty = False
        except Exception as e:
            print(e)
        finally:
            print("is_title_empty: ", is_title_empty)
            return is_title_empty

    def duplicate_descriptions(self):
        duplicate_descriptions = False
        try:
            tree_desc = self.element_tree.xpath('//meta/@name')
            if len(tree_desc) > 1:
                duplicate_descriptions = True
        except Exception as e:
            print(e)
        finally:
            print("duplicate_descriptions: ", duplicate_descriptions)
            return duplicate_descriptions

    def importance_elements_missing(self):
        importance_elements_missing = True
        try:
            tree_title_element = self.element_tree.xpath('//strong')[0]
            if tree_title_element != "":
                importance_elements_missing = False
        except Exception as e:
            print(e)
        finally:
            print("importance_elements_missing: ", importance_elements_missing)
            return importance_elements_missing

    def alt_tags_with_one_word(self):
        alt_tags_with_one_word = False
        try:
            tree_alt = self.element_tree.xpath('//img/@alt')
            for text in tree_alt:
                if len(text.split()) <= 1:
                    alt_tags_with_one_word = True
                    break
        except Exception as e:
            print(e)
        finally:
            print("alt_tags_with_one_word: ", alt_tags_with_one_word)
            return alt_tags_with_one_word

    def long_description(self):
        if self.is_description_missing():
            return False

        long_description = False
        try:
            tree_desc = self.element_tree.xpath(
                '//meta[@name="description"]/@content')[0]
            if len(tree_desc) > 156:
                long_description = True
        except Exception as e:
            print(e)
        finally:
            print("long_description: ", long_description)
            return long_description

    def h1_starts_with_lowercase(self):
        h1_starts_with_lowercase = True
        try:
            tree_title_element = self.element_tree.xpath(
                '//h1')[0].text_content()
            if tree_title_element[0].islower() == False:
                h1_starts_with_lowercase = False
        except Exception as e:
            print(e)
        finally:
            print("h1_starts_with_lowercase: ", h1_starts_with_lowercase)
            return h1_starts_with_lowercase

    def h2_starts_with_lowercase(self):
        h2_starts_with_lowercase = True
        try:
            tree_title_element = self.element_tree.xpath(
                '//h1')[0].text_content()
            if tree_title_element[0].islower() == False:
                h2_starts_with_lowercase = False
        except Exception as e:
            print(e)
        finally:
            print("h2_starts_with_lowercase: ", h2_starts_with_lowercase)
            return h2_starts_with_lowercase

    def title_starts_with_lowercase(self):
        title_starts_with_lowercase = True
        try:
            tree_title_element = self.element_tree.xpath(
                '//h1')[0].text_content()
            if tree_title_element[0].islower() == False:
                title_starts_with_lowercase = False
        except Exception as e:
            print(e)
        finally:
            print("title_starts_with_lowercase: ", title_starts_with_lowercase)
            return title_starts_with_lowercase

    def h1_too_long(self):
        h1_too_long = False
        try:
            tree_title_element = self.element_tree.xpath(
                '//h1')[0].text_content()
            if len(tree_title_element) > 70:
                h1_too_long = True
        except Exception as e:
            print(e)
        finally:
            print("h1_too_long: ", h1_too_long)
            return h1_too_long

    def h1_too_short(self):
        h1_too_short = False
        try:
            tree_title_element = self.element_tree.xpath(
                '//h1')[0].text_content()
            if len(tree_title_element) < 20:
                h1_too_short = True
        except Exception as e:
            print(e)
        finally:
            print("h1_too_short: ", h1_too_short)
            return h1_too_short

    def boldface_elements_missing(self):
        boldface_elements_missing = True
        try:
            tree_title_element = self.element_tree.xpath(
                '//b')[0].text_content()
            print("tree: ", tree_title_element)
            if tree_title_element != "":
                boldface_elements_missing = False
        except Exception as e:
            print(e)
        finally:
            print("boldface_elements_missing: ", boldface_elements_missing)
            return boldface_elements_missing

    def description_equal_to_title(self):
        description_equal_to_title = True
        try:
            if self.element_tree.xpath('//meta[@name="description"]/@content')[0] != self.element_tree.xpath('//title')[0].text_content():
                description_equal_to_title = False
        except Exception as e:
            print(e)
        finally:
            print("description_equal_to_title: ", description_equal_to_title)
            return description_equal_to_title

    def description_too_short(self):
        description_too_short = False
        try:
            tree_title_element = self.element_tree.xpath(
                '//meta[@name="description"]/@content')[0]
            if len(tree_title_element) < 50:
                description_too_short = True
        except Exception as e:
            print(e)
        finally:
            print("description_too_short: ", description_too_short)
            return description_too_short

    def title_too_long(self):
        title_too_long = False
        try:
            tree_title_element = self.element_tree.xpath(
                '//h1')[0].text_content()
            if len(title_too_long) > 70:
                title_too_long = True
        except Exception as e:
            print(e)
        finally:
            print("title_too_long: ", title_too_long)
            return title_too_long

    def title_too_short(self):
        title_too_short = False
        try:
            tree_title_element = self.element_tree.xpath(
                '//h1')[0].text_content()
            if len(tree_title_element) < 20:
                title_too_short = True
        except Exception as e:
            print(e)
        finally:
            print("title_too_short: ", title_too_short)
            return title_too_short

    def more_than_one_body_tag(self):
        more_than_one_body_tag = False
        try:
            tree_title_element = self.element_tree.xpath('//body')
            if len(tree_title_element) > 1:
                more_than_one_body_tag = True
        except Exception as e:
            print(e)
        finally:
            print("more_than_one_body_tag: ", more_than_one_body_tag)
            return more_than_one_body_tag

    def more_than_one_title_tag(self):
        more_than_one_title_tag = False
        try:
            tree_title_element = self.element_tree.xpath('//title')
            if len(tree_title_element) > 1:
                more_than_one_title_tag = True
        except Exception as e:
            print(e)
        finally:
            print("more_than_one_title_tag: ", more_than_one_title_tag)
            return more_than_one_title_tag

    def missing_html_lang(self):
        missing_html_lang = True
        try:
            tree_title_element = self.element_tree.xpath('//html/@lang')
            print("tree_title_element: ", tree_title_element)
            if len(tree_title_element) > 0:
                missing_html_lang = False
        except Exception as e:
            print(e)
        finally:
            print("missing_html_lang: ", missing_html_lang)
            return missing_html_lang

    def text_to_code_ratio_less_than_10_percent(self):
        try:
            text_to_code_ratio = 0.0
            text_to_code_ratio_less_than_10_percent = False
            tree_title_element = self.element_tree.xpath(
                '//html')[0].text_content()
            readable_text = tree_title_element.split()
            readable_chars = 0
            for word in readable_text:
                readable_chars += len(word)

            # code_and_text = self.resp.text.split()
            # total_chars = 0
            # for word in code_and_text:
            #     total_chars += len(word)
            # print(total_chars)

            total_chars = len(self.resp.text)
            text_to_code_ratio = readable_chars / \
                (total_chars-readable_chars) * 100

            if text_to_code_ratio < 10:
                text_to_code_ratio_less_than_10_percent = True

            print("text_to_code_ratio_less_than_10_percent: ",
                  text_to_code_ratio_less_than_10_percent)
            return text_to_code_ratio_less_than_10_percent
        except Exception as e:
            print(e)

    def non_html_urls(self):
        non_html_urls = False
        try:
            tree_urls = self.element_tree.xpath('//a/@href')
            for url in tree_urls:
                if "http:" in url:
                    non_html_urls = True
                    break
        except Exception as e:
            print(e)
        finally:
            print("non_html_urls: ", non_html_urls)
            return non_html_urls

    def has_favicon(self):
        has_favicon = False
        try:
            tree_links = self.element_tree.xpath('//link/@href')
            for link in tree_links:
                if "ico" in link:
                    has_favicon = True
                    break
        except Exception as e:
            print(e)
        finally:
            print("has_favicon: ", has_favicon)
            return has_favicon

    def page_links_to_http_image(self):
        page_links_to_http_image = False
        try:
            tree_links = self.element_tree.xpath('//img/@src')
            for link in tree_links:
                if "http:" in link:
                    page_links_to_http_image = True
                    break
        except Exception as e:
            print(e)
        finally:
            print("page_links_to_http_image: ", page_links_to_http_image)
            return page_links_to_http_image

    def low_word_count(self):
        try:
            low_word_count = False
            tree_title_element = self.element_tree.xpath(
                '//html')[0].text_content()
            readable_words = tree_title_element.split()

            print(len(readable_words))

            if len(readable_words) < 500:
                low_word_count = True
        except Exception as e:
            print(e)
        finally:
            print("low_word_count: ", low_word_count)
            return low_word_count

    def page_updated_over_an_year_ago(self):
        page_updated_over_an_year_ago = False
        try:
            print(self.resp.headers)
            # print(self.resp.headers["Last-Modified"])
            # print(self.resp.headers["Date"])
            last_modified = eut.parsedate_to_datetime(
                self.resp.headers["Last-Modified"])
            curr_date = eut.parsedate_to_datetime(
                self.resp.headers["Date"])

            diff = (curr_date - last_modified).total_seconds()
            days = divmod(diff, 86400)[0]

            if days > 365:
                page_updated_over_an_year_ago = True
        except Exception as e:
            print("HTTP Response Header does not contain the relevant information")
            print(e)
        finally:
            print("page_updated_over_an_year_ago: ",
                  page_updated_over_an_year_ago)
            return page_updated_over_an_year_ago

#################            LINKS           ########################
    def outgoing_malformed_links(self):
        outgoing_malformed_links = False
        try:
            tree_urls = self.element_tree.xpath('//a/@href')
            for url in tree_urls:
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
        try:
            tree_image = self.element_tree.xpath('count(//a/img)')
            print("tree_iamge: ", tree_image)
            tree_alt = self.element_tree.xpath('count(//a/img/@alt)')
            print("tree_alt: ", tree_alt)
            if tree_alt != tree_image:
                anchored_image_no_alt_text = True
        except Exception as e:
            print(e)
        finally:
            print("anchored_image_no_alt_text: ", anchored_image_no_alt_text)
            return anchored_image_no_alt_text

    def page_has_more_than_100_internal_links(self):
        page_has_more_than_100_internal_links = False
        count = 0
        domain = urlparse(self.url).netloc
        try:
            tree_urls = self.element_tree.xpath('//a/@href')
            for url in tree_urls:
                if domain == urlparse(url).netloc:
                    count += 1
                    if count >= 100:
                        page_has_more_than_100_internal_links = True
                        break
        except Exception as e:
            print(e)
        finally:
            print("page_has_more_than_100_internal_links: ",
                  page_has_more_than_100_internal_links)
            return page_has_more_than_100_internal_links

#################            INDEXABILITY           ########################
    def canonical_is_missing(self):
        canonical_is_missing = False
        try:
            tree_canonical = self.element_tree.xpath(
                '//head/link[@rel="canonical"]')[0]
            canonical_is_missing = True
        except Exception as e:
            print(e)
        finally:
            print("canonical_is_missing: ", canonical_is_missing)
            return canonical_is_missing

    def h2_has_other_tags_inside(self):
        h2_has_other_tags_inside = False
        try:
            tree_h2 = self.element_tree.xpath('//h2')[0]
            for x in tree_h2.iter():
                print("x: ", x.tag)
        except Exception as e:
            print(e)
        finally:
            print("h2_has_other_tags_inside: ", h2_has_other_tags_inside)
            return h2_has_other_tags_inside


if __name__ == "__main__":
    url = sys.argv[1]
    check = InPageSeoAudit(url)
    check.page_updated_over_an_year_ago()
    # check.page_code_has_less_than_500_symbols()
    # check.images_present()
    # check.pdf_present()
    # check.is_h1_tag_missing()
    # check.is_p_tag_missing()
    # check.is_alt_text_missing()
    # check.is_title_tag_missing()
    # check.is_description_missing()
    # check.is_description_empty()
    # check.is_h1_empty()
    # check.duplicate_descriptions()
    # check.importance_elements_missing()
    # check.alt_tags_with_one_word()
    # check.long_description()
    # check.h1_starts_with_lowercase()
    # check.h1_too_long()
    # check.h1_too_short()
    # check.boldface_elements_missing()
    # check.description_equal_to_title()
    # check.description_too_short()
    # check.more_than_one_body_tag()
    # check.missing_html_lang()
    # check.is_title_empty()
    # check.duplicate_h1()
