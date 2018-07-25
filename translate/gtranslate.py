import account_info
import http.client, urllib.parse, uuid, json
import requests
import io
import json
import re
import pandas as pd

# REF: https://stackoverflow.com/q/37667671
# REF: https://web.archive.org/web/20180513001508/https://ctrlq.org/code/19909-google-translate-api
# REF: https://web.archive.org/web/20180513001611/https://ctrlq.org/code/19899-google-translate-languages

# Language list: https://www.microsoft.com/en-us/translator/languages.aspx
# Main translator: https://www.microsoft.com/en-us/translator/translatorapi.aspx
# We need to look up the language labels (such as 'es', 'en' by trying out the widget here: https://www.bing.com/widget/translator and catching the URL live using Chrome's developer tool
# Note: EU's eTranslation service is not good for texts shorter than 30 characters, so we cannot apply that
# https://ec.europa.eu/info/resources-partners/machine-translation-public-administrations-etranslation_en
# We maybe able to use that to upload the whole mapping document and get it translated
# text = 'Ya hemos mirado la configuración en el panel de control como Miguel nos explicó pero el  problema  sigue existiendo'
# print('Source text:', text)
# print('Translated text:', translate(text, 'es', 'en'))


def translate(text, source_language, target_language):
    host = 'api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'

    requestBody = [{
        'Text': text,
    }]
    content = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')

    # Translate to German and Italian.
    params = ''.join(['&from=', source_language, '&to=', target_language])

    headers = {
        'Ocp-Apim-Subscription-Key': account_info.API_KEY,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    conn = http.client.HTTPSConnection(host)
    conn.request("POST", path + params, content, headers)
    response = conn.getresponse().read()
    return json.loads(response)

    # # Using Microsoft Bing's Translate API (my poor man's hack-ish attempt)
    # base_url_1 = 'https://api.microsofttranslator.com/v2/ajax.svc/TranslateArray?appId='
    # app_id = quote('"') + 'TIzUkShc-PwdtTGuWT6dBOmttItmhca2MXmdccZow2N4*' + quote('"')
    # base_url_2 = '&texts=['
    # text = quote('"') + quote(text) + quote('"')
    # base_url_3 = ']&from='
    # source_lang = quote('"') + source_language + quote('"')
    # base_url_4 = '&to='
    # target_lang = quote('"') + target_language + quote('"')
    # base_url_5 = '&oncomplete=_mstc5&onerror=_mste5'
    # url = base_url_1 + app_id + base_url_2 + text + base_url_3 + source_lang + base_url_4 + target_lang + base_url_5

    # # Google's Translation API (no longer works)
    # base_url= 'https://translate.googleapis.com/translate_a/single?client=gtx&dt=t'
    # source_lang= '&sl=' + source_language
    # target_lang= '&tl=' + target_language
    # text= '&q=' + text
    # url = base_url + source_lang + target_lang + text

    # rq = requests.get(url)
    # if rq.status_code == 200:
    #     ## Use following with Microsoft API
    #     regex = re.search(r'.*\((\[\{.*\}\])\)', rq.text)
    #     if regex:
    #         translated = json.load(io.StringIO(regex[1]))
    #         return translated[0]['TranslatedText']
    #     else:
    #         return rq.text
    #
    #     ## Use following with Google API
    #     # translated_text = json.load(io.StringIO(rq.text))
    #     # return translated_text[0][0][0]
    # return error_msg

print(
    translate('Ya hemos mirado la configuración en el panel de control como Miguel nos explicó pero el  problema  sigue existiendo',
      'es',
      'en')
)

# def clean_text(text):
#     str_before_comma=text.split(',')[0]
#     regex = re.compile('[^a-zA-Z]') # remove non-alphabetical stuff
#     str_with_only_alphabets = regex.sub(' ', str_before_comma)
#     str_with_just_one_space_allowed = ' '.join(str_with_only_alphabets.split())
#     str_lowered = str_with_just_one_space_allowed.lower() # this has positive effect on translation accuracy
#     return str_lowered
#
#
# if __name__ == "__main__":
#     source_lang = 'de'
#     target_lang = 'en'
#     df = pd.read_excel(open('to_translate.xlsx', 'rb'), sheetname='Products_Mapping')
#     cols = ['GM_COUNTRY_NAME', 'GM_ADVERTISER_NAME', 'GM_SECTOR_NAME', 'GM_CATEGORY_NAME', 'GM_BRAND_NAME',
#             'GM_PRODUCT_NAME', 'SOS_PRODUCT']
#     cols_to_translate = ['GM_COUNTRY_NAME', 'GM_ADVERTISER_NAME', 'GM_SECTOR_NAME', 'GM_CATEGORY_NAME', 'GM_BRAND_NAME',
#                          'GM_PRODUCT_NAME']
#     translated_output = []
#
#     for i, r in df.iterrows():
#         cur_row = []
#         for c in cols_to_translate:
#             cur_row.append(r[c])
#             cleaned_txt = clean_text(r[c])
#             translated_text = translate(cleaned_txt, source_lang, target_lang)
#             cur_row.append(translated_text)
#         cur_row.append(r['SOS_PRODUCT'])
#         print(cur_row)
#         translated_output.append(cur_row)
#
#     final_cols = [j for c in cols_to_translate for j in [c, '{}_Translated'.format(c)]] + ['SOS_PRODUCT']
#     df_out = pd.DataFrame(translated_output, columns=final_cols)
#     df_out.to_excel('translated.xlsx', index=False)
#     # writer = pd.ExcelWriter('translated.xlsx')
#     # df_out.to_excel(writer, index=False)
#     # writer.save()
#     print('Translation finished')

