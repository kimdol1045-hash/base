---
id: "dev.ai.multi-modal"
domain: "development.ai"
type: "pattern"
bloom_level: ""
tags: ["ai", "multi-modal", "vision", "image"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.ai.multi-modal

> #288 Multi-Modal AI (GPT-4V, OpenAI 2023; Claude 3 Vision, Anthropic 2024)

# 멀티모달 AI 가이드

## 핵심 원칙
- 텍스트, 이미지, 오디오 등 여러 모달리티를 함께 처리한다
- 이미지 입력 시 토큰 소비량을 고려한다
- 이미지 해상도와 품질의 트레이드오프를 관리한다
- 비전 기능의 한계를 이해하고 적절히 활용한다

## DO
- 이미지를 적절한 해상도로 리사이즈하여 토큰을 절약한다
- 이미지와 텍스트 프롬프트를 함께 제공하여 맥락을 보강한다
- OCR, 차트 분석, UI 검수 등에 비전 기능을 활용한다
- Base64 인코딩 대신 URL 참조를 사용한다 (가능한 경우)

## DON'T
- 고해상도 이미지를 원본 그대로 전송하지 않는다
- 텍스트만으로 충분한 작업에 이미지를 불필요하게 포함하지 않는다
- 비전 모델로 정밀한 수치 인식(OCR)에만 의존하지 않는다
- 민감한 이미지(개인 사진, 의료 이미지)를 무분별하게 API에 전송하지 않는다

## 코드 예시
```typescript
import Anthropic from "@anthropic-ai/sdk";
import sharp from "sharp";

const anthropic = new Anthropic();

// 이미지 전처리: 해상도 제한
async function prepareImage(imagePath: string): Promise<string> {
  const buffer = await sharp(imagePath)
    .resize(1024, 1024, { fit: "inside" })
    .jpeg({ quality: 85 })
    .toBuffer();
  return buffer.toString("base64");
}

// 멀티모달 요청
async function analyzeUI(screenshotPath: string) {
  const imageData = await prepareImage(screenshotPath);

  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [{
      role: "user",
      content: [
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/jpeg",
            data: imageData,
          },
        },
        {
          type: "text",
          text: `이 UI 스크린샷을 분석하여 다음을 평가하세요:
          1. 접근성 문제 (색상 대비, 터치 대상 크기)
          2. 레이아웃 정렬 문제
          3. 텍스트 가독성
          JSON 형식으로 응답하세요.`,
        },
      ],
    }],
  });

  return JSON.parse(response.content[0].text);
}
```
