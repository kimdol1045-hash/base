---
id: "dev.infra.cloud.aws-well-architected"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "cloud", "aws", "architecture", "well-architected"]
brain_region: "CEREBELLUM"
token_estimate: 420
---

# dev.infra.cloud.aws-well-architected

> #264 AWS Well-Architected Framework (AWS, 2015)

# AWS Well-Architected 가이드

## 핵심 원칙
- 6개 기둥(Pillar)에 따라 아키텍처를 설계하고 검증한다
- 운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속 가능성
- 정기적으로 Well-Architected Review를 수행한다
- 트레이드오프를 인식하고 비즈니스 요구사항에 맞게 결정한다

## 6대 기둥 핵심 체크리스트
| 기둥 | 핵심 질문 |
|------|-----------|
| 운영 우수성 | IaC로 관리되는가? 자동화된 배포인가? |
| 보안 | 최소 권한 원칙을 따르는가? 암호화가 적용되는가? |
| 안정성 | 장애 시 자동 복구되는가? 다중 AZ인가? |
| 성능 효율성 | 워크로드에 적합한 리소스 타입인가? |
| 비용 최적화 | 미사용 리소스가 있는가? 예약 인스턴스를 활용하는가? |
| 지속 가능성 | 리소스 사용을 최소화하고 있는가? |

## DO
- 모든 인프라를 IaC(Terraform/CDK)로 관리한다
- 다중 AZ(Availability Zone) 배포를 기본으로 한다
- IAM 정책에 최소 권한 원칙을 적용한다
- 비용 알림과 예산을 설정한다
- 정기적으로 AWS Trusted Advisor를 확인한다

## DON'T
- AWS Console에서 수동으로 리소스를 생성하지 않는다
- Root 계정을 일상 작업에 사용하지 않는다
- 단일 AZ에 모든 리소스를 배치하지 않는다
- 액세스 키를 코드에 하드코딩하지 않는다
- 비용 모니터링 없이 리소스를 무한정 생성하지 않는다

## 코드 예시
```hcl
# Terraform - Well-Architected 기본 패턴
# 다중 AZ VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  azs     = ["ap-northeast-2a", "ap-northeast-2b", "ap-northeast-2c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  enable_nat_gateway = true
}

# 최소 권한 IAM
resource "aws_iam_policy" "app_policy" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:PutObject"]
      Resource = "${aws_s3_bucket.app.arn}/*"
    }]
  })
}
```
