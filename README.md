# Uptime Beacon

A small, dependency-free HTTP(S) uptime checker for terminals, scheduled jobs, and CI pipelines. It verifies endpoint availability, measures latency, flags slow responses, and can emit structured JSON without sending monitoring data to a third party.

## English

### Why it exists
Simple availability checks should not require an account, hosted dashboard, or large dependency tree. Uptime Beacon provides a predictable local check that is easy to automate and inspect.

### Features
- Checks one or many HTTP/HTTPS endpoints.
- HEAD by default, with GET available for servers that require it.
- Treats HTTP 2xx/3xx as available and 4xx/5xx/network failures as down.
- Measures request latency and marks configurable slow responses.
- Reads targets from arguments or a UTF-8 file; comments and duplicates are handled.
- Human-readable and JSON output.
- Automation-friendly exit codes: `0` healthy, `1` endpoint failure (or slow with `--fail-on-slow`), `2` invalid invocation/configuration.
- Rejects non-HTTP(S) URLs and URLs containing embedded credentials.
- Python API, CLI, and `python -m uptime_beacon` entry points.
- No runtime dependencies, account, telemetry, or API key.

### Preview
```text
UP      84.21 ms  HTTP 200      https://example.com/
DOWN   203.10 ms  HTTP 503      https://status.example.test/
```
Actual latency and status depend on the target and network. For screenshots, run the CLI against endpoints you are authorized to monitor and capture the terminal output; no screenshot is bundled because results are environment-dependent.

### Requirements & installation
Python 3.10 or newer.

```bash
git clone https://github.com/rad03i2/uptime-beacon.git
cd uptime-beacon
python -m pip install -e .
```

### Usage
```bash
uptime-beacon https://example.com https://www.iana.org
uptime-beacon --file examples/targets.txt
uptime-beacon https://example.com --timeout 5 --slow-ms 750 --fail-on-slow
uptime-beacon https://example.com --method GET --json
python -m uptime_beacon https://example.com
```

Target files contain one URL per line. Blank lines and lines beginning with `#` are ignored.

Python API:
```python
from uptime_beacon import check_url

result = check_url("https://example.com", timeout=5, slow_ms=800)
print(result.ok, result.status, result.latency_ms)
```

### Configuration
There is deliberately no hidden config file or environment-variable requirement. Configure each run explicitly with `--timeout`, `--slow-ms`, `--method`, and `--fail-on-slow`. This keeps scheduled checks reproducible.

### Project structure
```text
src/uptime_beacon/   core checker, CLI, public API
tests/               deterministic unit/CLI tests
examples/targets.txt sample target-list format
.github/workflows/   cross-platform CI
```

### Testing
```bash
python -m pip install -e . pytest
python -m compileall -q src tests
python -m pytest -q
uptime-beacon --version
```
CI runs these checks on Ubuntu, Windows, and macOS with supported Python versions. Network behavior is mocked in tests so the suite does not depend on public services.

### Security & privacy
Checks run locally. Uptime Beacon does not store response bodies, cookies, credentials, or telemetry. Only monitor systems you are authorized to access. A wrapper that accepts arbitrary untrusted URLs would need additional SSRF protections before internet exposure; see `SECURITY.md`.

### Limitations
This is a polling primitive, not a hosted monitoring platform: it does not schedule itself, retain history, send alerts, render dashboards, perform browser transactions, or test DNS/TCP separately. Redirects follow Python's standard urllib behavior. A successful HTTP response does not prove application-level correctness.

### Optional roadmap
Optional future additions may include bounded retries, history persistence, and opt-in notification adapters while keeping the core lightweight.

### Contributing & license
See `CONTRIBUTING.md`. Licensed under the MIT License; see `LICENSE`.

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
**Uptime Beacon** أداة محلية خفيفة لفحص توفر عناوين HTTP/HTTPS من الطرفية أو المهام المجدولة أو CI. تتحقق من الاستجابة، وتقيس زمنها، وتحدد الاستجابات البطيئة، ويمكنها إخراج JSON منظم من دون إرسال بيانات المراقبة إلى خدمة خارجية.

