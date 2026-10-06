# 무드보드: 같은 장면의 6가지 방향

무드보드는 **한 이미지 안에 3열 × 2행의 6칸 그리드**로 만든다. 사용자가 번호로 방향을 선택하는 비교 자료다. 여섯 장면의 스토리보드가 아니다.

## 에이전트 작업 순서

1. 요청을 대표하는 장면 하나를 정한다. 피사체·행동·공간·주요 사물·카메라 각도·프레이밍·배치를 문장으로 고정한다.
2. 그 장면에 적용할 시각 방향 6개를 설계한다. 색감·화풍·재질·조명·분위기에 충분한 차이를 주되, 장면과 구도는 유지한다. 사용자가 정한 캐릭터·제품 특징도 유지한다.
3. 이미지 생성 **한 번으로 그리드 한 장**을 요청한다. 6장을 따로 생성해 붙이는 것을 기본 방식으로 삼지 않는다. 각 칸은 같은 크기이며 최종 영상의 화면 비율을 따른다. 전체 이미지 비율은 3열 × 2행 배치에 맞춘다.
4. 좌상단부터 가로 순서로 1–6 번호를 붙인다. 얇은 구분선과 작은 숫자만 사용하고 긴 설명은 이미지 밖에 둔다. 번호가 잘못 생성되면 로컬 도구로 정확히 표시한다.
5. 여섯 칸 모두 동일 장면·구도인지, 서로 비교 가능한 차이가 있는지 확인한다. 보드와 함께 번호·방향 이름·특징을 짧게 제시하고 사용자가 선택하도록 한다.
6. 사용자의 선택을 받기 전 임의로 한 방향을 확정해 후속 생성을 진행하지 않는다. 이미 방향을 선택했거나 선택을 위임했다면 반복 질문하지 않는다. 선택된 방향을 캐릭터·스토리보드·생성 프롬프트에 일관되게 적용한다.

그리드 전체를 H3의 단일 장면 입력으로 사용하지 않는다. 영상 입력이 필요하면 선택된 방향으로 격자·번호가 없는 장면 이미지를 별도로 준비한다. 추가 생성은 승인된 호출 범위를 따른다.

## 생성 프롬프트 템플릿

대괄호를 실제 작업 내용으로 모두 채워 사용한다. 시각 방향은 주제에 맞게 설계하며 여섯 칸에 서로 다른 사건·피사체·카메라 구도를 배정하지 않는다.

```text
Create ONE moodboard image containing exactly six equal panels arranged in a clean 3-column by 2-row grid. Each panel has a [TARGET ASPECT RATIO] aspect ratio. Use thin, consistent dividers.

Show the SAME scene in every panel: [SUBJECT, ACTION, SETTING, AND KEY OBJECTS]. Preserve the same subject identity, pose, camera angle, framing, composition, object placement, and scene content across all six panels. These are six alternative visual treatments of one scene, not six sequential story moments.

Vary only the visual treatment: palette, rendering style, material treatment, lighting quality, and mood.

Panel 1, top left: [VISUAL DIRECTION 1].
Panel 2, top middle: [VISUAL DIRECTION 2].
Panel 3, top right: [VISUAL DIRECTION 3].
Panel 4, bottom left: [VISUAL DIRECTION 4].
Panel 5, bottom middle: [VISUAL DIRECTION 5].
Panel 6, bottom right: [VISUAL DIRECTION 6].

Make the six treatments clearly distinguishable while keeping their scene and composition directly comparable. Place a small readable number 1 through 6 in the corresponding panel. No captions, titles, logos, or additional text. Deliver the complete six-panel board as one image.
```
