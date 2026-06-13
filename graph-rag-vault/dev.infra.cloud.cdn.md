---
id: "dev.infra.cloud.cdn"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "cloud", "cdn", "caching", "performance"]
brain_region: "CEREBELLUM"
token_estimate: 400
---

# dev.infra.cloud.cdn

> #267 CDN Architecture (Akamai, CloudFront Documentation)

# CDN (Content Delivery Network) 가이드

## 핵심 원칙
- 정적 자산을 사용자와 가까운 엣지 서버에서 서빙한다
- 캐시 정책을 자산 유형별로 세밀하게 설정한다
- 캐시 무효화(Invalidation) 전략을 명확히 정의한다
- 보안(HTTPS, WAF, DDoS 방어)을 CDN 레벨에서 적용한다

## DO
- 정적 자산(JS, CSS, 이미지)에 콘텐츠 해시 기반 파일명을 사용한다
- 해시 파일은 `max-age=31536000, immutable`로 장기 캐시한다
- HTML은 `max-age=0, s-maxage=60`으로 짧은 캐시를 설정한다
- Custom Domain에 SSL 인증서를 적용한다

## DON'T
- 인증이 필요한 API 응답을 CDN에 캐시하지 않는다
- 와일드카드 무효화(`/*`)를 빈번하게 사용하지 않는다
- 캐시 키에 불필요한 쿼리 파라미터를 포함하지 않는다
- 오리진 서버의 에러 응답을 장기간 캐시하지 않는다

## 코드 예시
```hcl
# CloudFront 배포 (Terraform)
resource "aws_cloudfront_distribution" "app" {
  origin {
    domain_name = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id   = "S3-static"
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-static"
    viewer_protocol_policy = "redirect-to-https"

    cache_policy_id = aws_cloudfront_cache_policy.static.id
  }

  # API 경로는 캐시하지 않음
  ordered_cache_behavior {
    path_pattern     = "/api/*"
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    target_origin_id = "API-origin"
    cache_policy_id  = data.aws_cloudfront_cache_policy.caching_disabled.id
    viewer_protocol_policy = "https-only"
  }
}
```

```nginx
# 캐시 헤더 설정 예시
# 해시된 정적 자산: 1년 캐시
location ~* \.[a-f0-9]{8,}\.(js|css|woff2)$ {
  add_header Cache-Control "public, max-age=31536000, immutable";
}

# HTML: CDN 60초, 브라우저 캐시 없음
location ~* \.html$ {
  add_header Cache-Control "public, max-age=0, s-maxage=60";
}
```
