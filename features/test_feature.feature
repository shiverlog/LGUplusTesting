Feature: 자동화가이드 TC Scripts 작성

    Background: U+ 닷컴 접속
        Given U+ 닷컴에 접속한다
    
    Scenario: Testcase_01. 메인 페이지 - 로그인
        When "U+ID" 로그인 버튼을 클릭한다
        Then "/login/onid-login" 페이지로 이동한다
        When 아이디와 비밀번호를 입력한다
        And "로그인" 버튼을 클릭한다
        Then 로그인 성공 및 메인페이지 정상 이동을 확인한다

    Scenario: Testcase_02. 메인 페이지 - KV 영역
        Then KV 영역의 이미지가 정상적으로 노출된다
        And img 개수 비교 성공 및 정상 노출을 확인한다

    Scenario: Testcase_03. 메인 페이지 - 기기 추천 영역
        When 기기 추천 영역에서 기기를 선택한다
        Then 기기 상세 페이지로 이동한다
        And 기기명이 일치하는지 확인한다

    Scenario: Testcase_04. 모바일 페이지 - GNB 모바일 - 테마 배너
        When GNB에서 "모바일"을 클릭한다
        Then 테마 배너 항목이 정상적으로 노출된다
        And 테마 배너 이미지 개수가 3개인지 확인한다  # 명확한 검증 기준 예시

    Scenario: Testcase_05. 모바일 페이지 - GNB 모바일 - 휴대폰 영역
        When GNB에서 "모바일"을 클릭한다
        And 휴대폰 영역에서 랜덤으로 탭을 선택한다
        And 랜덤으로 기기를 선택한다
        Then 기기 상세 페이지로 이동한다
        When 기기 옵션 및 주문 옵션을 랜덤으로 선택한다
        And "장바구니"를 클릭한다
        Then 장바구니 페이지로 이동한다
        And 기기명, 요금제, 금액이 일치하는지 확인한다
        When 해당 기기를 장바구니에서 삭제한다
        Then 장바구니 항목이 삭제된 것을 확인한다

    Scenario: Testcase_06. 모바일 페이지 - GNB 모바일 - 인터넷/IPTV 결합 영역
        When GNB에서 "모바일"을 클릭한다
        And 인터넷/IPTV 결합 영역에서 드롭다운 항목을 랜덤으로 선택한다
        And "가입 상담 신청"을 클릭한다
        Then 새창으로 상담 신청 페이지가 열린다
        And 메인 윈도우와 팝업 윈도우 간의 할인 금액이 일치한다

    Scenario: Testcase_07. 마이 페이지 - GNB 마이페이지 - 요금/납부 - 청구 내역
        When GNB에서 "마이페이지"를 클릭한다
        And 마이페이지 내 청구요금을 확인한다
        And "요금/납부" 탭을 클릭한다
        And 청구 내역에서 월을 확인하고 선택한다
        Then 해당 월의 청구요금 및 납부 페이지로 이동한다
        And 청구 금액이 일치하는지 확인한다

    Scenario: Testcase_08. 마이 페이지 - GNB 마이페이지 - 가입/사용 현황 - 사용 내역 조회
        When GNB에서 "마이페이지"를 클릭한다
        And "가입/사용 현황" 탭을 클릭한다
        Then 아코디언 메뉴가 정상적으로 노출된다
        When 서브메뉴 중 "사용내역 조회"를 클릭한다
        Then 사용내역 조회 페이지로 이동한다
        When 월별 사용량 조회 탭을 클릭한다
        And "월별 사용량 상세 조회"를 클릭한다
        Then 월별 사용량 상세 조회 탭 리스트가 정상적으로 노출된다

    Scenario: Testcase_09. 혜택/멤버십 페이지 - GNB 혜택/멤버십 - 온라인 가입 할인 혜택
        When GNB에서 "혜택/멤버십"을 클릭한다
        And 온라인 가입 할인 혜택 영역에서 "혜택 모두 보기"를 클릭한다
        Then 온라인 구매 혜택 페이지로 이동한다
        And 온라인 구매 혜택 탭 리스트가 정상적으로 노출된다

    Scenario: Testcase_10. 혜택/멤버십 페이지 - GNB 혜택/멤버십 - 이벤트
        When GNB에서 "혜택/멤버십"을 클릭한다
        When 유저가 이벤트 영역에서 "이벤트 모두 보기"를 클릭한다
        Then 이벤트 페이지로 이동한다

    Scenario: Testcase_11. 고객지원 페이지 - GNB 고객지원 - 자주 찾는 검색어
        When GNB에서 "고객지원"을 클릭한다
        When 유저가 자주 찾는 검색어에 검색어를 랜덤으로 입력하여 검색버튼을 클릭한다
        Then 검색 결과 페이지로 이동한다
        And 검색 결과가 정상적으로 노출된다

    Scenario: Testcase_12. 고객지원 페이지 - GNB 고객지원 - 검색창
        When GNB에서 "고객지원"을 클릭한다
        When 검색창에 특수 문자를 입력한다
        And 검색 결과 페이지로 이동한다
        Then 검색 결과가 존재하지 않습니다 문구를 확인한다