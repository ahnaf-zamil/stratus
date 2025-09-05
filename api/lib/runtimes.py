"""
Loads and transforms runtime configuration from a YAML file.
Used to provide available deployment runtimes to the frontend/API.
"""

import yaml

# Internal cache to avoid repeated file reads
_runtime_cache = None


def _load_yaml_once(filepath="shared/config/runtimes.yaml"):
    global _runtime_cache
    if _runtime_cache is None:
        try:
            with open(filepath, "r") as f:
                raw = yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load runtime config: {e}")

        _runtime_cache = _transform(raw)
    return _runtime_cache


def _transform(data):
    result = []
    for language, versions in data.get("runtimes", {}).items():
        for version_id, details in versions.items():
            result.append(
                {
                    "id": version_id,
                    "version": details["version"],
                    "language": language,
                }
            )
    return result


def get_runtime_config():
    """Returns the cached and transformed runtime config as a list of dicts."""
    return _load_yaml_once()


def get_runtime_by_id(rid: str):
    conf = get_runtime_config()

    for i in conf:
        if i["id"] == rid:
            return i
