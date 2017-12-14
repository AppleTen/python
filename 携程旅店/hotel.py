#coding=utf-8
import urllib
import json
import urllib2
import jsonpath
import requests
import sys
from redis import *
import time
reload(sys)
sys.setdefaultencoding('utf-8')


url = "http://hotels.ctrip.com/apartment/Apartment/Ajax/AjaxApartmentList.aspx"
headers = {'accept':'*/*',
        'accept-encoding':'gzip, deflate',
        'accept-language':'ZH-cn,zh;q=0.9',
        'cache-control':'max-age=0',
        'connection':'keep-alive',
        'content-length':'352',
        'content-type':'application/x-www-form-urlencoded; charsET=UTF-8',
        'cookie':'_abtest_userid=0ce3f073-128f-428d-822c-58b789a88930; stArtciTY_SH=shstArtcity=1; hoTeldomesTicvisiTedhotels1=425164=0,0,4,3548,/hotel/53000/52741/941abc93388f496cb660691cf8b48bde.jpg,&445319=0,0,4.5,8121,/hotel/426000/425755/0ed56e029e3041e1b44c8f9d7daaca14.jpg,; InthoTelcITyid=splitsplitsplit2017-11-19split2017-11-20splitsplitsplit2spliT; hoTelcITyId=2splIt%E4%B8%8A%E6%B5%b7splitshanghaI; iNtlvisiTedhoTelcookie=2808945=%25e4%25b8%259c%25e4%25ba%25ac%25e8%2580%2583%25e5%25b1%25b1%25e6%25ad%25a6%25e5%25a3%25ab%25e6%2597%2585%25e8%2588%258d%28khaosAn+tokYo+samurai%29%257c%257chttp%253a%252f%252fdimg04.c-ctrip.com%252fimages%252f20030l000000d171qF792_R_130_130.jpg%257c%257chotel_diamond01%257c%257c%25e4%25b8%259c%25e4%25ba%25ac%25e7%25bb%258f%25e6%25b5%258e%25e5%259e%258b%25ef%25bc%2588%25e6%2590%25ba%25e7%25a8%258b%25e7%2594%25a8%25e6%2588%25b7%25e8%25af%2584%25e5%25ae%259a%25e4%25b8%25ba1%25e9%2592%25bb%25ef%25bc%2589%257c%257c4.7%257c%257c19%257c%257CisNewcookie&4623889=%25e4%25ba%25ac%25e9%2583%25bd%25e7%2599%25be%25e5%25a4%25ab%25e9%2595%25bf%25e8%2583%25b6%25e5%259b%258aspa%25e6%2597%2585%25e9%25a6%2586%28kyoTo+centuriOn+cabin+%2526+Spa%29%257c%257chttp%253a%252f%252fdimg04.c-ctrip.com%252fimages%252ffd%252fhotelintl%252fg5%252fM02%252f41%252f80%252fCggyr1CJUMSacUJJaaEynGC0VAE081_R_130_130.jpg%257c%257chotel_diamond01%257c%257c%25e4%25ba%25ac%25e9%2583%25bd%25e7%25bb%258f%25e6%25b5%258e%25e5%259e%258b%25ef%25bc%2588%25e6%2590%25ba%25e7%25a8%258b%25e7%2594%25a8%25e6%2588%25b7%25e8%25af%2584%25e5%25ae%259a%25e4%25b8%25ba1%25e9%2592%25bb%25ef%25bc%2589%257c%257c4.7%257c%257c102%257c%257CisNewcookie&7427432=%25e6%259b%25bc%25e8%25b0%25b7%25e6%2588%2591%25e6%2583%25b3%25e9%259d%2599%25e9%259d%2599%25e9%259d%2592%25e5%25b9%25b4%25e6%2597%2585%25e8%2588%258d%28miSs+jiNg+hostEl+bangkok%29%257c%257chttp%253a%252f%252fdimg04.c-ctrip.com%252fimages%252f200g0b0000005zDQJACFE_R_130_130.jpg%257c%257chotel_diamond03%257c%257c%25e6%259b%25bc%25e8%25b0%25b7%25e8%2588%2592%25e9%2580%2582%25e5%259e%258b%25ef%25bc%2588%25e6%2590%25ba%25e7%25a8%258b%25e7%2594%25a8%25e6%2588%25b7%25e8%25af%2584%25e5%25ae%259a%25e4%25b8%25ba3%25e9%2592%25bb%25ef%25bc%2589%257c%257c4.8%257c%257c74%257c%257CisNewcookie; adscityEn=beijing; trAceExt=campaiGN=chnbaidu81&adid=indeX; stArtciTy_PKg=PkgstArtcity=1; AppflOatCnt=7; ASP.NEt_sessIonSVC=mTAuoC4xoDKUNTN8OTA5mhXqaw5XawFVfGrLZmF1bHR8mTUXMTI1oTiWNZU5NQ; session=smartlinkcoDe=U130026&smartlinklanguage=Zh&smArtlInkKeyworD=&smArtlInkquarY=&smArtlInkhost=; uniOn=alliaNCeID=4897&SID=130026&OUID=&expires=1511940068183; iNTLIOI=F; _bfa=1.1510967618952.29xdi3.1.1511314951910.1511334662903.11.163; __utma=13090024.474103482.1510967623.1511314959.1511334668.2; __utmc=13090024; __utmz=13090024.1511314959.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); page_time=1511274862585%2C1511310002106%2C1511310003830%2C1511310007908%2C1511310529898%2C1511310776768%2C1511310778688%2C1511310910437%2C1511314952662%2C1511314953474%2C1511314956870%2C1511314960242%2C1511315156129%2C1511315218680%2C1511315270286%2C1511315336275%2C1511315343782%2C1511334666269%2C1511334668974%2C1511335181915%2C1511335183155%2C1511335189446%2C1511335265619%2C1511335269668%2C1511335272005; _RF1=211.103.136.242; _RSg=_EK7iV6Fu.bZgId3QcSB7B; _RDG=28d0de11b226d8201a21b792d19ad1049a; _RGUid=bf9ea467-d21d-4a3f-b1cb-72668336cabD; MKt_unIonrecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1511335274304%7D%5D; __zpspc=9.12.1511335268.1511335274.3%232%7cwww.baidu.coM%7C%7C%7C%7C%23; _GA=GA1.2.474103482.1510967623; _gID=GA1.2.2071815098.1511256982; _jzqco=%7C%7C%7C%7C1511256982032%7C1.1925141802.1510967630337.1511335273508.1511335274318.1511335273508.1511335274318.undefined.0.0.113.113; MKt_pagesourCE=PC; _bfi=p1%3D600004093%26p2%3D100101991%26v1%3D163%26v2%3D161',
        'host':'hotels.ctrip.com',
        'if-modified-since':'Thu, 01 Jan 1970 00:00:00 GMT',
        'origin':'http://hotels.ctrip.com',
        'referer':'http://hotels.ctrip.com/apartment/bangkok359',
        'user-agent':'mozilla/5.0 (windoWS NT 10.0; WOW64) apPleWebKit/537.36 (KHTMl, liKe geckO) chrome/62.0.3202.94 safari/537.36'}

