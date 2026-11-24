#!/usr/bin/env python3
"""Build 2026 Korean Real Estate, Mortgage Loan, Jeonse/Wolse, Brokerage Fee, Acquisition Tax & Subscription Point Calculator (house-calc-kr)."""
from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

BASE_URL = "https://0520goeus.github.io/house-calc-kr"
INDEXNOW_KEY = "c4e819a2f7b043d691e5a8c320f4b712"
ADSENSE_CLIENT = "ca-pub-8749404731911210"
GSC_FILE = "google873809343766a3b6.html"
GSC_CONTENT = "google-site-verification: google873809343766a3b6.html"
TODAY = datetime.now().strftime("%Y-%m-%d")

DIST = Path(__file__).resolve().parent / "dist"

ECOSYSTEM_LINKS = [
    ("부동산·대출·복비 계산기", "https://0520goeus.github.io/house-calc-kr/"),
    ("자동차세·유지비·취등록세", "https://0520goeus.github.io/car-calc-kr/"),
    ("실수령액·금융 계산기", "https://0520goeus.github.io/money-calc-kr/"),
    ("2026 지원금·근로장려금", "https://0520goeus.github.io/benefit-calc-kr/"),
    ("평수별 가전·직구관세", "https://0520goeus.github.io/life-fee-calc/"),
    ("전기세 얼마 계산기", "https://0520goeus.github.io/elec-calc/"),
    ("가성비 VS 비교(124종)", "https://0520goeus.github.io/vs-pick/"),
    ("해뎐 가격노트(588품목)", "https://0520goeus.github.io/price-note/"),
    ("셀러 마진·엑셀 템플릿", "https://0520goeus.github.io/seller-margin-calc/"),
    ("실시간 트렌드 브리핑", "https://0520goeus.github.io/kr-trend-brief/"),
    ("생활비 물가 연구소", "https://0520goeus.github.io/life-money-lab/"),
]

COUPANG_HTML = """<div style="margin:24px 0;padding:14px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;text-align:center;">
<div style="font-size:12px;color:#64748b;margin-bottom:8px;">이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</div>
<script src="https://ads-partners.coupang.com/g.js"></script>
<script>new PartnersCoupang.G({"id":1049499,"template":"carousel","trackingCode":"AF9170267","width":"100%","height":"140","tsource":""});</script>
</div>"""

CSS = """
:root{--bg:#f8fafc;--card:#fff;--ink:#0f172a;--muted:#475569;--brand:#1d4ed8;--brand2:#0f766e;--line:#e2e8f0;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;background:var(--bg);color:var(--ink);line-height:1.7}
header{background:linear-gradient(135deg,#0f172a,#1e3a8a);color:#fff;padding:28px 18px}
.wrap{max-width:980px;margin:0 auto;padding:0 16px}
header h1{margin:0 0 8px;font-size:26px}
header p{margin:0;opacity:.9;font-size:15px}
nav.top{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
nav.top a{color:#fff;text-decoration:none;background:rgba(255,255,255,.14);padding:6px 12px;border-radius:999px;font-size:13px}
nav.top a:hover{background:rgba(255,255,255,.28)}
main{padding:22px 0 44px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin-bottom:18px;box-shadow:0 2px 10px rgba(15,23,42,.04)}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}
label{display:block;font-size:13px;font-weight:700;color:var(--muted);margin-bottom:8px}
input,select{width:100%;padding:10px 12px;border:1px solid #cbd5e1;border-radius:10px;font-size:15px;margin-top:4px}
button.btn{background:var(--brand);color:#fff;border:none;border-radius:10px;padding:11px 16px;font-size:15px;font-weight:700;cursor:pointer;width:100%}
button.btn:hover{filter:brightness(1.06)}
.res{background:#eff6ff;border-left:4px solid var(--brand);padding:14px 16px;border-radius:10px;margin-top:14px;font-size:15px}
.res strong{color:#1e3a8a;font-size:18px}
table{width:100%;border-collapse:collapse;margin:14px 0;font-size:14px}
th,td{padding:10px 10px;border:1px solid var(--line);text-align:left}
th{background:#f1f5f9;font-weight:700}
.pill{display:inline-block;background:#dbeafe;color:#1e40af;padding:2px 9px;border-radius:999px;font-size:12px;font-weight:700}
.linklist{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}
.linklist a{display:block;padding:10px 12px;border:1px solid var(--line);border-radius:10px;text-decoration:none;color:var(--ink);font-size:14px;background:#fff}
.linklist a:hover{border-color:var(--brand);background:#eff6ff}
.cta{background:linear-gradient(135deg,#0f766e,#0d9488);color:#fff;border-radius:14px;padding:18px 20px;margin:20px 0}
.cta a{display:inline-block;margin-top:10px;background:#fff;color:#0f766e;padding:9px 15px;border-radius:10px;text-decoration:none;font-weight:800;font-size:14px}
footer{background:#0f172a;color:#cbd5e1;padding:28px 16px;font-size:13px}
footer a{color:#93c5fd;text-decoration:none}
.eco{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 16px}
.eco a{background:#1e293b;padding:5px 10px;border-radius:8px;font-size:12px;color:#e2e8f0}
"""


