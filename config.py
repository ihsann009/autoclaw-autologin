"""AutoClaw Proxy — Constants & Config"""

import os

# ── App Signing ──
APP_ID = "100003"
APP_KEY = "38d2391985e2369a5fb8227d8e6cd5e5"
PRODUCT = "autoclaw"
VERSION = "4.6.2"
PLATFORM = "win"

# ── Endpoints ──
USER_API_BASE = "https://autoglm-api.zhipuai.cn"
LLM_PROXY_BASE = "https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw"
CHAT_COMPLETIONS = f"{LLM_PROXY_BASE}/chat/completions"

# ── Auth Endpoints ──
GOOGLE_OAUTH_URL = f"{USER_API_BASE}/userapi/overseasv1/zai-oauth-url"
GOOGLE_OAUTH_LOGIN = f"{USER_API_BASE}/userapi/overseasv1/zai-oauth-login"
REFRESH_URL = f"{USER_API_BASE}/userapi/v1/refresh"
PROFILE_URL = f"{USER_API_BASE}/userapi/v1/user-profile"
WALLET_URL = f"{USER_API_BASE}/agent-assetmgr/api/v2/wallets?biz_app_id=autoclaw"
LEDGER_URL = f"{USER_API_BASE}/agent-assetmgr/api/v1/ledgers_std?asset_type=point&wallet_type=all"

# ── Token Storage ──
TOKENS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tokens.json")

# ── Proxy Server ──
PROXY_HOST = "0.0.0.0"
PROXY_PORT = 31000

# ── Model Map (X-Request-Model → alias) ──
# Key = what client sends as "model" in OpenAI body
# Value = X-Request-Model header value sent to AutoClaw upstream
MODEL_MAP = {
    # Best — real GLM-5.2 (may be unavailable)
    "glm-5.2": "openrouter_glm-5.2",
    "glm-5.2-true": "openrouter_glm-5.2",
    # Cheapest — glm-5-turbo (always available)
    "glm-5-turbo": "zai_glm-5-turbo",
    "cheap": "zai_glm-5-turbo",
    # Avoid — secretly DeepSeek-V4-Pro ~7x cost
    "auto": "zai_auto",
    "deepseek": "zai_auto",
}

DEFAULT_MODEL = "openrouter_glm-5.2"

# ── Access Token TTL (24h, refresh 5min before expiry) ──
ACCESS_TOKEN_TTL = 86400  # 24h
REFRESH_MARGIN = 300      # 5min before expiry

# ── Rotating Proxy for Registration ──
# Load proxies from proxies.txt (format: host:port:user:pass per line)
# Used by auth.py to bypass 630014 rate limit. Each account gets next proxy round-robin.
import os as _os
_PROXY_FILE = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "proxies.txt")
PROXY_LIST = []
if _os.path.exists(_PROXY_FILE):
    with open(_PROXY_FILE) as _f:
        for _line in _f:
            _line = _line.strip()
            if not _line or _line.startswith("#") or ":" not in _line:
                continue
            _parts = _line.split(":")
            if len(_parts) == 4:
                _host, _port, _user, _pwd = _parts
                PROXY_LIST.append({
                    "server": f"http://{_host}:{_port}",
                    "username": _user,
                    "password": _pwd,
                })

# ── Billing Header Quirks ──
# LLM proxy: X-Authorization (capital X)
# Assetmgr: authorization (lowercase)
