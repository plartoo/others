from lxml import html
import csv

f = open(r'C:\Users\phyo.thiha\Desktop\others\random_stuff\parse_local_html\nn.html')
tree = html.fromstring(f.read())
accnts = tree.xpath('//td[@class="ComboOption"]/text()')

fo = open('output.csv','w', newline='')
wr = csv.writer(fo)
for r in accnts:
 wr.writerow([r,])
 
#wr.writerows([accnts])
fo.close()
