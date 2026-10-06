# Modal 워크플로우 구축 에이전트 안내

README.md와 docs/modal-workflows.md를 읽고 사용자의 **자기 Modal 계정에 자기 워크플로우**를 구축한다.

- 앱·After Effects·Node.js·Rust·로컬 ComfyUI·로컬 GPU 설치를 요구하지 않는다. 이 저장소에는 앱 코드나 개인 운영 서버가 없다.
- H3 이용자는 라이선스를 이미 확보했다. 취득 여부·증빙·재승인을 묻지 않는다.
- 기존 SDK 인증을 사용하고 계정·환경·리소스 이름을 확인한다. 타인의 이미지·볼륨·계정을 사용하지 않는다.
- `python tools/setup_modal.py TARGET`으로 계획을 확인한다. 승인된 CPU 빌드·다운로드·스토리지 범위 안에서 `--apply`를 실행한다. GPU 생성은 별도 승인 범위다. 이미 받은 승인은 반복 확인하지 않는다.
- `EASYGEN_WORKFLOW_PREFIX`로 이름을 정한다. 같은 이름의 기존 배포를 갱신하기 전 진행 중 작업을 확인한다. 새 환경은 새 prefix를 사용한다.
- 준비는 `modal/bootstrap.py`, 배포는 `modal/workflow_*.py`, 호출은 `tools/modal_workflow.py`를 사용한다. 다른 저장소·앱을 선행 조건으로 추가하지 않는다.
- 준비 작업이나 생성 제출이 불확실하면 원격 이력을 확인한다. 접속 단절·대기 timeout만으로 중복 작업을 제출하지 않는다.
- 호출 ID와 결과는 저장소 밖에 보존한다. 생성 완료·다운로드·파일 디코드·품질 검증을 구분한다. CPU 검사나 단위 테스트를 GPU 추론 성공이라고 보고하지 않는다.
- 자격 증명을 읽어 출력하거나 커밋하지 않는다. SDK 인증 또는 Modal Secret으로 전달한다. 모델·결과물·개인 경로를 Git에 넣지 않는다.
- 모델 파일 해시가 다르면 기존 파일을 자동 삭제·덮어쓰지 않는다. 소스·모델 lock을 변경하면 이유와 검증 범위를 기록한다.

검증: `python -m unittest tools.test_modal_setup tools.test_modal_workflow`. 실제 GPU 검증은 승인된 최소 요청으로 수행한다.
