### git 명령어

```
git init                       # 로컬 저장소를 초기화
git pull origin main           # 원격 저장소의 main 브랜치를 로컬로 가져오기
git add .                      # 변경된 모든 파일을 스테이징
git commit -m "커밋 메시지"     # 변경 사항을 커밋
git checkout <브랜치 이름>      # 지정된 브랜치로 전환
git remote add origin <원격 저장소 주소> # 원격 저장소 주소를 추가
git push origin main           # 로컬 main 브랜치를 원격 저장소로 푸시
git fetch origin               # 원격 브랜치의 최신 상태 가져오기
git reset --hard origin/main   # 로컬 브랜치를 원격 브랜치로 강제로 덮어쓰기
```

### TEST-RPA 구조

```
TEST-RPA/
├── base/                      # WebDriver 기본 설정 및 공통 클래스
├── config/                    # 프로젝트 설정 파일
├── features/                  # 테스트 기능 구현
├── locators/                  # 웹 요소 위치 정보
├── logs/                      # 로그 파일 저장
├── pages/                     # 페이지 객체 모델
│   ├── GNB_m1.py              # GNB 메뉴 1번 테스트
│   ├── GNB_m3.py              # GNB 메뉴 3번 테스트
│   ├── GNB_m4.py              # GNB 메뉴 4번 테스트
│   ├── login.py               # 로그인 관련 테스트
│   └── main.py                # 메인 페이지 테스트
├── screenshots/               # 테스트 중 캡처된 스크린샷
├── utils/                     # 유틸리티 함수 모음
│   ├── custom_actionchains.py # 사용자 정의 액션 체인
│   ├── custom_logger.py       # 로깅 유틸리티
│   ├── element_utils.py       # 요소 조작 유틸리티
│   ├── exception_handler.py   # 예외 처리 유틸리티
│   ├── modal_utils.py         # 모달 창 처리 유틸리티
│   ├── page_handling.py       # 페이지 처리 유틸리티
│   └── screenshot.py          # 스크린샷 유틸리티
├── README.md                  # 프로젝트 설명 문서
├── requirements.txt           # 프로젝트 의존성 목록
└── runner.py                  # 테스트 실행 스크립트
```
