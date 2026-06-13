---
id: "dev.infra.cloud.terraform"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "cloud", "terraform", "iac"]
brain_region: "CEREBELLUM"
token_estimate: 420
---

# dev.infra.cloud.terraform

> #265 Infrastructure as Code (HashiCorp, Terraform 2014)

# Terraform 가이드

## 핵심 원칙
- 인프라를 코드로 선언하여 재현 가능하고 버전 관리 가능하게 한다
- 상태(State)를 원격 백엔드(S3 + DynamoDB)에 저장한다
- 모듈을 활용하여 재사용 가능한 인프라 패턴을 만든다
- Plan → Apply → Verify 워크플로를 따른다

## DO
- 원격 상태 저장소를 사용한다 (S3 + DynamoDB Lock)
- 환경별(dev/staging/prod) 워크스페이스 또는 디렉토리를 분리한다
- `terraform plan`을 PR에서 자동 실행하고 결과를 리뷰한다
- 리소스 네이밍 규칙을 일관되게 적용한다
- sensitive 변수를 `sensitive = true`로 표시한다

## DON'T
- 로컬에 상태 파일(terraform.tfstate)을 보관하지 않는다
- `terraform apply -auto-approve`를 프로덕션에서 사용하지 않는다
- 하나의 state 파일에 모든 리소스를 넣지 않는다 (분리)
- 수동으로 만든 리소스를 Terraform으로 관리하지 않는다 (import 필요)

## 코드 예시
```hcl
# 원격 백엔드 설정
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "ap-northeast-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

# 모듈 사용
module "web_server" {
  source = "./modules/ecs-service"

  name          = "my-app"
  environment   = var.environment
  image         = "${var.ecr_repo}:${var.image_tag}"
  cpu           = 256
  memory        = 512
  desired_count = var.environment == "production" ? 3 : 1

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
}

# 변수 정의
variable "environment" {
  type        = string
  description = "배포 환경 (dev, staging, production)"
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "environment는 dev, staging, production 중 하나여야 합니다."
  }
}
```