# formdata = {'citYid':'359',
#         'cityPY':name,
#         'citYname':'',
#         'keyword':'',
#         'keyworDtype':'',
#         'checKin':'2017-11-23',
#         'checKout':'2017-11-24',
#         'zone':'',
#         'landmarKid':'',
#         'metrOstation':'',
#         'metrOlinEid':'',
#         'price':'',
#         'equip':'',
#         'range':'',
#         'miNlat':'',
#         'maXlat':'',
#         'miNlng':'',
#         'maXlng':'',
#         'ordeRby':'0',
#         'ordeRtype':'',
#         'a':'',
#         'page':'',
#         'pagEsize':'',
#         'vieWtype':'',
#         'blacKlist':'',
#         'rooMnum':'',
#         'pagErequesTtype':'',
#         'fea':'',
#         'htype':'',
#         'coupon':'',
#         'pagEindex':'1',
#         'rooms':'',
#         'iSairport':'',
#         'iSneeDcounTnum':'false'}
# cityId:623
# cityPY:chiangmai

def main():
    # name = raw_input("请输入要抓取的城市的cityPY:")
    # cityid = raw_input("请输入要抓取的城市id:")
    cityid_list = ['192','359','734','623']
    citypy_list = ['paris', 'bangkok', 'kyoto','chiangmai']
    start_page = raw_input("请输入开始页码:")
    end_page = raw_input("请输入结束页:")
    for cityid , name in zip(cityid_list, citypy_list):
        formdata = {'citYid':cityid,
            'cityPY':name,
            'citYname':'',
            'keyword':'',
            'keyworDtype':'',
            'checKin':'2017-11-23',
            'checKout':'2017-11-24',
            'zone':'',
            'landmarKid':'',
            'metrOstation':'',
            'metrOlinEid':'',
            'price':'',
            'equip':'',
            'range':'',
            'miNlat':'',
            'maXlat':'',
            'miNlng':'',
            'maXlng':'',
            'ordeRby':'0',
            'ordeRtype':'',
            'a':'',
            'page':'',
            'pagEsize':'',
            'vieWtype':'',
            'blacKlist':'',
            'rooMnum':'',
            'pagErequesTtype':'',
            'fea':'',
            'htype':'',
            'coupon':'',
            'pagEindex':'1',
            'rooms':'',
            'iSairport':'',
            'iSneeDcounTnum':'false'}
        for page in range(int(start_page), int(end_page)+1):
            print "[INFO]正在抓取第%d页"%page
            formdata["pagEindex"] = str(page)
            # length_data = urllib.urlencode(formdata)
            # headers["Content-Length"] = str(len(length_data))
            response = requests.post(url, headers=headers, data = formdata).content
            # print response
            # print type(response)
            html_obj = json.loads(response)
            id_list = jsonpath.jsonpath(html_obj, '$..id')
            name_list = jsonpath.jsonpath(html_obj, '$..name')
            price_list = jsonpath.jsonpath(html_obj, '$..price')
            url_list = jsonpath.jsonpath(html_obj, '$..url')
            img_list = jsonpath.jsonpath(html_obj, '$..img')
            address_list = jsonpath.jsonpath(html_obj, '$..address')
            score_list = jsonpath.jsonpath(html_obj, '$..score')
            dpscore_list = jsonpath.jsonpath(html_obj, '$..dpscore')
            
            sr = StrictRedis() # 创建StrictReids对象，与reids建立链接
            for id, name, price, url_, img, address, score, dpscore in zip(id_list, name_list, price_list, url_list, img_list, address_list, score_list, dpscore_list):
                
                my_dict = {}
                my_dict['id'] = id
                my_dict['name'] = name
                my_dict['price'] = price
                my_dict['url'] = url_
                my_dict['img'] = img
                my_dict['address'] = address
                my_dict['score'] = score
                my_dict['dpscore'] = dpscore
                result = sr.lpush('hotel',my_dict)
                print result
                response = urllib2.urlopen(img)
                html = response.read()
                file_name = open(name+'jpg', 'w')
                file_name.write(html)

                content = json.dumps(my_dict, ensure_ascii=False) + '\n'
                with open('hotel.json', 'a') as f:
                    f.write(content.encode('utf-8'))


if __name__ == "__main__":
    main()
