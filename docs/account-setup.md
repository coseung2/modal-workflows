# 처음 시작하기: 가입·카드·API 토큰

확인 기준: 2026-10-06. 계정 준비는 사용자가 직접 하고 이후 구축은 에이전트에 맡깁니다. 이미 완료한 단계를 반복하지 않습니다.

## 1. 가입과 워크스페이스

[Modal 가입](https://modal.com/signup)에서 계정을 만들고 로그인합니다. 사용할 자신의 워크스페이스를 선택하거나 생성합니다. 이후 카드·토큰·배포는 모두 같은 워크스페이스를 대상으로 합니다.

## 2. 카드 등록과 Starter 크레딧

Settings의 **Usage & Billing → Manage payment details**에서 결제 수단을 등록합니다. 연결되는 결제 화면에서 사용자 본인의 카드와 청구 정보를 직접 입력합니다. Modal은 서비스를 사용하려면 등록된 결제 수단이 필요하다고 안내합니다. [공식 Billing 안내](https://modal.com/docs/guide/billing)

Starter는 기본 구독료 $0에 사용량 과금이 더해지며 **매월 $30의 무료 컴퓨트 크레딧**이 포함됩니다. 일회성 가입 보너스나 무제한 무료 사용이 아닙니다. 카드 등록 후 Usage & Billing에서 Starter 플랜과 크레딧 적용 상태를 확인하세요. 초과분이나 크레딧 적용 대상이 아닌 사용은 청구될 수 있습니다. [공식 가격표](https://modal.com/pricing)

카드 등록은 사용자만 수행합니다. 에이전트에 카드 번호를 전달하지 않습니다. 크레딧이 있다는 사실만으로 모든 유료 실행을 허용한 것은 아니며, 에이전트에 작업 종류·횟수·비용 범위를 알려줍니다.

## 3. API 토큰 발급

아래 CLI 명령은 먼저 [README의 uv 준비](../README.md#1-로컬-준비)를 마친 뒤 저장소 루트에서 실행합니다. Python 별도 설치나 가상환경 활성화는 필요 없습니다.

Modal Dashboard에서 사용할 워크스페이스의 설정으로 이동해 **API Tokens**를 찾아 토큰을 생성합니다. 토큰은 **Token ID와 Token Secret 한 쌍**입니다. 이 저장소의 SDK 인증에는 API 토큰을 사용하며 웹 엔드포인트용 Proxy Token과 구분합니다. [공식 SDK 인증 안내](https://modal.com/docs/guide/trigger-deployed-functions)

토큰 발급 화면의 유효기간과 권한을 확인하고, 값은 자신의 비밀 저장소 또는 에이전트 실행기의 Secret 설정에 보관합니다. 토큰 원문을 채팅·스크린샷·Git·요청 JSON에 넣지 않습니다.

PC에서만 사용할 경우 수동 환경 변수 대신 아래 CLI 인증을 선택해도 됩니다. 별도 토큰을 중복 발급할 필요는 없습니다.

```sh
uv run python -m modal setup
```

이미 SDK가 설치돼 있고 새 CLI 토큰을 직접 발급하려면 `uv run python -m modal token new`를 사용합니다. 기존에 발급받은 토큰을 CLI 저장소에 입력하려면 `uv run python -m modal token set`의 입력 프롬프트를 사용합니다. [공식 토큰 CLI](https://modal.com/docs/cli/latest/token)

## 4. 환경 변수로 전달하는 경우

에이전트 실행기의 비밀 환경 변수에 다음 두 이름을 등록하고 해당 실행기를 다시 시작합니다.

| 이름 | 값 |
| --- | --- |
| `MODAL_TOKEN_ID` | 발급받은 Token ID |
| `MODAL_TOKEN_SECRET` | 함께 발급받은 Token Secret |

환경 변수는 CLI 프로필보다 우선할 수 있습니다. 다른 계정의 변수가 남아 있지 않은지 값 자체를 출력하지 않고 확인하세요. 프로젝트의 `.env` 파일에 적는 것만으로 이 도구가 자동으로 읽지는 않습니다. [Modal 설정 문서](https://modal.com/docs/sdk/py/latest/config)

### PowerShell 7: 현재 터미널 세션

아래는 실제 값을 명령 기록에 적지 않고 사용자 입력으로 받는 방법입니다.

```powershell
$env:MODAL_TOKEN_ID = Read-Host 'Modal Token ID' -MaskInput
$env:MODAL_TOKEN_SECRET = Read-Host 'Modal Token Secret' -MaskInput
uv run python -m modal app list --json
```

이 터미널에서 실행한 Python·CLI·에이전트 자식 프로세스에 적용됩니다. 이미 실행 중인 별도 데스크톱 에이전트에는 전달되지 않습니다. 그 경우 실행기의 Secret 설정이나 CLI 인증을 이용합니다. 터미널을 닫으면 이 방식의 설정은 사라집니다.

### macOS/Linux: Bash 세션

```bash
read -r -s -p 'Modal Token ID: ' MODAL_TOKEN_ID; echo
read -r -s -p 'Modal Token Secret: ' MODAL_TOKEN_SECRET; echo
export MODAL_TOKEN_ID MODAL_TOKEN_SECRET
uv run python -m modal app list --json
```

현재 Bash와 그 자식 프로세스에만 적용됩니다. 다른 셸에서는 실행기의 Secret 설정 또는 CLI 인증을 사용합니다.

## 5. 연결 확인과 에이전트 인계

저장소 README대로 Python 가상환경과 `requirements.txt`를 준비한 뒤:

```sh
uv run python -m modal app list --json
uv run python -m modal volume list
uv run python tools/setup_modal.py h3
```

새 계정이라 앱·볼륨 목록이 비어 있어도 오류 없이 조회되면 인증 연결은 된 것입니다. 이것만으로 카드 등록·크레딧·GPU 실행 가능 여부까지 확인된 것은 아닙니다. 결제·크레딧 상태는 사용자가 Dashboard에서 확인합니다.

에이전트에는 다음처럼 알려줍니다:

> 내 Modal 가입·카드 등록과 Starter 크레딧 적용을 확인했고 인증도 준비했어. 이 계정에서 [워크플로우 이름]으로 H3 환경을 구축해줘. H3 라이선스는 이미 확보했어. 먼저 다운로드·실행 계획을 보여주고 내가 승인한 비용 범위 안에서 진행해줘.

이후 [워크플로우 구축 안내](modal-workflows.md)를 따릅니다. API 토큰 발급·카드 등록을 에이전트가 했다고 보고하거나, 사용자 확인 없이 결제 준비 완료라고 가정하지 않습니다.
