# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib.parse import urlparse

from scrapy.pipelines.files import FilesPipeline


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CoaScraperPipeline:
    def process_item(self, item, spider):
        return item



class CoaFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
    	print(request.headers['content-disposition'])
    	# content-disposition: inline;filename=document_873BE53F-F0FB-9ABC-DD5AAC2D54DADEE3.pdf
    	return item.text+'.pdf'
#        return 'files/' + os.path.basename(urlparse(request.url).path)