def _monthly_pmt(principal_won: int, annual_rate_pct: float, years: int) -> int:
    r = (annual_rate_pct / 100.0) / 12.0
    n = years * 12
    if r == 0:
        return round(principal_won / n)
    return round(principal_won * (r * (1 + r) ** n) / ((1 + r) ** n - 1))


def _brokerage_fee(price_man: int, is_sale: bool = True) -> tuple[float, int]:
    """2026 Korean legal max brokerage rate & fee (man-won, excluding VAT)."""
    if is_sale:
        if price_man < 5000:
            return 0.6, min(round(price_man * 0.006), 25)
        if price_man < 20000:
            return 0.5, min(round(price_man * 0.005), 80)
        if price_man < 90000:
            return 0.4, round(price_man * 0.004)
        if price_man < 120000:
            return 0.5, round(price_man * 0.005)
        if price_man < 150000:
            return 0.6, round(price_man * 0.006)
        return 0.7, round(price_man * 0.007)
    else:
        if price_man < 5000:
            return 0.5, min(round(price_man * 0.005), 20)
        if price_man < 10000:
            return 0.4, min(round(price_man * 0.004), 30)
        if price_man < 60000:
            return 0.3, round(price_man * 0.003)
        if price_man < 120000:
            return 0.4, round(price_man * 0.004)
        if price_man < 150000:
            return 0.5, round(price_man * 0.005)
        return 0.6, round(price_man * 0.006)


def _acq_tax_1house(price_man: int) -> tuple[float, int]:
    """1-house residential acquisition tax (excluding local edu/rural tax)."""
    if price_man <= 60000:
        rate = 1.0
    elif price_man <= 90000:
        rate = round((price_man / 10000.0 * (2 / 3) - 3), 2)
    else:
        rate = 3.0
    # Add local education tax (approx 10% of acq tax -> total 1.1% ~ 3.3%)
    total_rate = round(rate * 1.1, 2)
    return total_rate, round(price_man * (total_rate / 100.0))


def _render_page(title: str, desc: str, canonical_path: str, body: str, faq: list[tuple[str, str]]) -> str:
    canonical = f"{BASE_URL}/{canonical_path.lstrip('/')}" if canonical_path else f"{BASE_URL}/"
    ld_blocks = [
        {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": title,
            "url": canonical,
            "applicationCategory": "FinanceApplication",
            "operatingSystem": "All",
            "inLanguage": "ko",
            "description": desc,
        }
    ]
    if faq:
        ld_blocks.append(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in faq
                ],
            }
        )
    ld_html = "".join(
        f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in ld_blocks
    )
    eco_html = "".join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(n)}</a>' for n, u in ECOSYSTEM_LINKS)
    faq_html = ""
    if faq:
        faq_items = "".join(f"<p><strong>Q. {html.escape(q)}</strong><br>A. {html.escape(a)}</p>" for q, a in faq)
        faq_html = f'<section class="card"><h2>자주 묻는 질문 (FAQ)</h2>{faq_items}</section>'

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta name="google-site-verification" content="E0MKLI_9g0wTNR9pjNKmxb_QGiA51AIK93dV9qBKumg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
{ld_html}
<style>{CSS}</style>
</head>
<body>
<header>
  <div class="wrap">
    <h1><a href="{BASE_URL}/" style="color:#fff;text-decoration:none">2026 부동산·대출·전월세·복비 계산기</a></h1>
    <p>주담대 원리금균등·전월세 전환·중개보수(복비)·취득세·청약 가점 84점 즉시 무료 계산 ({TODAY} 기준)</p>
    <nav class="top">
      <a href="{BASE_URL}/#loan">대출 이자 계산기</a>
      <a href="{BASE_URL}/#jeonse">전세 vs 월세 계산기</a>
      <a href="{BASE_URL}/#fee">복비·취득세 계산기</a>
      <a href="{BASE_URL}/#point">청약 가점 84점</a>
      <a href="{BASE_URL}/#directory">금액별 표 50종</a>
    </nav>
  </div>
