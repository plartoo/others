from lxml import html
import csv

f = open(r'C:\Users\lacheephyo\Desktop\nn.html')
tree = html.fromstring(f.read())
accnts = tree.xpath('//td[@class="ComboOption"]/text()')

fo = open('output.csv','w', newline='')
wr = csv.writer(fo)
for r in accnts:
 wr.writerow([r,])
 
#wr.writerows([accnts])
fo.close()
