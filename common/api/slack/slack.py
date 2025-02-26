import os, ssl, certifi, tenacity
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler

class SlackClient:
    def slack_client_setting():
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.check_hostname = False  # 호스트 이름 검증 비활성화
        ssl_context.verify_mode = ssl.CERT_NONE  # 인증서 검증 비활성화
        client = WebClient(token=os.environ['SLACK_TOKEN'],ssl=ssl_context)
        rate_limit_handler = RateLimitErrorRetryHandler(max_retry_count=2)
        client.retry_handlers.append(rate_limit_handler)
        return client
    
class Slack:
    client = SlackClient.slack_client_setting()
    channel = var.common_el['channel']
    file_path = None
    server_thread_ts = None
    poc = 'MW'
    text_format = {
        'pass': f'[{poc} - PASS]',
        'fail': f'[{poc} - FAIL]',
        'log': f'[{poc} - LOG]',
    }
    blocks_form={
        'title':[
            {
                "type": "header",
                "text":{
                    "type": "plain_text",
                    "text": "{}"
                }
            }
        ],
        'server_result':[
            {
                "type": "header",
                "text":{
                    "type": "plain_text",
                    "text": f"{poc} 테스트자동화 {{}}"
                }
            }
        ],
        'server_title':[
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{poc} 테스트자동화 실행"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "실행 시간 :  {}월 {}일 {}시 {}분"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"POC : `{poc} (Selenium)` "
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "테스트자동화 상세 케이스의 실행 결과는 쓰레드를 참고 해 주세요"
                }
            }
        ]
    }

    
    @classmethod
    def setServerThreadTS(cls,server_thread_ts=None):
        '''
            server_thread_ts 세팅
        '''
        if server_thread_ts is None:
            raise Exception("server_thread_ts is None")
        else:
            cls.server_thread_ts=server_thread_ts
        return
    @classmethod
    def getServerThreadTS(cls):
        '''
            server_thread_ts 세팅 가져오기
        '''
        if cls.server_thread_ts is None:
            raise Exception("server_thread_ts is None")
        return cls.server_thread_ts
    @classmethod
    def setFilePath(cls,file_path=None):
        '''
            file_path 세팅
        '''
        if file_path is None:
            raise Exception("file_path is None")
        else:
            cls.file_path=file_path
        return
    @classmethod
    def getFilePath(cls):
        '''
            file_path 세팅 가져오기
        '''
        if cls.file_path is None:
            raise Exception("file_path is None")
        return cls.file_path

    @classmethod
    def send_slack(cls,log:str,test_result:bool=True,img_comment:str=None):
        '''
        slack API; 테스트 실행 결과 로그 전송(이슈 발생 시, 로그와 이미지 전송)
        '''
        cls.send_slack_text(log,test_result)
        if test_result is False:
            cls.send_slack_img(img_comment)

    @classmethod
    @tenacity.retry(wait=tenacity.wait_fixed(10),stop=tenacity.stop_after_attempt(5),reraise=True,)
    def send_slack_server_title(cls):
        '''
        slack API; 드라이버 시작 로그 전송(서버 로그)
        '''
        now = datetime.now()
        def apply_format(data, *args):
            if isinstance(data, dict):
                return {k: apply_format(v, *args) for k, v in data.items()}
            elif isinstance(data, list):
                return [apply_format(item, *args) for item in data]
            elif isinstance(data, str):
                return data.format(*args)
            return data

        blocks_form = apply_format(cls.blocks_form['server_title'],now.month,now.day,now.hour,now.minute)

        try:
            response = cls.client.chat_postMessage(
            channel=cls.channel,
            blocks=blocks_form,
            text="test",
            )       
            assert response["message"]
            cls.setServerThreadTS(response['ts']) 
            return response['ts']


        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"] 
            print(f"Got an error: {e.response['error']}") 

    @classmethod
    @tenacity.retry(wait=tenacity.wait_fixed(10),stop=tenacity.stop_after_attempt(5),reraise=True,)
    def send_slack_server_result(cls,test_result:bool=None):
        '''
        slack API; 테스트 완료 시, 결과 로그 전송(서버 로그)
        test_result: True/False에 따라 테스트 결과를 반환(PASS/FAIL) 
        '''
        res = "PASS" if test_result is True else "FAIL"

        def apply_format(data, *args):
            if isinstance(data, dict):
                return {k: apply_format(v, *args) for k, v in data.items()}
            elif isinstance(data, list):
                return [apply_format(item, *args) for item in data]
            elif isinstance(data, str):
                return data.format(*args)
            return data

        blocks_form = apply_format(cls.blocks_form['server_result'],res)
        try:
            response = cls.client.chat_postMessage(
            channel=cls.channel,
            blocks=blocks_form,
            text="test",
            )       
            assert response["message"]

            if cls.channel == var.common_el['mention_channel'] and res == "FAIL":
                cls.send_slack_mention()

            cls.setServerThreadTS(response['ts'])
            return response['ts']


        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"] 
            print(f"Got an error: {e.response['error']}") 
            

    @classmethod
    @tenacity.retry(wait=tenacity.wait_fixed(10),stop=tenacity.stop_after_attempt(5),reraise=True,)
    def send_slack_text(cls,log:str='',test_result:bool=True):
        '''
        slack API; 테스트 결과 로그(FAIL/PASS) 전송
        전송 실패 시, 10초간격으로 최대 5회까지 반복
        '''
        if test_result is True:
            result=cls.text_format['pass']
        elif test_result is False:
            result=cls.text_format['fail']
        else:
            result=cls.text_format['log']
        
        try:
            response = cls.client.chat_postMessage(
            channel=cls.channel,
            thread_ts=cls.getServerThreadTS(),
            text=f"{result} - {log}"
            )
            assert response["message"]

            return response['ts']


        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"] 
            print(f"Got an error: {e.response['error']}")
    @classmethod        
    @tenacity.retry(wait=tenacity.wait_fixed(10),stop=tenacity.stop_after_attempt(5),reraise=True,)
    def send_slack_img(cls,img_comment:str=None):
        '''
        slack API; 테스트 실패 시, 스크린샷 전송
        전송 실패 시, 10초간격으로 최대 5회까지 반복
        '''
        
        print(f"경로 -> {cls.getFilePath()}")
        if cls.getFilePath() is None:
            raise Exception('file 경로가 잘못되었습니다.')
        if img_comment is None:
            img_comment = '이슈'
        try:
            # 이슈 이미지 전송
            response = cls.client.files_upload_v2(
                initial_comment=img_comment,
                channel=cls.channel,
                thread_ts=cls.getServerThreadTS(),
                title='이슈 이미지',
                file=cls.getFilePath(),
            )
            assert response["file"]

        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"] 
            print(f"Got an error: {e.response['error']}")

    @classmethod
    @tenacity.retry(wait=tenacity.wait_fixed(10),stop=tenacity.stop_after_attempt(5),reraise=True,)
    def send_slack_title(cls,text:str):
        '''
        slack API; 테스트 시작 및 종료 로그 전송
        text: '{POC} 실행 시작/종료' 문구 출력
        '''
        def apply_format(data, *args):
            if isinstance(data, dict):
                return {k: apply_format(v, *args) for k, v in data.items()}
            elif isinstance(data, list):
                return [apply_format(item, *args) for item in data]
            elif isinstance(data, str):
                return data.format(*args)
            return data

        blocks_form = apply_format(cls.blocks_form['title'],text)
        try:
            response = cls.client.chat_postMessage(
            channel=cls.channel,
            thread_ts=cls.getServerThreadTS(),
            blocks=blocks_form,
            text="test",
            )       
            assert response["message"] 


        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"] 
            print(f"Got an error: {e.response['error']}")


    @classmethod
    @tenacity.retry(wait=tenacity.wait_fixed(10),stop=tenacity.stop_after_attempt(5),reraise=True,)
    def send_slack_mention(cls):
        '''
        slack API; 테스트 결과 FAIL 인 경우 멘션 기능
        '''
        mention = var.common_el['mention_id']
        try:
            response = cls.client.chat_postMessage(
            channel=cls.channel,
            thread_ts=cls.getServerThreadTS(),
            text=mention,
            )       
            assert response["message"]
            return response['ts']
        
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"] 
            print(f"Got an error: {e.response['error']}")

    @classmethod
    def send_slack_log_file(cls):
        '''
        result/debug/_.log 파일 전송
        '''
        file_path = 'result/debug/' + datetime.now().strftime('%Y%m%d') + '_info.log'
        try:
            response = cls.client.files_upload(
                channels = 'C06599H0H08',
                file = file_path,
                filetype = "text",
                title = f'{cls.poc}_log_file',
            )

        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"] 
            print(f"Got an error: {e.response['error']}")