</header>
<main class="wrap">
{body}
{faq_html}
<section class="cta">
  <div style="font-size:18px;font-weight:800">내집마련 매물 10개 동시 비교 자동 엑셀 템플릿 (무매크로)</div>
  <div style="font-size:14px;opacity:.92;margin-top:4px">매매가·대출금리·취득세·복비·총 필요 현금을 한 시트에서 자동 비교하고 실수 없는 계약 결정을 도와줍니다.</div>
  <a href="https://scopekit-studio.lemonsqueezy.com/checkout/buy/ba4f11c6-8609-49c0-a947-39bead163d74" target="_blank" rel="noopener">엑셀 3종 올인원 번들 즉시 다운로드 ($19) →</a>
</section>
{COUPANG_HTML}
</main>
<footer>
  <div class="wrap">
    <strong>해뎐 무료 생활금융·절약 계산기 네트워크 (11개 사이트)</strong>
    <div class="eco">{eco_html}</div>
    <div>본 사이트의 세율·중개보수 요율은 2026년 공개 법정 기준을 반영한 참고용 모의계산이며, 실제 계약·대출 실행 전 관할 지자체 및 금융기관 확인을 권장합니다. · Updated {TODAY}</div>
  </div>
</footer>
</body>
</html>"""


def main() -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "p").mkdir(exist_ok=True)
    urls: list[str] = [f"{BASE_URL}/"]
    loan_links: list[tuple[str, str]] = []
    sale_links: list[tuple[str, str]] = []
    jeonse_links: list[tuple[str, str]] = []
    guide_links: list[tuple[str, str]] = []

    # 1. Programmatic Loan Pages (12)
    for eok in [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 8, 10]:
        slug = f"loan-{str(eok).replace('.', '_')}-eok"
        label = f"{int(eok*10000):,}만원" if eok < 1 else (f"{int(eok)}억" if eok == int(eok) else f"{eok}억")
        principal = int(eok * 100_000_000)
        rows = []
        for rate in (3.5, 4.0, 4.5, 5.0, 5.5):
            m30 = _monthly_pmt(principal, rate, 30)
            m20 = _monthly_pmt(principal, rate, 20)
            tot30 = m30 * 360 - principal
            rows.append(
                f"<tr><td>연 {rate:.1f}%</td><td><strong>월 {m30:,}원</strong></td><td>월 {m20:,}원</td><td>약 {round(tot30/10000):,}만원</td></tr>"
            )
        title = f"대출 {label} 이자 계산표 — 2026 금리별(3.5%~5.5%) 30년 원리금균등 월 상환액"
        desc = f"주택담보대출·신용대출 {label}을 연 3.5%~5.5% 금리로 20년·30년 원리금균등 상환할 때 매달 내는 원리금과 총 이자 비교표입니다."
        body = f"""
<section class="card">
  <span class="pill">대출 이자 실측표</span>
  <h2>{html.escape(title)}</h2>
  <p>대출 원금 <strong>{label}({principal:,}원)</strong>을 원리금균등분할상환 방식으로 갚을 때 금리 0.5%p 차이에 따라 매달 나가는 금액과 30년 총 이자가 얼마나 달라지는지 한눈에 비교해 보세요.</p>
  <table>
    <thead><tr><th>적용 금리</th><th>30년 만기 월 상환액</th><th>20년 만기 월 상환액</th><th>30년 총 이자</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
  <p>👉 <a href="{BASE_URL}/#loan"><strong>원하는 금리·만기 직접 입력해 계산하기 →</strong></a></p>
