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
│   ├── GNB_m5.py              # GNB 메뉴 5번 테스트
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
```
TEST-RPA/
├── common/                     # 공통 모듈 및 서비스
│   ├── api/                    # API 테스트 관련 파일 (Swagger, Postman 포함)
│   │   ├── swagger/            # Swagger API 문서 및 설정
│   │   ├── postman/            # Postman 컬렉션 및 테스트
│   ├── notifications/          # 알림 시스템 연동 (Slack, Teams 분리)
│   │   ├── slack/              # Slack 연동 모듈
│   │   ├── teams/              # Microsoft Teams 연동 모듈
│   ├── pubsub/                 # Pub/Sub 메시징 시스템
│   │   ├── publisher.ts        # 메시지 발행 모듈
│   │   ├── subscriber.ts       # 메시지 구독 모듈
│   ├── db/                     # 공통 DB 관련 설정 및 JSON 오류 저장
│   ├── docker/                 # Docker 설정 및 CI/CD 환경 구성 (공통으로 유지)
│   │   ├── Dockerfile          # 공통 Docker 설정
│   │   ├── docker-compose.yml  # Docker Compose 설정 파일
│   ├── scripts/                # 공통 실행 스크립트 (배치파일, 쉘 스크립트 등)
│   │   ├── run_tests.bat       # Windows 환경에서 Playwright 테스트 실행
│   │   ├── run_tests.sh        # Linux/macOS 환경에서 Playwright 테스트 실행
│   │   ├── run_tests.ps1       # PowerShell 실행 스크립트
│   │   ├── start_services.sh   # 공통 서비스 실행 스크립트
│   │   ├── stop_services.sh    # 공통 서비스 종료 스크립트
│   ├── utils/                  # 공통 유틸리티 함수 모음
│   │   ├── logging.ts          # 로깅 유틸리티
│   │   ├── requestHandler.ts   # API 요청 처리 유틸리티
│   │   ├── validation.ts       # 데이터 검증 유틸리티
│   ├── requirements.txt        # 공통 패키지 목록 (Playwright, API 관련 라이브러리 포함)
│   ├── README.md               # 공통 모듈 설명 문서
│
├── chrome-pc/                  # Chrome (Windows/Linux) 테스트 프로젝트
│   ├── src/
│   │   ├── tests/              # Playwright 테스트 스크립트
│   ├── pages/                  # POM 기반 페이지 객체
│   ├── locators/               # Chrome PC 전용 요소 위치 정보 (JSON 형식)
│   │   ├── loginPage.json      # 로그인 페이지 로케이터
│   │   ├── mainPage.json       # 메인 페이지 로케이터
│   ├── config/                 # 설정 파일
│   │   ├── playwright.config.ts # Playwright 설정 파일
│   ├── utils/                  # 테스트 유틸리티 모음
│   ├── components/             # Chrome PC 전용 UI 컴포넌트 모음
│   ├── logs/                   # 테스트 실행 로그
│   ├── test-results/           # 테스트 결과 저장소
│   ├── screenshots/            # 스크린샷 저장소
│   ├── requirements.txt        # Chrome PC 전용 추가 패키지
│   ├── Dockerfile              # Chrome PC 테스트용 Docker 설정
│   ├── README.md               # Chrome PC 테스트 프로젝트 설명 문서
│
```
```
PLAYWRIGHT-SAMPLE-PROJECT/
│── docs/                          # 문서화 관련 파일
│
├── src/                           # 소스 코드 폴더
│   ├── advantage/                 # UI 테스트 관련 폴더 (POM + Steps)
│   │   ├── constants/             # 상수 관리
│   │   ├── pages/                 # Page Object Model (POM) 폴더
│   │   ├── steps/                 # 테스트 실행 단계 관리
│   │   │   ├── DatabaseStep.ts    # DB 관련 Step 정의
│   │   ├── API/                    # API 테스트 관련 폴더
│   │
│   ├── database/                   # 데이터베이스 관련 모듈
│   │   ├── constants/               # DB 관련 상수
│   │   ├── steps/                   # DB 테스트 실행 단계
│   │
│   ├── framework/                   # 테스트 프레임워크 관련 설정
│   │   ├── config/                   # Playwright 설정 및 환경 설정
│   │   ├── constants/                # 전역 상수
│   │   ├── logger/                   # 로깅 시스템
│   │   ├── manager/                  # 브라우저 및 테스트 실행 매니저
│   │   ├── playwright/               # Playwright 관련 설정 및 실행 파일
│   │   ├── reporter/                 # 테스트 리포트 생성기
│   │   ├── template/                 # 템플릿 관련 파일 (예: 이메일 템플릿)
│   │   ├── utils/                    # 공통 유틸리티 함수 모음
│   │
│   ├── resources/                    # 기타 리소스 파일 (예: 데이터 파일)
│   ├── tests/                         # 테스트 실행 코드 (E2E 테스트 실행)
│
├── .env                               # 환경 변수 파일 (테스트 URL, API Key 등)
├── .eslintignore                      # ESLint 무시 파일
```
