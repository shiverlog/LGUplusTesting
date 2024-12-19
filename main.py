from behave import __main__ as behave_runner

if __name__ == '__main__':
    behave_runner.main([
        '-f', 'pretty',  # 보고서 형식 지정 (선택 사항)
        'features',  # Feature 파일이 있는 디렉토리 경로 (필수)
        # '--name', '테스트 시나리오 이름'  # 특정 시나리오만 실행 (선택 사항)
    ])