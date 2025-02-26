import os, signal, time, subprocess, urllib3
import common 

class AppiumServer():
    def __init__(self,PORT:int|str=4723):
        self.PORT=str(PORT)
        self.server_process=None
        self.server_log_path=self.set_log_path(f'result\\debug\\server_step_{self.PORT}.log')
    
    def set_log_path(self,log_path='result\\debug\\server_step.log'):
        '''
        result_path: 서버 로그를 저장할 경로
        ex) 'result\\debug\\server_step.log'
        '''
        if '\\' not in log_path:
            raise Exception("서버 로그 파일 경로를 '\\'로 구분지어 사용해주세요 ")
        current_path=os.getcwd()
        parent_folder_name = log_path.split('\\',1)[0]
        for _ in range(2):
            is_result_folder = os.path.join(current_path, parent_folder_name)
            if not os.path.exists(is_result_folder):
                current_path=os.path.dirname(current_path)
                pass
            else:
                break
        path = os.path.join(current_path,log_path)
        return path   


    @property
    def is_running(self) -> bool:
        """
        appium 서버가 실행 중이면 True 반환
        """
        return self.server_process is not None and self.server_process.poll() is None


    def stop(self,test_result:bool) -> bool:
        """
        appium 서버가 정상적으로 멈추면 True 반환
        """
        is_terminated = False
        if self.is_running:
            assert self.server_process
            self.server_process.send_signal(signal.CTRL_BREAK_EVENT)
            os.kill(self.server_process.pid,signal.SIGTERM)
            # os.system('adb shell pm clear com.lguplus.mobile.cs')
            os.system('adb shell am force-stop com.android.chrome')
            # self.server_process.kill()
            os.system("adb shell am force-stop com.lguplus.mobile.cs")
            print("----------- appium server stop -----------")
            Slack.send_slack_server_result(test_result)
            Slack.send_slack_log_file()
            is_terminated = True
        self.server_process = None
        return is_terminated
    
    @property
    def is_listening(self) -> bool:
        """
        appium 서버가 정상 listening 중이면 True 반환
        """
        # if not self.is_running:
        #     return False
        try:
            return self._poll_status()
        except Exception:
            return False
        
    def _poll_status(self,timeout_ms: int=1000) -> bool:
        time_started_sec = time.time()
        conn = urllib3.PoolManager(timeout=1.0)
        while time.time() < time_started_sec + timeout_ms / 1000.0:
            if not self.is_running:
                raise Exception("appium server를 실행하세요.")
            try:
                resp = conn.request('GET', f"http://127.0.0.1:{self.PORT}/status")
                print(f"resp.status ==> {resp.status}")
                if resp.status < 400:
                    print(resp.data.decode())
                    return True
            except urllib3.exceptions.HTTPError:
                pass
            time.sleep(1.0)
        return False
    
    def waiting(self) -> bool:
        count=0
        try:
            while True:
                count+=1
                if count > 15:
                    raise Exception("서버 실행 불가")
                time.sleep(1)
                print(count)
                if self.is_listening == self.is_running is True:
                    print("-"*15+" Appium Server Starting "+"-"*15)
                    break
            return True
        except Exception :
            # os.system('adb shell pm clear com.lguplus.mobile.cs')
            return False

    def appium_service(self) -> int|str:
        """
        실행중인 포트번호 시, 임의로 포트번호 지정
        서버 실행 후, 임의 지정된 포트번호 반환
        """

        # 포트 실행 여부 확인
        while True:
            res=subprocess.getstatusoutput(f"netstat -ano | findstr :{self.PORT}")
            if res[0] == 0:
                print(f"현재 {self.PORT} 포트는 사용중인 포트입니다 ")
                self.PORT = int(self.PORT) + 1
            else:
                print(f"{self.PORT} 는 사용가능한 포트 입니다.")
                self.server_log_path=self.set_log_path(f'result\\debug\\server_step_{self.PORT}.log') #서버 파일명 재설정
                break
        Slack.send_slack_server_title()

        if self.is_running is False:
            ANDROID_HOME=os.getenv('ANDROID_HOME', 'None')
            JAVA_HOME=os.getenv('JAVA_HOME', 'None')
            if ANDROID_HOME == 'None':
                print('ANDROID_HOME 가져올 수 없음')
                raise Exception(RuntimeError)
                # os.environ['ANDROID_HOME'] = 'C:/Users/User/AppData/Local/Android/Sdk'  # TODO ANDROID_HOME 환경 변수 직접 지정
            if JAVA_HOME == 'None':
                print('JAVA_HOME 가져올 수 없음')
                raise Exception(RuntimeError)
                # os.environ['JAVA_HOME'] = 'C:/Program Files/Java/jdk-11' # TODO JAVA_HOME 환경 변수 직접 지정
            env=os.environ.copy()

            os.environ["PATH"] += os.pathsep + os.path.join(os.getenv('ANDROID_HOME'),'platform-tools')       
            os.environ["PATH"] += os.pathsep + os.path.join(os.getenv('ANDROID_HOME'),'build-tools\\30.0.3')
            os.environ["PATH"] += os.pathsep + os.path.join(os.getenv('ANDROID_HOME'),'tools\\bin')
            os.environ["PATH"] += os.pathsep + os.path.join(os.getenv('ANDROID_HOME'),'tools')
            os.environ["PATH"] += os.pathsep +os.path.join(os.getenv('JAVA_HOME'),'bin')

            # print(f"env(ANDROID_HOME): {os.environ['ANDROID_HOME']}")
            # print(f"env(JAVA_HOME): {os.environ['JAVA_HOME']}")
            # print(f"env: {env}")
            # print(" ===== appium thread start =====")
            try:
                # self.server_process=subprocess.Popen(['appium','-a','0.0.0.0','-p',f'{self.PORT}','--session-override','>',f'{self.server_log_path}','2>&1'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                # self.server_process=subprocess.Popen(['appium','--allow-insecure','chromedriver_autodownload','-a','0.0.0.0','-p',f'{self.PORT}','--session-override','>',f'{self.server_log_path}','2>&1'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                print('appium','-a','0.0.0.0','-p',f'{self.PORT}','>',f'{self.server_log_path}','2>&1')
                self.server_process=subprocess.Popen(['appium','-a','0.0.0.0','-p',f'{self.PORT}','>',f'{self.server_log_path}','2>&1'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                
                return self.PORT
            
            except BaseException as e:
                print('ERROR!')
                print(e)
            except Exception(RuntimeError):
                print('ERROR!')
                self.stop()
                raise Exception(RuntimeError)
        else: 
            print("is running")
  
