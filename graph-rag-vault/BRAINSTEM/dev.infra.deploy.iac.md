---
id: "dev.infra.deploy.iac"
domain: "development.infra"
type: "pattern"
region: BRAINSTEM
token_estimate: 420
theory: "#151 Infrastructure as Code (Kief Morris, 2016)"
tags: [infra, iac, terraform, devops]
---

# dev.infra.deploy.iac

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.infra`  
> **Type**: `pattern`  
> **Theory**: #151 Infrastructure as Code (Kief Morris, 2016)  
> **Tokens**: 420

## Content

Infrastructure as Code (인프라를 코드로 관리하여 재현성을 보장한다):

### 핵심 원칙
- 모든 인프라를 코드로 정의 (수동 변경 금지)
- 버전 관리 (Git) 필수
- 멱등성: 같은 코드 여러 번 실행해도 결과 동일
- 불변 인프라: 수정 대신 교체 (서버 패치 X → 새 이미지 배포)

### 도구 비교
| 도구 | 용도 | 접근 방식 |
|------|------|----------|
| Terraform | 인프라 프로비저닝 | 선언적 (HCL) |
| Pulumi | 인프라 프로비저닝 | 명령적 (TS/Python) |
| Ansible | 구성 관리 | 절차적 (YAML) |
| Docker Compose | 로컬 오케스트레이션 | 선언적 (YAML) |

### Terraform 예시
```hcl
resource "aws_instance" "app" {
  ami           = "ami-xxx"
  instance_type = "t3.micro"

  tags = {
    Name        = "app-server"
    Environment = var.environment
  }
}
```

### 디렉토리 구조
```
infra/
  modules/          # 재사용 가능한 모듈
    networking/
    compute/
  environments/     # 환경별 설정
    dev/
    staging/
    prod/
  variables.tf      # 변수 정의
  outputs.tf        # 출력 정의
```

### 주의사항
- State 파일 원격 저장 (S3 + DynamoDB Lock)
- 시크릿은 코드에 포함 금지 (Vault, AWS Secrets Manager)
- Plan → Review → Apply 워크플로우 필수
- 환경별 변수 분리 (tfvars)

## Connections

*Connections will be populated by Graph RAG ingest.*