### لماذا المشروع؟
الفحص البسيط لتوفر المواقع لا يحتاج بالضرورة إلى حساب سحابي أو لوحة مستضافة أو اعتماديات كثيرة. يوفر المشروع فحصًا واضحًا وقابلًا للأتمتة ويمكن مراجعة سلوكه محليًا.

### المزايا
- فحص عنوان واحد أو عدة عناوين HTTP/HTTPS.
- استخدام HEAD افتراضيًا مع دعم GET.
- اعتبار 2xx و3xx متاحة، و4xx و5xx وأخطاء الشبكة غير متاحة.
- قياس زمن الاستجابة وحد قابل للتخصيص لتصنيف الاستجابة البطيئة.
- قراءة الأهداف من سطر الأوامر أو ملف UTF-8 مع تجاهل التعليقات والتكرار.
- إخراج نصي أو JSON.
- رموز خروج مناسبة للأتمتة: `0` سليم، `1` فشل هدف، و`2` إدخال أو إعداد غير صالح.
- رفض البروتوكولات غير HTTP(S) ورفض بيانات الاعتماد المضمنة في الرابط.
- Python API وCLI وتشغيل عبر `python -m uptime_beacon`.
- بلا اعتماديات تشغيل خارجية أو حساب أو Telemetry أو API key.

### المعاينة
يعرض الوضع النصي حالة `UP` أو `SLOW` أو `DOWN` مع زمن الاستجابة ورمز HTTP والرابط. القيم الفعلية تعتمد على الشبكة والهدف، لذلك لا توجد لقطة ثابتة تدّعي نتائج حقيقية.

### المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث:
```bash
git clone https://github.com/rad03i2/uptime-beacon.git
cd uptime-beacon
python -m pip install -e .
```

### الاستخدام
```bash
uptime-beacon https://example.com
uptime-beacon --file examples/targets.txt --json
uptime-beacon https://example.com --timeout 5 --slow-ms 750 --fail-on-slow
uptime-beacon https://example.com --method GET
```

ومن Python:
```python
from uptime_beacon import check_url
result = check_url("https://example.com", timeout=5)
print(result.ok, result.latency_ms)
```

### الإعداد
لا يحتاج المشروع إلى `.env` أو ملف إعداد مخفي. تمرر الخيارات صراحةً عبر `--timeout` و`--slow-ms` و`--method` و`--fail-on-slow` لتبقى المهام قابلة لإعادة الإنتاج.

### بنية المشروع
`src/uptime_beacon` للمحرك والواجهة البرمجية، و`tests` للاختبارات، و`examples` لأمثلة الإدخال، و`.github/workflows` للتكامل المستمر.

### الاختبارات
```bash
python -m pip install -e . pytest
python -m compileall -q src tests
python -m pytest -q
```
الاختبارات تحاكي الشبكة ولا تعتمد على توفر مواقع عامة، بينما يعمل CI على Linux وWindows وmacOS.

### الأمان والخصوصية
الأداة تعمل محليًا ولا تحفظ أجسام الاستجابات أو Cookies أو بيانات الاعتماد أو Telemetry. استخدمها فقط مع الأنظمة المسموح لك بمراقبتها. إذا بُنيت خدمة عامة فوقها تقبل روابط من مستخدمين غير موثوقين فيجب إضافة حماية SSRF؛ راجع `SECURITY.md`.

### القيود
المشروع أداة فحص وليس منصة مراقبة مستضافة: لا يجدول نفسه، ولا يحتفظ بسجل زمني، ولا يرسل تنبيهات، ولا يوفر Dashboard، ولا ينفذ معاملات متصفح. نجاح HTTP وحده لا يضمن صحة منطق التطبيق.

### تطوير اختياري
يمكن مستقبلًا إضافة retries محدودة، وسجل محلي، وموصلات تنبيه اختيارية مع الحفاظ على بساطة المحرك.

### المساهمة والترخيص
راجع `CONTRIBUTING.md`. المشروع مرخص برخصة MIT الموجودة في `LICENSE`.

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
