"""Rebuild a single-file offline-readable HTML from structured answers.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
payload = json.loads((ROOT / 'answers.json').read_text(encoding='utf-8'))
assert len(payload['chapters']) == 42
questions = [q for ch in payload['chapters'] for q in ch['questions']]
assert len(questions) == 198
assert [q['id'] for q in questions] == list(range(1,199))
assert all(q['answer'].strip() for q in questions)
inline = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))
inline = inline.replace('<', '\\u003c').replace('>', '\\u003e').replace('&','\\u0026')
template = (ROOT / 'template.html').read_text(encoding='utf-8')
assert template.count('__QUESTIONS_JSON_PLACEHOLDER__') == 1
result=template.replace('__QUESTIONS_JSON_PLACEHOLDER__', inline)
(ROOT / 'index.html').write_text(result, encoding='utf-8')
print(f'Built {ROOT / "index.html"}: {len(payload["chapters"])} chapters, {len(questions)} questions, {len(result):,} chars')
