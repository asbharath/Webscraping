import sys
spider = sys.argv[1] # name of the parameter
if __name__ == '__main__':
    from scrapy import cmdline
    val = "scrapy crawl {}".format(spider)
    print(val)
    cmdline.execute("scrapy crawl {}".format(spider).split())
else:
    print("out of main")