"""훅 공통 유틸리티."""

from __future__ import annotations

import os


def load_env(project_root: str) -> None:
    """프로젝트 루트의 .env 파일을 파싱하여 환경변수 설정.

    지원: 따옴표, export 접두사, 주석, 빈 줄.
    """
    env_path = os.path.join(project_root, ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[7:]
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            # 따옴표 제거
            if len(value) >= 2 and (
                (value[0] == '"' and value[-1] == '"')
                or (value[0] == "'" and value[-1] == "'")
            ):
                value = value[1:-1]
            os.environ.setdefault(key, value)