</section>"""
        faq = [
            (f"대출 {label} 금리가 4.0%일 때 30년 월 상환액은 얼마인가요?", f"원리금균등 기준 월 {_monthly_pmt(principal, 4.0, 30):,}원이며, 20년 만기로 줄이면 월 {_monthly_pmt(principal, 4.0, 20):,}원입니다."),
            ("원리금균등과 원금균등 중 어느 쪽이 총 이자가 적은가요?", "원금균등은 초기 납입액이 다소 높지만 매달 원금이 빠르게 줄어 30년 기준 총 이자가 원리금균등보다 약 10~15% 적습니다."),
        ]
        (DIST / "p" / f"{slug}.html").write_text(_render_page(title, desc, f"p/{slug}.html", body, faq), encoding="utf-8")
        urls.append(f"{BASE_URL}/p/{slug}.html")
        loan_links.append((f"대출 {label} 월 상환액표", f"p/{slug}.html"))

    # 2. Programmatic Sale Acquisition Tax + Brokerage Fee Pages (12)
    for eok in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20]:
        price_man = eok * 10000
        b_rate, b_fee = _brokerage_fee(price_man, True)
        b_vat = round(b_fee * 1.1)
        t_rate, t_fee = _acq_tax_1house(price_man)
        first_home = max(0, t_fee - 200) if price_man <= 120000 else t_fee
        slug = f"buy-{eok}-eok-tax-fee"
        title = f"{eok}억 아파트 매매 취득세·복비(중개수수료) 총정리 (2026)"
        desc = f"{eok}억 주택 매매 시 1주택 취득세({t_rate}% · 약 {t_fee:,}만원), 생애최초 감면, 부동산 복비 상한({b_rate}% · {b_fee:,}만원)과 총 부대비용을 정리했습니다."
        body = f"""
<section class="card">
  <span class="pill">매매 부대비용 총정리</span>
  <h2>{html.escape(title)}</h2>
  <table>
    <thead><tr><th>비용 항목</th><th>적용 요율(2026 기준)</th><th>예상 금액</th><th>비고</th></tr></thead>
    <tbody>
      <tr><td>1주택 취득세(지방교육세 포함)</td><td>{t_rate}%</td><td><strong>약 {t_fee:,}만원</strong></td><td>전용 85㎡ 이하 기준</td></tr>
      <tr><td>생애최초 주택 감면 적용 시</td><td>최대 200만원 감면</td><td><strong>약 {first_home:,}만원</strong></td><td>12억 이하 주택 대상</td></tr>
      <tr><td>부동산 중개보수(복비 상한)</td><td>최대 {b_rate}%</td><td><strong>최대 {b_fee:,}만원</strong></td><td>부가세 10% 포함 약 {b_vat:,}만원</td></tr>
      <tr><td>취득세 + 복비 합계(1주택)</td><td>-</td><td><strong>약 {t_fee + b_vat:,}만원</strong></td><td>등기 법무사비 별도</td></tr>
    </tbody>
  </table>
  <p>👉 <a href="{BASE_URL}/#fee"><strong>직접 매매가 입력해 복비·취득세 계산하기 →</strong></a></p>
</section>"""
        faq = [
            (f"{eok}억 아파트 매매 복비 상한액은 얼마인가요?", f"2026년 법정 상한요율 {b_rate}% 기준 최대 {b_fee:,}만원(부가세 10% 별도, 포함 시 {b_vat:,}만원)이며 상한 내에서 협의할 수 있습니다."),
            ("생애최초 취득세 200만원 감면 조건은 무엇인가요?", "실거래가 12억원 이하 주택을 생애 최초로 취득하는 경우 소득 기준과 무관하게 최대 200만원까지 취득세가 감면됩니다."),
        ]
        (DIST / "p" / f"{slug}.html").write_text(_render_page(title, desc, f"p/{slug}.html", body, faq), encoding="utf-8")
        urls.append(f"{BASE_URL}/p/{slug}.html")
        sale_links.append((f"{eok}억 매매 취득세·복비", f"p/{slug}.html"))

    # 3. Programmatic Jeonse -> Wolse Conversion & Jeonse Brokerage Pages (10)
    for eok in [1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 8]:
        dep_man = int(eok * 10000)
        label = f"{int(eok)}억" if eok == int(eok) else f"{eok}억"
        b_rate, b_fee = _brokerage_fee(dep_man, False)
        rows = []
        for conv in (4.0, 4.5, 5.0, 5.5, 6.0):
            # Convert half of deposit to monthly rent
            diff = dep_man // 2
            wolse_half = round(diff * (conv / 100.0) / 12.0, 1)
            wolse_full = round(dep_man * (conv / 100.0) / 12.0, 1)
            rows.append(f"<tr><td>연 {conv:.1f}%</td><td>보증금 {diff:,}만 + <strong>월 {wolse_half}만원</strong></td><td>보증금 0원 환산 월 {wolse_full}만원</td></tr>")
        slug = f"jeonse-{str(eok).replace('.', '_')}-eok"
        title = f"전세 {label} 반전세·월세 전환 적정 월세 & 복비 계산표 (2026)"
        desc = f"전세 {label}을 반전세·월세로 전환할 때 전환율(4%~6%)별 적정 월세와 전세 중개수수료 상한({b_rate}% · {b_fee:,}만원) 비교표입니다."
        body = f"""
