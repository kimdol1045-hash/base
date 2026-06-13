---
id: "dev.backend.api.file-upload"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "api", "file-upload", "s3", "presigned-url", "security"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.api.file-upload

> #116 OWASP A04 Insecure Design

파일 업로드 패턴 (서버를 경유하지 않고 Presigned URL로 직접 업로드한다 -- 서버 리소스와 보안을 동시에 확보):

### Presigned URL 업로드 흐름
클라이언트 → 서버(URL 요청) → S3/R2(Presigned URL 발급) → 클라이언트(직접 업로드) → 서버(후처리 트리거)

DO:
```typescript
// 1단계: Presigned URL 발급
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { randomUUID } from "crypto";

const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp", "application/pdf"] as const;
const MAX_SIZE: Record<string, number> = {
  "image/jpeg": 5 * 1024 * 1024,   // 5MB
  "image/png": 5 * 1024 * 1024,     // 5MB
  "image/webp": 5 * 1024 * 1024,    // 5MB
  "application/pdf": 20 * 1024 * 1024, // 20MB
};

app.post("/api/v1/uploads/presigned", authMiddleware, async (c) => {
  const { contentType, fileName } = UploadRequestSchema.parse(await c.req.json());

  if (!ALLOWED_TYPES.includes(contentType)) {
    throw Errors.badRequest("허용되지 않는 파일 형식입니다");
  }

  const key = `uploads/${c.get("userId")}/${randomUUID()}.${getExtension(contentType)}`;
  const command = new PutObjectCommand({
    Bucket: env.S3_BUCKET,
    Key: key,
    ContentType: contentType,
    ContentLength: MAX_SIZE[contentType], // 최대 크기 제한
  });

  const url = await getSignedUrl(s3Client, command, { expiresIn: 300 }); // 5분
  return c.json({ data: { uploadUrl: url, key, expiresIn: 300 } });
});

// 2단계: 업로드 완료 후 검증 & 비동기 처리
app.post("/api/v1/uploads/complete", authMiddleware, async (c) => {
  const { key } = CompleteUploadSchema.parse(await c.req.json());

  // S3에서 파일 메타데이터 확인
  const head = await s3Client.send(new HeadObjectCommand({
    Bucket: env.S3_BUCKET, Key: key,
  }));

  // magic bytes 기반 실제 파일 타입 검증
  const stream = await s3Client.send(new GetObjectCommand({
    Bucket: env.S3_BUCKET, Key: key, Range: "bytes=0-11",
  }));
  const magicBytes = Buffer.from(await stream.Body!.transformToByteArray());
  const detectedType = detectFileType(magicBytes);

  if (!ALLOWED_TYPES.includes(detectedType)) {
    await s3Client.send(new DeleteObjectCommand({ Bucket: env.S3_BUCKET, Key: key }));
    throw Errors.badRequest("파일 내용이 허용된 형식과 일치하지 않습니다");
  }

  // 비동기 이미지 처리 큐에 등록
  await uploadQueue.add("process-upload", { key, userId: c.get("userId") });
  return c.json({ data: { status: "processing", key } });
});
```

### Magic Bytes 검증
```typescript
// 파일 확장자가 아닌 실제 바이너리 시그니처로 검증
function detectFileType(buffer: Buffer): string {
  const hex = buffer.toString("hex").slice(0, 16);
  if (hex.startsWith("ffd8ff")) return "image/jpeg";
  if (hex.startsWith("89504e47")) return "image/png";
  if (hex.startsWith("52494646") && hex.slice(16).startsWith("57454250")) return "image/webp";
  if (hex.startsWith("25504446")) return "application/pdf";
  return "unknown";
}
```

### 이미지 리사이즈 파이프라인
```typescript
// Worker: 업로드 후 비동기 리사이징
import sharp from "sharp";

const SIZES = { thumbnail: 150, medium: 600, large: 1200 };

async function processImage(key: string): Promise<void> {
  const original = await downloadFromS3(key);

  for (const [name, width] of Object.entries(SIZES)) {
    const resized = await sharp(original)
      .resize(width, null, { withoutEnlargement: true })
      .webp({ quality: 80 })
      .toBuffer();

    await uploadToS3(`${key.replace(/\.[^.]+$/, '')}_${name}.webp`, resized);
  }
}
```

DON'T:
```typescript
// ❌ 서버 메모리로 직접 업로드 -- 대용량 파일 시 OOM
app.post("/uploads", async (c) => {
  const file = await c.req.file("upload"); // 서버 메모리에 전체 로드
  await s3.upload({ Body: file.stream() });
});

// ❌ 확장자만 신뢰 -- .jpg로 위장한 실행파일 가능
if (fileName.endsWith(".jpg")) { /* OK */ }

// ❌ 크기 제한 없음 -- 10GB 파일 업로드 가능
const command = new PutObjectCommand({ Bucket, Key, ContentType });
```

### 파일 크기 제한 기준
| 파일 유형 | 최대 크기 | 비고 |
|-----------|-----------|------|
| 이미지 (JPEG/PNG/WebP) | 5MB | 리사이즈 파이프라인 적용 |
| 문서 (PDF) | 20MB | 바이러스 스캔 권장 |
| 동영상 | 100MB | Multipart Upload 필수 |
| 프로필 아바타 | 2MB | 정사각형 크롭 강제 |

### 흔한 실수
- Presigned URL 만료 시간을 너무 길게 설정 (5분 이내 권장, 최대 15분)
- Content-Length 조건 미설정으로 Presigned URL을 이용한 대용량 업로드 허용
- 원본 파일명을 그대로 저장 -> path traversal 공격 가능 (UUID로 재명명 필수)
- multipart upload 시 파트 완료 확인 없이 complete 호출
- 업로드 실패 시 S3에 고아 객체(orphan) 방치 -> lifecycle 정책으로 자동 삭제 설정

## Connections

- [[dev.backend.api.security]] — CO_CREATES (weight: 0.6)
