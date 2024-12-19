Feature: 자동화가이드 TC Scripts 작성

    Scenario: Testcase_01. U+아이디로 로그인
        Given U+ 웹사이트에 접속한다
        When "U+ID" 로그인 버튼을 클릭한다
        Then "/login/onid-login" 페이지로 이동한다
        When 아이디와 비밀번호를 입력한다
        And "로그인" 버튼을 클릭한다
        Then 로그인이 성공한다
        
    Scenario: Testcase_02. 
        Given Chrome browser 실행하여 NAVER 페이지 접근
        When NAVER 페이지에서 로그인 버튼 클릭
        Then 5초간 대기 후 브라우저 종료
    
    Scenario: Testcase_03
        Given Chrome browser 실행하여 NAVER 페이지 접근
        When NAVER 페이지에서 로그인 버튼 클릭
        Then 5초간 대기 후 브라우저 종료