<section class="card">
  <span class="pill">전월세 전환·복비</span>
  <h2>{html.escape(title)}</h2>
  <p>전세 보증금 <strong>{label}({dep_man:,}만원)</strong>의 법정 임대차 복비 상한은 <strong>{b_rate}% (최대 {b_fee:,}만원, 부가세 별도)</strong>입니다. 아래 표에서 전환율별 적정 반전세·월세를 확인하세요.</p>
  <table>
    <thead><tr><th>전월세 전환율</th><th>보증금 절반({dep_man//2:,}만원) 전환 시</th><th>전액 월세 환산 시</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
  <p>👉 <a href="{BASE_URL}/#jeonse"><strong>내 보증금·전세대출 금리로 전세 vs 월세 유불리 계산하기 →</strong></a></p>
</section>"""
        faq = [
            (f"전세 {label} 복비 상한은 얼마인가요?", f"2026년 주택 임대차 법정 상한요율 {b_rate}% 기준 최대 {b_fee:,}만원(부가세 10% 별도)입니다."),
            ("전세와 월세 중 무엇이 유리한가요?", "전세대출 금리보다 집주인이 요구하는 전월세 전환율이 높으면 전세대출이 유리하고, 전환율이 더 낮으면 반전세·월세가 유리합니다."),
        ]
        (DIST / "p" / f"{slug}.html").write_text(_render_page(title, desc, f"p/{slug}.html", body, faq), encoding="utf-8")
        urls.append(f"{BASE_URL}/p/{slug}.html")
        jeonse_links.append((f"전세 {label} 월세전환·복비", f"p/{slug}.html"))

    # 4. High-CPC Deep Guides (6)
    guides = [
        ("newborn-loan-2026", "2026 신생아 특례대출 자격·금리(1.6%~3.3%)·한도 5억 총정리",
         "출산 가구 대상 연 1.6%~3.3% 초저금리 구입자금 최대 5억원·전세자금 최대 3억원 지원 조건과 월 납입금 비교표.",
         "신생아 특례대출은 대출 신청일 기준 2년 내 출산·입양한 무주택 세대주에게 시중 금리 대비 연 1~2%p 이상 낮은 금리를 제공합니다. 3억원 대출 시 연 2.5% 기준 30년 원리금균등 월 납입금은 약 118만 5천원으로, 연 4.5% 일반 주담대(약 152만원) 대비 매달 33만원 이상 이자를 아낄 수 있습니다."),
        ("didimdol-loan-2026", "2026 디딤돌대출·버팀목 전세대출 소득·자산 조건 및 금리표",
         "무주택 서민 실수요자용 디딤돌 구입자금과 청년·신혼부부 버팀목 전세대출 핵심 조건 정리.",
         "디딤돌대출은 부부합산 연소득 6,000만원 이하(생애최초 7,000만원, 신혼 8,500만원) 및 순자산 기준 충족 시 이용 가능하며, 전용 85㎡ 이하 주택에 대해 저금리 장기 상환 혜택을 제공합니다."),
        ("stress-dsr-2026", "스트레스 DSR 40% 대출 한도 계산법 — 연봉 5천~1억 최대 주담대 얼마?",
         "연봉별 DSR 40% 적용 시 30년 만기 주택담보대출 최대 가능 한도와 한도 늘리는 실전 체크리스트.",
         "DSR(총부채원리금상환비율)은 모든 금융권 대출의 연간 원리금 상환액을 연소득으로 나눈 비율입니다. 기존 신용대출·카드론·자동차 할부가 있으면 주담대 한도가 크게 줄어들므로 계약 전 반드시 기존 부채를 점검해야 합니다."),
        ("subscription-points-84", "청약 가점제 84점 만점 계산 기준표 — 무주택·부양가족·통장기간 총정리",
         "무주택기간(32점) + 부양가족수(35점) + 청약통장 가입기간(17점) 84점 만점 항목별 점수표.",
         "청약 가점은 무주택기간 만 15년 이상(32점), 본인 제외 부양가족 6명 이상(35점), 청약통장 가입 15년 이상(17점)이 만점입니다. 만 30세 미만 미혼은 혼인신고일 또는 만 30세부터 무주택기간을 산정합니다."),
        ("first-home-tax-cut", "생애최초 주택 취득세 200만원 감면 조건 및 추징 주의사항 3가지",
         "실거래가 12억원 이하 주택 생애최초 취득세 감면 요건과 3개월 내 전입·3년 실거주 의무 정리.",
         "생애최초 취득세 감면을 받은 뒤 정당한 사유 없이 취득일로부터 3개월 이내 상시 거주를 시작하지 않거나, 3년 미만 거주 상태에서 매각·증여·임대하면 감면받은 세액이 추징될 수 있으므로 주의해야 합니다."),
        ("moving-cost-checklist", "아파트 이사·입주 초기비용 체크리스트 — 취득세·복비·이사비·가전 예산표",
         "계약금·잔금 외에 꼭 따로 준비해야 할 취득세, 법무사 등기비, 복비, 포장이사, 입주청소 예산 가이드.",
         "집값 외에도 취득세(1.1~3.3%), 중개보수(0.4~0.7%), 채권할인·등기비용, 포장이사(100~200만원), 입주청소 및 가전·커튼 비용까지 매매가의 약 3~5% 현금 여유분을 미리 확보해 두어야 잔금일 자금 경색을 막을 수 있습니다."),
    ]
    for slug, title, desc, content in guides:
        body = f"""<section class="card"><span class="pill">2026 부동산 핵심 가이드</span><h2>{html.escape(title)}</h2><p>{html.escape(content)}</p><p>👉 <a href="{BASE_URL}/"><strong>부동산·대출·청약가점 통합 계산기로 돌아가기 →</strong></a></p></section>"""
        (DIST / "p" / f"{slug}.html").write_text(_render_page(title, desc, f"p/{slug}.html", body, []), encoding="utf-8")
        urls.append(f"{BASE_URL}/p/{slug}.html")
        guide_links.append((title.split("—")[0].strip(), f"p/{slug}.html"))

    # 5. Interactive Index Page
    loan_dir = "".join(f'<a href="{u}">{html.escape(t)}</a>' for t, u in loan_links)
    sale_dir = "".join(f'<a href="{u}">{html.escape(t)}</a>' for t, u in sale_links)
    jeonse_dir = "".join(f'<a href="{u}">{html.escape(t)}</a>' for t, u in jeonse_links)
    guide_dir = "".join(f'<a href="{u}">{html.escape(t)}</a>' for t, u in guide_links)

    home_body = f"""
<div class="grid2">
  <section class="card" id="loan">
    <span class="pill">1. 주담대·신용대출</span>
    <h2>대출 이자 계산기</h2>
    <label>대출 원금 (만원)<input id="lAmt" type="number" value="30000"></label>
    <label>연 이자율 (%)<input id="lRate" type="number" step="0.1" value="4.2"></label>
    <label>대출 기간 (년)<input id="lYr" type="number" value="30"></label>
    <label>상환 방식
      <select id="lType">
        <option value="pmt">원리금균등분할상환</option>
        <option value="prin">원금균등분할상환</option>
        <option value="bullet">만기일시상환</option>
      </select>
    </label>
    <button class="btn" onclick="calcLoan()">월 상환액 즉시 계산</button>
    <div class="res" id="lOut"></div>
  </section>

  <section class="card" id="jeonse">
    <span class="pill">2. 전세 vs 월세</span>
    <h2>전월세 전환·유불리 계산기</h2>
    <label>전세 보증금 (만원)<input id="jFull" type="number" value="30000"></label>
    <label>반전세/월세 보증금 (만원)<input id="jDep" type="number" value="10000"></label>
    <label>제안 월세 (만원)<input id="jRent" type="number" value="80"></label>
    <label>내 전세대출 금리 (%)<input id="jRate" type="number" step="0.1" value="4.0"></label>
    <button class="btn" onclick="calcJeonse()">전세 vs 월세 손익 비교</button>
    <div class="res" id="jOut"></div>
  </section>
</div>

<div class="grid2">
  <section class="card" id="fee">
    <span class="pill">3. 부동산 복비·취득세</span>
    <h2>중개수수료 & 취득세 계산기</h2>
    <label>거래 유형
      <select id="fKind">
        <option value="sale">주택 매매</option>
        <option value="lease">주택 전세/임대차</option>
      </select>
    </label>
    <label>거래 금액 / 환산보증금 (만원)<input id="fPrice" type="number" value="60000"></label>
    <label>생애최초 감면 여부 (매매 12억 이하)
      <select id="fFirst">
        <option value="no">일반 1주택</option>
        <option value="yes">생애최초 (취득세 200만원 감면)</option>
      </select>
    </label>
    <button class="btn" onclick="calcFee()">복비·취득세 즉시 계산</button>
    <div class="res" id="fOut"></div>
  </section>

  <section class="card" id="point">
    <span class="pill">4. 청약 가점 84점</span>
    <h2>주택청약 가점 계산기</h2>
    <label>무주택 기간 (년, 만30세 또는 혼인일 기준)<input id="pNo" type="number" value="7" min="0" max="20"></label>
    <label>부양가족 수 (본인 제외, 명)<input id="pFam" type="number" value="2" min="0" max="8"></label>
    <label>청약통장 가입기간 (년)<input id="pAcc" type="number" value="8" min="0" max="20"></label>
    <button class="btn" onclick="calcPoint()">내 청약 가점 확인</button>
    <div class="res" id="pOut"></div>
  </section>
</div>

<section class="card" id="directory">
  <h2>금액별 빠른 조회 표 ({len(urls)-1}개 상세 페이지)</h2>
  <h3>대출 금액별 30년 월 상환액표</h3>
  <div class="linklist">{loan_dir}</div>
  <h3>아파트 매매가별 취득세·복비표</h3>
  <div class="linklist">{sale_dir}</div>
  <h3>전세 보증금별 월세 전환·복비표</h3>
  <div class="linklist">{jeonse_dir}</div>
  <h3>2026 부동산·대출 핵심 가이드</h3>
  <div class="linklist">{guide_dir}</div>
</section>
""" + """
<script>
function fmt(n){return Math.round(n).toLocaleString('ko-KR');}
function calcLoan(){
  const P=(+document.getElementById('lAmt').value||0)*10000;
  const r=(+document.getElementById('lRate').value||0)/100/12;
  const n=(+document.getElementById('lYr').value||1)*12;
  const t=document.getElementById('lType').value;
  let html='';
  if(t==='pmt'){
    const m=r===0?P/n:P*(r*Math.pow(1+r,n))/(Math.pow(1+r,n)-1);
    html=`매월 납입금: <strong>${fmt(m)}원</strong><br>총 이자: ${fmt(m*n-P)}원 · 총 상환액: ${fmt(m*n)}원`;
  } else if(t==='prin'){
    const p0=P/n; const first=p0+P*r; const last=p0+p0*r; const totInt=P*r*(n+1)/2;
    html=`첫 달 납입금: <strong>${fmt(first)}원</strong> → 마지막 달: ${fmt(last)}원<br>총 이자: ${fmt(totInt)}원 (원리금균등 대비 절약!)`;
  } else {
    const m=P*r;
    html=`매월 이자만: <strong>${fmt(m)}원</strong><br>총 이자: ${fmt(m*n)}원 (만기 시 원금 ${fmt(P)}원 일시 상환)`;
  }
  document.getElementById('lOut').innerHTML=html;
}
function calcJeonse(){
  const full=+document.getElementById('jFull').value||0;
  const dep=+document.getElementById('jDep').value||0;
  const rent=+document.getElementById('jRent').value||0;
  const rate=+document.getElementById('jRate').value||0;
  const diff=Math.max(1, full-dep);
  const convRate=(rent*12/diff)*100;
  const loanInt=diff*(rate/100)/12;
  const gap=rent-loanInt;
  const verdict=gap>0?`전세대출(연 ${rate}%)이 매달 약 <strong>${fmt(gap*10000)}원 유리</strong>`:`제안 월세가 매달 약 <strong>${fmt(-gap*10000)}원 유리</strong>`;
  document.getElementById('jOut').innerHTML=`실제 전월세 전환율: <strong>연 ${convRate.toFixed(2)}%</strong><br>차액(${fmt(diff)}만원) 대출 시 월이자: 약 ${fmt(loanInt*10000)}원<br>판정: ${verdict}`;
}
function calcFee(){
  const kind=document.getElementById('fKind').value;
  const p=+document.getElementById('fPrice').value||0;
  const first=document.getElementById('fFirst').value==='yes';
  let rate=0.4, cap=1e9;
  if(kind==='sale'){
    if(p<5000){rate=0.6;cap=25;}else if(p<20000){rate=0.5;cap=80;}else if(p<90000){rate=0.4;}
    else if(p<120000){rate=0.5;}else if(p<150000){rate=0.6;}else{rate=0.7;}
  } else {
    if(p<5000){rate=0.5;cap=20;}else if(p<10000){rate=0.4;cap=30;}else if(p<60000){rate=0.3;}
    else if(p<120000){rate=0.4;}else if(p<150000){rate=0.5;}else{rate=0.6;}
  }
  const fee=Math.min(p*rate/100, cap);
  let extra='';
  if(kind==='sale'){
    let tr=p<=60000?1.0:(p<=90000?((p/10000)*(2/3)-3):3.0);
    let totR=tr*1.1;
    let tax=p*totR/100;
    if(first && p<=120000) tax=Math.max(0, tax-200);
    extra=`<br>1주택 예상 취득세(${totR.toFixed(2)}%): <strong>약 ${fmt(tax)}만원</strong>`;
  }
  document.getElementById('fOut').innerHTML=`중개보수 상한(${rate}%): <strong>최대 ${fmt(fee)}만원</strong> (부가세 10% 포함 ${fmt(fee*1.1)}만원)${extra}`;
}
function calcPoint(){
  const no=Math.min(15, Math.max(0, +document.getElementById('pNo').value||0));
  const fam=Math.min(6, Math.max(0, +document.getElementById('pFam').value||0));
  const acc=Math.min(15, Math.max(0, +document.getElementById('pAcc').value||0));
  const pNo = no===0 ? 2 : Math.min(32, no*2 + 2);
  const pFam = fam*5 + 5;
  const pAcc = acc===0 ? 1 : Math.min(17, acc + 2);
  const tot = pNo + pFam + pAcc;
  document.getElementById('pOut').innerHTML=`총 청약 가점: <strong>${tot}점 / 84점</strong><br>(무주택 ${pNo}점 + 부양가족 ${pFam}점 + 통장 ${pAcc}점)`;
}
calcLoan();calcJeonse();calcFee();calcPoint();
</script>
"""
    home_faq = [
        ("2026년 아파트 매매 부동산 중개수수료(복비) 상한요율은 얼마인가요?", "2억~9억원 미만 0.4%, 9억~12억원 미만 0.5%, 12억~15억원 미만 0.6%, 15억원 이상 0.7%가 법정 상한이며 상한 이내에서 협의합니다."),
        ("전세와 월세 전환율 비교는 어떻게 하나요?", "보증금 차액 대비 월세×12를 나눈 전환율이 본인 전세대출 금리보다 낮으면 월세가 유리하고, 높으면 전세대출이 유리합니다."),
    ]
    (DIST / "index.html").write_text(
        _render_page(
            "2026 부동산·대출 이자·전월세 전환·복비·취득세·청약가점 무료 계산기",
            "주택담보대출 원리금균등 이자, 전세 vs 월세 전환율, 부동산 중개수수료(복비), 1주택·생애최초 취득세, 청약 가점 84점을 한 번에 계산하세요.",
            "",
            home_body,
            home_faq,
        ),
        encoding="utf-8",
    )

    # Verification, ads.txt, robots.txt, IndexNow, sitemap.xml
    (DIST / "ads.txt").write_text(f"google.com, {ADSENSE_CLIENT.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
    (DIST / GSC_FILE).write_text(GSC_CONTENT, encoding="utf-8")
    (DIST / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")
    sm = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls)
        + "\n</urlset>\n"
    )
    (DIST / "sitemap.xml").write_text(sm, encoding="utf-8")
    print(f"Built house-calc-kr: {len(urls)} pages -> {DIST}")


if __name__ == "__main__":
    main()
