---
id: "dev.infra.cloud.multi-region"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "cloud", "multi-region", "disaster-recovery", "high-availability"]
brain_region: "CEREBELLUM"
token_estimate: 420
---

# dev.infra.cloud.multi-region

> #268 Multi-Region Architecture (AWS Multi-Region Best Practices, 2023)

# 멀티 리전 아키텍처 가이드

## 핵심 원칙
- 지리적으로 분산된 리전에 서비스를 배포하여 가용성을 극대화한다
- 데이터 복제 전략(동기/비동기)을 요구사항에 맞게 선택한다
- RPO(Recovery Point Objective)와 RTO(Recovery Time Objective)를 명확히 정의한다
- 비용과 복잡성 대비 비즈니스 필요성을 평가한다

## 배포 전략
| 전략 | RPO | RTO | 비용 | 복잡도 |
|------|-----|-----|------|--------|
| Active-Passive | 분~시간 | 분~시간 | 중 | 중 |
| Active-Active | 거의 0 | 거의 0 | 높음 | 높음 |
| Pilot Light | 분 | 10분~1시간 | 낮음 | 낮음 |

## DO
- Route 53 헬스체크로 자동 페일오버를 구성한다
- 데이터베이스 복제 지연(Replication Lag)을 모니터링한다
- 각 리전에서 독립적으로 동작할 수 있도록 설계한다
- 정기적으로 페일오버 테스트(Game Day)를 수행한다

## DON'T
- 모든 서비스에 멀티 리전을 적용하지 않는다 (비용 대비 효과 평가)
- 동기 복제로 인한 지연시간 증가를 무시하지 않는다
- 리전 간 데이터 일관성 문제를 간과하지 않는다
- 페일오버 테스트 없이 운영하지 않는다

## 코드 예시
```hcl
# Terraform - Active-Passive 멀티 리전
# Primary: ap-northeast-2 (서울)
module "primary" {
  source      = "./modules/app-stack"
  region      = "ap-northeast-2"
  is_primary  = true
  providers   = { aws = aws.primary }
}

# Secondary: ap-northeast-1 (도쿄)
module "secondary" {
  source      = "./modules/app-stack"
  region      = "ap-northeast-1"
  is_primary  = false
  providers   = { aws = aws.secondary }
}

# Route 53 페일오버 라우팅
resource "aws_route53_record" "primary" {
  zone_id = var.zone_id
  name    = "api.example.com"
  type    = "A"
  set_identifier = "primary"
  failover_routing_policy { type = "PRIMARY" }
  alias {
    name    = module.primary.alb_dns_name
    zone_id = module.primary.alb_zone_id
  }
  health_check_id = aws_route53_health_check.primary.id
}

resource "aws_route53_record" "secondary" {
  zone_id = var.zone_id
  name    = "api.example.com"
  type    = "A"
  set_identifier = "secondary"
  failover_routing_policy { type = "SECONDARY" }
  alias {
    name    = module.secondary.alb_dns_name
    zone_id = module.secondary.alb_zone_id
  }
}

# RDS 교차 리전 읽기 복제본
resource "aws_rds_cluster" "secondary" {
  provider               = aws.secondary
  replication_source_identifier = module.primary.rds_cluster_arn
  engine                 = "aurora-postgresql"
}
```
