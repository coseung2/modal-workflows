# Modal Workflows

**자신의 Modal 계정에 영상·이미지·음악 생성 워크플로우를 구축하는 안내와 실행 코드**입니다. 코딩 에이전트가 환경 빌드, 모델 다운로드, 배포, 생성과 결과 회수까지 진행할 수 있습니다.

앱 코드나 개인 운영 서버는 포함하지 않습니다. **앱·After Effects·Node.js·Rust·로컬 GPU·로컬 ComfyUI는 필요 없습니다.** uv, Git, 자신의 Modal 계정을 준비합니다. Python 3.12는 uv가 준비합니다. FFmpeg는 다운로드한 미디어 검증에 선택적으로 사용합니다.

H3 이용자는 **이용 라이선스를 이미 확보한 것으로 전제**합니다. 에이전트가 취득 여부나 증빙을 다시 묻지 않습니다. Modal 인증, 모델 다운로드 접근권과 비용 사용 범위는 각자 자신의 환경에서 설정합니다.

## 에이전트에게 요청하기

**[워크플로우별 예제 작업](examples/README.md)**에서 H3 텍스트·이미지·참조 영상, Krea 이미지, Ideogram 포스터, YuE2 노래, 6칸 무드보드를 골라 시작하세요. 바로 쓸 요청 JSON과 캐릭터 시트·TTS·스토리보드·후속 편집 연결 예제를 제공합니다.

환경 준비 후에는 **인물이 컵을 들어 올려 한 모금 마시는 도자기 컵 광고**를 완성하는 연결 예제를 제안합니다. 무드보드와 캐릭터 시트를 고르고, 인물 행동·카메라·음성 타이밍을 담은 스토리보드를 승인한 다음 장면 이미지와 영상을 생성합니다. 컵만 보여주는 제품 단독 영상은 별도로 선택할 수 있습니다.

**사용자는 대화하고, 에이전트가 준비·생성·후속 편집을 진행합니다.** 예를 들어 “이 캐릭터로 10초 영상을 만들고, 내레이션과 자막을 붙여줘”라고 요청할 수 있습니다. 에이전트가 로컬 편집 환경도 확인하고 필요한 도구를 추천합니다. H3는 클립당 최대 15초를 요청할 수 있으며 긴 영상은 여러 클립을 편집해 구성합니다.

[추천 제작 파이프라인](docs/production-pipelines.md)에 무드보드·캐릭터 시트·스토리보드·TTS·로컬 편집의 순서와 도구 선택을 정리했습니다. 캐릭터 시트는 [기본 프롬프트](prompts/character-sheet.md)를 요청에 맞게 변형하고, TTS 기본 추천은 Google Gemini 3.8 Flash TTS입니다. TTS는 별도 Google API 경로이며 현재 이 레포에 전용 호출 CLI가 포함된 것은 아닙니다.

> 이 저장소의 README.md, AGENTS.md와 docs/modal-workflows.md를 읽고 내 Modal 계정에 독립 워크플로우를 구축해줘. 사용할 종류는 [H3 영상/이미지/YuE2 음악], 워크플로우 이름은 [이름]이야. 앱이나 After Effects는 설치하지 마. H3 라이선스는 이미 확보했으니 다시 묻지 마. 준비 계획과 다운로드 규모·비용 범위를 확인한 뒤 환경을 만들고, 승인된 생성 1건으로 결과까지 검증해줘. 원격 호출 ID를 보존하고 접속이 끊겨도 중복 제출하지 마.

무드보드는 **같은 장면을 한 이미지의 6칸 그리드(3열 × 2행)**로 보여줍니다. 사용자가 번호로 원하는 스타일을 고르면 에이전트가 그 방향으로 제작을 이어갑니다. [무드보드 구성·프롬프트](prompts/moodboard.md)

광고 제작은 [연출·컷 편집 가이드](docs/direction-and-editing.md)와 [온유 ONYU 20초 연출안](examples/onyu-direction.md)을 따릅니다. 후킹·카메라·시점·트랜지션·음향·폰트·브랜드 노출을 먼저 설계하고, 그 편집에 필요한 클립을 생성합니다.

