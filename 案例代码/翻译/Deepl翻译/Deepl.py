import requests
import json
import time


class DeeplTranslator:

    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "content-type": "application/json",
        }
        self.request_url = "https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs"

    def translate(self,source_context,target_lang):
        request_data = {
            "id": int(time.time()),
            "jsonrpc": "2.0",
            "method": "LMT_handle_jobs",
            "params": {
                "commonJobParams": {"formality": None},
                "jobs": [{
                    "kind": "default",
                    "raw_en_sentence": "",
                    "raw_en_context_before": [],
                    "raw_en_context_after": [],
                    "preferred_num_beams": 4,
                    "quality": "fast"
                }],
                "lang": {
                    "user_preferred_langs": [],
                    "source_lang_user_selected": "auto",
                    "target_lang": ""
                },
                "priority": -1,
                "timestamp": int(time.time())
            }
        }
        request_data["params"]["jobs"][0]["raw_en_sentence"] = source_context
        request_data["params"]["lang"]["target_lang"] = target_lang
        resp = requests.post(url=self.request_url, data=json.dumps(request_data,ensure_ascii=False), headers=self.headers)
        response_text_dict = json.loads(resp.text)
        if response_text_dict.get('error'):
            return ("Too many requests")

        result = response_text_dict["result"]["translations"][0]["beams"][0]["postprocessed_sentence"]
        return result


if __name__ == '__main__':
    deepl_translator = DeeplTranslator()
    # 访问频繁只能换IP
    while 1:
        #'输入的是英文'
        result = deepl_translator.translate(source_context="hello world", target_lang="ZH")
        print(result)

        #'输入的是中文'
        source_context = "你好世界".encode('unicode-escape').decode()
        result = deepl_translator.translate(source_context, target_lang="EN")
        print(result.encode('utf-8').decode())