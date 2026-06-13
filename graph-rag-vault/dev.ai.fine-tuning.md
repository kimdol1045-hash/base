---
id: "dev.ai.fine-tuning"
domain: "development.ai"
type: "pattern"
bloom_level: ""
tags: ["ai", "fine-tuning", "lora", "training"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.ai.fine-tuning

> #281 Fine-Tuning LLMs (OpenAI Fine-Tuning Guide, 2023; LoRA, Hu et al. 2021)

# LLM 파인튜닝 가이드

## 핵심 원칙
- 프롬프트 엔지니어링 → Few-shot → RAG → 파인튜닝 순으로 시도한다
- 파인튜닝은 특정 형식, 톤, 도메인 전문성이 필요할 때 사용한다
- 고품질 학습 데이터가 모델 성능을 결정한다
- LoRA/QLoRA로 효율적으로 파인튜닝한다

## DO
- 최소 100개 이상의 고품질 학습 데이터를 준비한다
- 학습/검증/테스트 세트를 분리한다 (80/10/10)
- 평가 지표를 미리 정의하고 기준선(baseline)을 측정한다
- LoRA로 파라미터 효율적 파인튜닝(PEFT)을 수행한다
- 과적합(overfitting)을 모니터링한다

## DON'T
- 프롬프트로 해결 가능한 문제에 파인튜닝을 사용하지 않는다
- 저품질 데이터로 파인튜닝하지 않는다 (Garbage In, Garbage Out)
- 평가 없이 파인튜닝된 모델을 배포하지 않는다
- 전체 모델 파라미터를 파인튜닝하지 않는다 (LoRA 사용)

## 파인튜닝 적합 시나리오
| 시나리오 | 파인튜닝 | 프롬프트/RAG |
|----------|----------|-------------|
| 특정 출력 형식 일관성 | O | - |
| 도메인 전문 용어 이해 | O | - |
| 새로운 사실 학습 | - | RAG |
| 특정 톤/스타일 유지 | O | 프롬프트 |
| 비용 절감 (토큰 절약) | O | - |

## 코드 예시
```python
# LoRA 파인튜닝 (Hugging Face + PEFT)
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM, TrainingArguments, Trainer

# LoRA 설정
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                    # LoRA rank
    lora_alpha=32,           # 스케일링 팩터
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj"],  # Attention 레이어만 튜닝
)

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3-8B")
model = get_peft_model(model, lora_config)
print(f"학습 가능 파라미터: {model.print_trainable_parameters()}")
# 전체의 ~0.5%만 학습

# 학습
trainer = Trainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    args=TrainingArguments(
        output_dir="./output",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        learning_rate=2e-4,
        evaluation_strategy="steps",
        eval_steps=100,
    ),
)
trainer.train()
```