## 0. 가입·카드 등록·API 토큰 준비

처음 사용한다면 **[계정 준비 안내](docs/account-setup.md)**를 먼저 따르세요.

1. Modal에 가입하고 자신의 워크스페이스를 선택합니다.
2. **카드를 등록합니다.** Modal 사용에는 결제 수단이 필요하며, Starter 플랜은 **매월 $30 컴퓨트 크레딧**을 제공합니다. 일회성 가입 보너스가 아닙니다. 등록 후 Usage & Billing에서 플랜·크레딧 적용을 확인하세요. [공식 결제 안내](https://modal.com/docs/guide/billing), [Starter 요금](https://modal.com/pricing)
3. 자신의 API 토큰을 발급하고 `MODAL_TOKEN_ID`, `MODAL_TOKEN_SECRET`을 에이전트 실행 환경에 설정하거나 CLI 인증을 사용합니다.
4. 연결 확인 후 에이전트가 환경 구축을 이어갑니다. 가입·카드 입력·토큰 전달은 사용자가 직접 하며 값을 채팅에 붙여 넣지 않습니다.

크레딧 초과 사용은 청구될 수 있으므로 실행 전에 비용 범위를 정합니다.

## 1. 로컬 준비

먼저 `uv --version`으로 설치 여부를 확인합니다. 없으면 Windows에서는 `winget install --id=astral-sh.uv -e`, macOS에서는 `brew install uv`를 사용할 수 있습니다. Linux 또는 다른 설치 방법은 [uv 공식 설치 안내](https://docs.astral.sh/uv/getting-started/installation/)를 따릅니다. 설치 후 필요하면 터미널을 다시 엽니다.

```sh
git clone https://github.com/coseung2/modal-workflows.git
cd modal-workflows
uv venv --python 3.12
uv pip install --python .venv -r requirements.txt
```

Python 3.12가 없으면 uv가 내려받습니다. 가상환경 활성화 없이 **저장소 루트에서 `uv run python ...`**으로 실행합니다. 기존 `.venv`가 있으면 먼저 Python 버전을 확인하고, 다른 환경을 임의로 삭제하거나 덮어쓰지 않습니다.

```sh
uv run python --version
uv run python -m modal profile current
uv run python -m modal app list --json
```

인증이 없다면 `uv run python -m modal setup`에서 사용자가 한 번 인증합니다. 기존 인증이 있으면 재발급하지 않습니다. 자동화 환경에서는 자신의 Modal API 토큰을 비밀 환경 변수로 제공할 수 있습니다. 토큰을 채팅·요청 JSON·Git에 넣지 않습니다.

## 2. 자기 워크플로우 구축

```sh
# 로컬 계획만 출력: 원격 실행·다운로드 없음
uv run python tools/setup_modal.py h3
# 승인한 CPU 빌드·다운로드·배포를 실제 수행
uv run python tools/setup_modal.py h3 --apply
```

이미지는 `image`, 음악은 `music`으로 바꿉니다. 필요한 종류만 실행하세요.

| 대상 | 기본 배포 이름 | 모델 다운로드 | 결과 |
| --- | --- | --- | --- |
| H3 | `my-workflow-h3` | 약 72.96 GiB | 최종·업스케일 전 MP4 |
| Krea 2 Turbo·Ideogram 4 | `my-workflow-image` | 약 44.82 GiB | PNG |
| YuE2 | `my-workflow-music` | 약 7.26 GiB | FLAC |

이름을 정하려면 준비·배포·요청 준비 전에 `EASYGEN_WORKFLOW_PREFIX`를 설정하세요. PowerShell 예: `$env:EASYGEN_WORKFLOW_PREFIX = 'my-studio'`. macOS/Linux 예: `export EASYGEN_WORKFLOW_PREFIX=my-studio`. 그러면 `my-studio-h3` 등으로 생성됩니다. 같은 이름이 이미 있으면 갱신하므로 별도 구축에는 새 이름을 사용합니다.

`--apply`는 자신의 계정에서 공개 이미지 빌드 → CPU 노드 검사 → 모델 다운로드·SHA-256 검사 → 배포를 수행합니다. 유지보수자의 이미지 ID·모델 볼륨·비공개 패키지는 사용하지 않습니다. **CPU 실행·다운로드·스토리지 비용이 발생할 수 있으며 GPU 생성은 아직 실행하지 않습니다.**

모델 출처·고정 revision·해시는 [모델 목록](easygen_runtime/models.json), ComfyUI·custom node 버전은 [소스 목록](easygen_runtime/sources.json)에 있습니다. 접근 인증, 다운로드 재개와 개별 배포 명령은 [상세 안내](docs/modal-workflows.md)를 따르세요.

## 3. 생성·조회·다운로드

환경 구축이 끝나면 에이전트가 **“가상 도자기 브랜드 온유 ONYU의 상업 광고 영상을 무드보드부터 내레이션·영상 생성·자막·최종 편집까지 완성해볼까요?”**라고 먼저 제안합니다. 동의하면 필요한 도구·서비스·비용을 확인하고, 6칸 무드보드에서 선택한 방향으로 [연결 예제](examples/README.md)를 끝까지 진행합니다. 이미 전체 실행을 요청했다면 같은 승인을 반복해서 묻지 않습니다.

저장소 밖 `video-request.json`에 요청을 저장합니다.

```json
{
  "mode": "text",
  "prompt": "A small sailboat crossing a calm lake, slow camera pan.",
  "seconds": 2,
  "width": 1344,
  "height": 768,
  "seed": 42
}
```

```sh
uv run python tools/modal_workflow.py prepare video --request ../video-request.json --out ../video-run
# 승인된 GPU 생성 1건 제출
uv run python tools/modal_workflow.py submit ../video-run
uv run python tools/modal_workflow.py status ../video-run
# completed 이후
uv run python tools/modal_workflow.py download ../video-run
```

`prepare`는 로컬 검사만 합니다. `submit`은 유료 GPU 실행을 제출하고 호출 ID를 보존합니다. `status`는 한 번 조회하고 종료하므로 진행 중이면 30–60초 후 같은 폴더를 다시 조회하세요. 응답이 늦다고 재제출하지 않습니다. 중단 요청은 `cancel`입니다.

이미지·음악 요청, 참조 영상 입력, 취소·복구·검증은 [종류별 상세 실행 안내](docs/modal-workflows.md#4-앱-없이-직접-실행)에 있습니다. 출력과 실행 상태는 원하는 저장소 밖 폴더에 보관합니다.

## 코드 구성

| 경로 | 역할 |
| --- | --- |
| `tools/setup_modal.py` | 환경 구축 계획·실행 |
| `tools/modal_workflow.py` | 생성 준비·제출·조회·회수·취소 |
| `modal/workflow_*.py` | 사용자의 독립 GPU 워크플로우 |
| `modal/bootstrap.py` | CPU 모델 다운로드·검증 |
| `modal/check_environment.py` | 공개 이미지 빌드·CPU 노드 검사 |
| `easygen_runtime/` | 공개 빌드 정의, 리소스 이름, 모델·소스 목록 |
| `worker/graphs/`, `worker/h3_graph.py` | H3 UI JSON과 API 변환 |

H3는 JSON 그래프를 사용합니다. **YuE2는 ComfyUI JSON이 아닌 Python 파이프라인**입니다. 이미지 그래프도 Python 함수로 정의돼 있습니다. 모델 가중치·영상 제작 관리·레퍼런스 수집 시스템은 이 저장소에 포함하지 않습니다.

## 검증 범위

```sh
uv run python -m unittest tools.test_modal_setup tools.test_modal_workflow
```

공개 소스 이미지 빌드와 CPU 필수 노드 14개 등록을 실제 확인했습니다. 새 계정의 전체 모델 다운로드와 GPU 추론은 사용자 환경에서 별도로 검증해야 합니다. [검증 기록](docs/modal-bootstrap-verification.md)에 확인한 범위와 미검증 범위를 구분했습니다.
