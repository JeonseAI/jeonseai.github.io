"""index.html 의 디자인·움직임을 그대로 가져와 영상용 film.html 을 만든다.
index.html 은 읽기만 한다."""
import re, sys
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + os.sep
s = open(R + 'index.html', encoding='utf-8').read()

def cut(a, b, inclusive_b=False):
    i = s.index(a); j = s.index(b, i)
    return s[i:j + (len(b) if inclusive_b else 0)].strip()

landing_css = s[s.index('<style>') + 7:s.index('</style>')]
hero_stage = cut('<div class="stage" role="img"', '<p class="hnote">')
wcs = cut('<div class="wcs">', '<p class="wnext')
stations = cut('<div class="stations" data-stations>', '<div class="askai"')
askai = s[s.index('<div class="askai" data-askai>'):]
askai = askai[:askai.index('</section>')].strip()
# askai 끝의 how 섹션 닫는 태그 2개 제거 (askai = div.askai > div.wrap)
_pi = askai.index('<div class="pill'); _e = askai.index('</div>\n</div>\n</div>', _pi) + len('</div>\n</div>\n</div>')
askai = askai[:_e]
tri = cut('<div class="tri" data-ring>', '\n</div>\n</section>')
ai_svg = re.search(r'<svg class="ai" viewBox="0 0 35 40".*?</svg>', s, re.S).group(0)
ai_svg = re.sub(r'aig\d+', 'aigend', ai_svg)

# 등장 효과(.rv · .ln)를 위한 .in 은 장면 쪽에서 붙인다
captions = [
 '등기부 사진 몇 장, 약 30초. <b>위험한 줄을 내 사진 위에</b> 형광펜으로 표시해요.',
 '이 지역 <b>실제 경매 매각가율</b>로 계산해요. 먼저 받는 최우선변제까지 넣어요.',
 'AI가 실제 판례 중 <b>이 집과 닮은 사건</b>을 골라, 이 집 숫자로 설명해요.',
 '위험 신호에 맞춘 <b>질문을 그대로</b> 보여 주세요. 멈춰야 할 답도 함께 알려요.',
 '잔금 날 아침에 알려 드려요. 다시 찍으면 <b>새로 생긴 빚만</b> 골라 보여 줘요.',
]

film_css = r'''
/* ━━━━━━━━ 영상용 무대 (여기부터는 film.html 전용) ━━━━━━━━ */
@font-face{font-family:"Jua";font-weight:400;font-display:block;src:url(film/fonts/Jua.film.woff2) format("woff2")}
@font-face{font-family:"Noto Serif KR";font-weight:700;font-display:block;src:url(film/fonts/NotoSerifKR-Bold.film.woff2) format("woff2")}
html,body{margin:0;height:100%;overflow:hidden !important;background:var(--fbg,#07140F) !important;transition:background-color .6s ease;cursor:none}
body::before{display:none}
#fstage{position:absolute;left:50%;top:50%;width:1920px;height:1080px;margin:-540px 0 0 -960px;transform:scale(var(--k,1));overflow:hidden;color:var(--white)}
.fsc{position:absolute;inset:0;padding:54px 96px;display:none;flex-direction:column;justify-content:center;opacity:0;transition:opacity .6s ease}
.fsc.on{display:flex}
.fsc.on.f-s1{display:grid}
.fsc.vis{opacity:1}
.f-dark{background:radial-gradient(ellipse at 30% 30%,#0F3A2A,#07140F 65%)}
.f-paper{background:var(--paper);color:var(--text)}
.f-black{background:#030806}
.f-forest{background:radial-gradient(ellipse at 70% 30%,#14503A,#0E3526 60%)}
.f-a{opacity:0;transform:translateY(28px);transition:opacity .55s var(--fin), transform .7s var(--fin)}
.vis .f-a{opacity:1;transform:none}
.vis .f-a.d1{transition-delay:.12s}.vis .f-a.d2{transition-delay:.24s}.vis .f-a.d3{transition-delay:.36s}
#fstage{--fin:cubic-bezier(.2,.8,.2,1)}
.f-kick{font-size:34px;font-weight:800;letter-spacing:.08em;color:var(--gold)}
.f-paper .f-kick{color:var(--green)}
.f-h{margin:18px 0 0;font-size:104px;line-height:1.16;letter-spacing:-.045em;font-weight:800}
.f-hl{position:relative;display:inline-block;color:var(--gold);isolation:isolate}
.f-hl::after{content:"";position:absolute;left:-6px;right:-6px;bottom:.06em;height:.24em;border-radius:6px;background:rgba(226,194,127,.32);z-index:-1;transform-origin:0 50%;transform:scaleX(0);transition:transform .8s cubic-bezier(.6,.1,.2,1) .5s}
.vis .f-hl::after{transform:none}
.f-hl.gr{color:var(--green)}.f-hl.gr::after{background:rgba(20,114,75,.2)}
.f-p{margin:28px 0 0;font-size:44px;line-height:1.45;color:var(--dim);letter-spacing:-.02em}
.f-p b{color:var(--white)}
.f-paper .f-p{color:var(--body)}.f-paper .f-p b{color:var(--text)}
.f-src{position:absolute;left:96px;bottom:54px;font-size:26px;color:rgba(255,255,255,.5)}

/* 1 질문: 왼쪽 제목 + 오른쪽 랜딩 폰 장면(그대로, 1.4배) */
.f-s1{display:grid;grid-template-columns:1fr 760px;gap:20px;align-items:center}
.f-s1 .f-h{font-size:108px}
.f-phone{width:540px;zoom:1.4;justify-self:center}
.f-phone .stage{margin:0}

/* 2 현실: 숫자 + 그래프가 그려짐 → 100명 중 76명 */
.f-s2 .f-part{position:absolute;inset:54px 96px;display:flex;flex-direction:column;justify-content:center;transition:opacity .5s ease, transform .6s var(--fin)}
.f-s2 .f-p2{opacity:0;transform:translateY(30px)}
.f-s2[data-step="1"] .f-p1{opacity:0;transform:translateY(-30px)}
.f-s2[data-step="1"] .f-p2{opacity:1;transform:none}
.f-row2{display:grid;grid-template-columns:minmax(0,1fr) 860px;gap:56px;align-items:center}
.f-num{font-size:180px;line-height:1;font-weight:800;letter-spacing:-.05em;color:var(--gold);font-variant-numeric:tabular-nums;margin-top:18px;white-space:nowrap}
.f-num small{font-size:80px;margin-left:10px;color:var(--white)}
.f-ch{position:relative;border-radius:36px;background:rgba(255,255,255,.04);border:2px solid rgba(255,255,255,.1);padding:34px 34px 24px}
.f-ch b{display:block;font-size:34px}
.f-ch span{display:block;font-size:26px;color:var(--dim);margin-top:6px}
.f-ch svg{display:block;width:100%;height:auto;margin-top:18px;overflow:visible}
.f-ch .grid line{stroke:rgba(255,255,255,.1);stroke-width:2}
.f-ch .ax{fill:rgba(255,255,255,.6);font-size:24px;font-family:var(--sans)}
.f-ch .ln2{fill:none;stroke:#BD872C;stroke-width:5;stroke-linejoin:round;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1}
.f-ch .area{fill:url(#far);opacity:0}
.f-ch .pt{fill:#BD872C;stroke:#0A1E16;stroke-width:4;opacity:0}
.f-ch .end{fill:var(--gold-hi);stroke:#0A1E16;stroke-width:4;opacity:0}
.f-ch .endlab{fill:#fff;font-size:30px;font-weight:800;font-family:var(--sans);opacity:0}
.vis .f-ch .ln2{stroke-dashoffset:0;transition:stroke-dashoffset 2.2s cubic-bezier(.4,0,.2,1) .5s}
.vis .f-ch .area,.vis .f-ch .pt{opacity:.9;transition:opacity .8s ease 2.4s}
.vis .f-ch .end,.vis .f-ch .endlab{opacity:1;transition:opacity .5s ease 2.6s}
.f-dots{display:grid;grid-template-columns:repeat(20,40px);gap:14px;margin-top:44px}
.f-dots i{width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.16);transform:scale(.4);opacity:0;transition:transform .3s ease, opacity .3s ease}
.f-dots i.y{background:var(--gold)}
.f-s2[data-step="1"] .f-dots i{transform:none;opacity:1}

/* 3 왜 어려운가: 랜딩 카드 3장(무너지는 집 · 낯선 말 · 단계 선) */
.f-s3 .f-h{font-size:96px}
.f-s3 .wcs{zoom:1.5;margin-top:30px;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.f-s3 .wc h3{font-size:30px;margin-bottom:8px}
.f-s3 .wc .no{width:36px;height:36px;font-size:16px}
.f-s3 .wc p{font-size:24px;line-height:1.45}

/* 4 하는 일: 랜딩 카드 5장을 펼친 뒤 한 장씩 */
.f-s4 .f-h{font-size:96px}
.f-s4 .stations{zoom:1.25;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px;overflow:visible;margin:26px 0 0;padding:0 8px}
.f-s4 .stn{flex:none;transition:opacity .45s ease, transform .45s var(--fin), box-shadow .45s ease;opacity:0;transform:translateY(40px)}
.f-s4.vis .stn{opacity:1;transform:none}
.f-s4.vis .stn:nth-child(2){transition-delay:.08s}.f-s4.vis .stn:nth-child(3){transition-delay:.16s}.f-s4.vis .stn:nth-child(4){transition-delay:.24s}.f-s4.vis .stn:nth-child(5){transition-delay:.32s}
.f-s4 .stn p{display:none}
.f-s4 .stn h3{font-size:24px;min-height:62px}
.f-s4 .when,.f-s4 .ai-b{font-size:14px}
.f-s4.vis[data-step]:not([data-step="0"]) .stn{opacity:.32;transform:scale(.97);transition-delay:0s}
.f-s4.vis[data-step="1"] .stn:nth-child(1),.f-s4.vis[data-step="2"] .stn:nth-child(2),.f-s4.vis[data-step="3"] .stn:nth-child(3),.f-s4.vis[data-step="4"] .stn:nth-child(4),.f-s4.vis[data-step="5"] .stn:nth-child(5){opacity:1;transform:translateY(-10px) scale(1.04);box-shadow:0 34px 70px -30px rgba(22,33,27,.55),0 0 0 3px var(--green)}
.f-cap{position:relative;height:130px;margin-top:34px}
.f-cap p{position:absolute;inset:0;margin:0;font-size:44px;line-height:1.45;color:var(--body);letter-spacing:-.02em;opacity:0;transform:translateY(16px);transition:opacity .4s ease, transform .5s var(--fin)}
.f-cap p b{color:var(--text)}
.f-s4[data-step="1"] .f-cap p:nth-child(1),.f-s4[data-step="2"] .f-cap p:nth-child(2),.f-s4[data-step="3"] .f-cap p:nth-child(3),.f-s4[data-step="4"] .f-cap p:nth-child(4),.f-s4[data-step="5"] .f-cap p:nth-child(5){opacity:1;transform:none}

/* 5 챗봇: 랜딩 연보라 카드 그대로, 질문이 한 글자씩 */
.f-s5{padding:0}
.f-s5 .askai{zoom:1.7;margin:0;border-radius:0;height:calc(1080px / 1.7);display:flex;flex-direction:column;justify-content:center;box-shadow:none}
.f-s5 .askai .lead .sen:last-child{display:none}
.f-s5 .askai .kick{font-size:20px}
.f-s5 .askai .h2{font-size:62px;line-height:1.2}
.f-s5 .askai .lead{font-size:26px;max-width:none}
.f-s5 .pill{width:640px;margin-top:40px;padding:20px 26px 20px 30px}
.f-s5 .pt{font-size:28px}.f-s5 .cur{height:30px}

/* 6 철학: 큰 글씨가 왼쪽부터 차오름 */
.f-s6 .f-line{position:absolute;inset:54px 96px;display:flex;flex-direction:column;justify-content:center;opacity:0;transform:translateY(40px);transition:opacity .5s ease, transform .7s var(--fin)}
.f-s6[data-step="0"] .l1,.f-s6[data-step="1"] .l2,.f-s6[data-step="2"] .l3{opacity:1;transform:none}
.f-s6 .fill{font-size:210px;line-height:1.08;margin-top:10px}
.f-s6 .f-p{max-width:1500px}
.f-ups{display:flex;align-items:center;gap:22px;margin-top:44px}
.f-ups img{height:44px;margin-right:10px}
.f-ups .model{font-size:28px;min-height:0;padding:12px 26px}

/* 7 비전: 문장 → 개인 · 기관 · 나라 삼각형 */
.f-s7 .f-part{position:absolute;inset:54px 96px;display:flex;flex-direction:column;justify-content:center;transition:opacity .5s ease, transform .6s var(--fin)}
.f-s7 .f-p2{opacity:0;transform:translateY(30px)}
.f-s7[data-step="1"] .f-p1{opacity:0;transform:translateY(-30px)}
.f-s7[data-step="1"] .f-p2{opacity:1;transform:none}
.f-s7 .vh{font-size:120px;line-height:1.36}
.f-s7 .tri{zoom:1.55;margin-top:0}
.f-s7 .tri-l b{font-size:19px}.f-s7 .tri-l p{font-size:16px}

/* 8 엔딩 */
.f-s8{align-items:center;text-align:center}
.f-lock{display:flex;align-items:center;gap:40px}
.f-icon{width:190px;height:190px;border-radius:50px;background:var(--paper);display:flex;align-items:center;justify-content:center;box-shadow:0 30px 60px -30px rgba(0,0,0,.8)}
.f-icon img{width:66%}
.f-s8 .wm{font-size:180px;letter-spacing:-2px}
.f-s8 .f-p{margin-top:40px}
'''

dots = ''.join('<i class="y"></i>' if k < 76 else '<i></i>' for k in range(100))
cap = ''.join(f'<p>{c}</p>' for c in captions)
html = f'''<!doctype html>
<html lang="ko" class="an">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>전세이프 · 부스 영상</title>
<link rel="icon" href="favicon.png">
<!-- 부스 노트북용 영상 랜딩. 디자인과 움직임은 index.html 에서 그대로 가져온다(scripts 없이 손으로 고치지 말고, 바꿀 땐 index 를 먼저 고친다). -->
<style>
{landing_css}
{film_css}
</style>
</head>
<body>
<div id="fstage">

<section class="fsc f-dark f-s1" data-bg="#07140F">
<div>
<div class="f-kick f-a">AI 전세사기 예방 서비스</div>
<h1 class="f-h f-a d1">내 보증금,<br>돌려받을 수<br>있을까요?<br><span class="f-hl">찍어서 확인하세요</span></h1>
</div>
<div class="f-phone">{hero_stage}</div>
</section>

<section class="fsc f-dark f-s2" data-bg="#0A1E16">
<div class="f-part f-p1">
<div class="f-row2">
<div>
<div class="f-kick f-a">전세사기, 지금</div>
<div class="f-h f-a d1" style="font-size:96px">피해 인정만</div>
<div class="f-num f-a d1"><span data-count="41559">0</span><small>건</small></div>
<p class="f-p f-a d2">2023년 6월 특별법 시행 뒤 쌓인 숫자예요.</p>
</div>
<div class="f-ch f-a d2"><b>전세사기 피해자 결정 누적 건수</b><span>2023.6 특별법 시행 ~ 2026.9 · 국토교통부 발표</span><div data-fchart></div></div>
</div>
</div>
<div class="f-part f-p2">
<div class="f-kick">전세사기, 지금</div>
<div class="f-h"><span class="f-hl" style="--x:0">100명 중 76명</span>은<br>40세 미만이에요</div>
<p class="f-p">30대 50.7% · 20대 25.2%</p>
<div class="f-dots">{dots}</div>
</div>
<p class="f-src">출처: 국토교통부 발표(2026.10.12) · 언론 보도</p>
</section>

<section class="fsc f-dark f-s3 why" data-bg="#06110D">
<div class="f-kick f-a">왜 막기 어려울까</div>
<div class="f-h f-a d1">혼자 막기엔, <span class="f-hl">챙길 게 너무 많아요</span></div>
{wcs}
</section>

<section class="fsc f-paper f-s4" data-bg="#F2EEE5">
<div class="f-kick f-a">전세이프가 하는 일</div>
<div class="f-h f-a d1">사진 몇 장으로, <span class="f-hl gr">다섯 가지</span>를 챙겨요</div>
{stations}
<div class="f-cap">{cap}</div>
</section>

<section class="fsc f-s5" data-bg="#EEE9FF">
{askai}
</section>

<section class="fsc f-black f-s6 trust" data-bg="#030806">
<div class="f-line l1"><div class="f-kick">믿을 수 있게</div><p class="fill" data-ffill>판정은 규칙이</p><p class="f-p">위험 등급은 HUG 전세보증 가입 요건과 한국부동산원 전세가율 기준으로만 정해요. AI는 등급을 바꾸지 못해요.</p></div>
<div class="f-line l2"><div class="f-kick">믿을 수 있게</div><p class="fill g" data-ffill>설명은 AI가</p><p class="f-p">한국 부동산 문제는 한국 AI로 풀어요. 두 갈래로 따로 읽고 서로 맞춰 봐서, 놓치는 줄 없이 꼼꼼하게 분석해요.</p>
<div class="f-ups"><img src="assets/upstage.png" alt="Upstage"><span class="model">Information Extract</span><span class="model">Document OCR</span><span class="model">Solar Pro 2</span><span class="model">Embeddings</span></div></div>
<div class="f-line l3"><div class="f-kick">믿을 수 있게</div><p class="fill" data-ffill>검증은 사용자가</p><p class="f-p">판정 근거를 내가 찍은 사진 위에서 직접 확인해요. 못 잡는 위험은 못 잡는다고 그대로 적어요.</p></div>
</section>

<section class="fsc f-forest f-s7 with" data-bg="#0E3526">
<div class="f-part f-p1">
<div class="f-kick f-a">우리가 꿈꾸는 세상</div>
<p class="vh f-a d1" style="margin-top:24px">피해 뒤의 구제보다,<br>계약 전의 확인이<br><em>당연한 세상</em></p>
</div>
<div class="f-part f-p2">{tri}</div>
</section>

<section class="fsc f-dark f-s8" data-bg="#07140F">
<div class="f-lock f-a"><span class="f-icon"><img src="assets/logo.png" alt=""></span><span class="wm" role="img" aria-label="전세AI프">전세{ai_svg}프</span></div>
<p class="f-p f-a d1">전세를 AI로 안전하게</p>
<p class="f-p f-a d2" style="margin-top:14px;color:var(--gold)">팀 동크크</p>
</section>

</div>
<script>
(function () {{
  // 장면: dur(ms) · steps(단계가 바뀌는 시점) · ins([시점, 선택자] → .in 을 붙여 랜딩 움직임 시작) · freeze(이 시점에 반복 움직임을 멈춰 완성 화면으로 고정)
  var PLAN = [
    {{ dur: 12300, steps: [], ins: [], freeze: 10800 }},
    {{ dur: 9200, steps: [5200], ins: [] }},
    {{ dur: 7000, steps: [], ins: [[500, '.wc']], freeze: 5300 }},
    {{ dur: 17000, steps: [2200, 5200, 8200, 11200, 14200], ins: [[300, '.stn'], [2200, '.stn:nth-child(1)', 1], [5200, '.stn:nth-child(2)', 1], [8200, '.stn:nth-child(3)', 1], [11200, '.stn:nth-child(4)', 1], [14200, '.stn:nth-child(5)', 1]] }},
    {{ dur: 4800, steps: [], ins: [[150, '.askai']], type: [900, '확정일자|는 언제 받아야 해?'] }},
    {{ dur: 9000, steps: [3000, 6000], ins: [], fills: [0, 3000, 6000] }},
    {{ dur: 7300, steps: [3000], ins: [[3100, '.tri']] }},
    {{ dur: 4500, steps: [], ins: [] }}
  ];
  var stage = document.getElementById('fstage');
  var scenes = Array.prototype.slice.call(stage.querySelectorAll('.fsc'));
  var root = document.documentElement;
  function fit() {{ stage.style.setProperty('--k', Math.min(innerWidth / 1920, innerHeight / 1080)); }}
  addEventListener('resize', fit); fit();

  // 그래프 (랜딩과 같은 숫자)
  var SERIES = [[0, 0], [5, 9100], [10, 15433], [18, 25578], [20, 27372], [24, 31437], [28, 34481], [30, 35909], [36, 39669], [39, 41559]];
  (function () {{
    var W = 900, H = 470, L = 70, Rr = 20, T = 40, B = 40;
    var X = function (m) {{ return L + (W - L - Rr) * m / 40; }}, Y = function (v) {{ return T + (H - T - B) * (1 - v / 45000); }};
    var g = '', ax = '';
    [10000, 20000, 30000, 40000].forEach(function (v) {{ g += '<line x1="' + L + '" x2="' + (W - Rr) + '" y1="' + Y(v) + '" y2="' + Y(v) + '"/>'; ax += '<text x="' + (L - 12) + '" y="' + (Y(v) + 8) + '" text-anchor="end">' + (v / 10000) + '만</text>'; }});
    [[7, '2024'], [19, '2025'], [31, '2026']].forEach(function (a) {{ ax += '<text x="' + X(a[0]) + '" y="' + (H - 4) + '" text-anchor="middle">' + a[1] + '</text>'; }});
    var d = SERIES.map(function (p, k) {{ return (k ? 'L' : 'M') + X(p[0]).toFixed(1) + ' ' + Y(p[1]).toFixed(1); }}).join('');
    var e = SERIES[SERIES.length - 1];
    var pts = SERIES.slice(0, -1).map(function (p) {{ return '<circle class="pt" r="7" cx="' + X(p[0]) + '" cy="' + Y(p[1]) + '"/>'; }}).join('');
    document.querySelector('[data-fchart]').innerHTML = '<svg viewBox="0 0 ' + W + ' ' + H + '" aria-hidden="true"><defs><linearGradient id="far" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#BD872C" stop-opacity=".4"/><stop offset="1" stop-color="#BD872C" stop-opacity="0"/></linearGradient></defs><g class="grid">' + g + '</g><g class="ax">' + ax + '</g><path class="area" d="' + d + 'L' + X(e[0]) + ' ' + Y(0) + 'L' + X(0) + ' ' + Y(0) + 'Z"/><path class="ln2" pathLength="1" d="' + d + '"/>' + pts + '<circle class="end" r="11" cx="' + X(e[0]) + '" cy="' + Y(e[1]) + '"/><text class="endlab" x="' + (X(e[0]) - 18) + '" y="' + (Y(e[1]) - 22) + '" text-anchor="end">41,559건 · 2026.9</text></svg>';
  }})();
  var counter = document.querySelector('[data-count]'), target = +counter.getAttribute('data-count');
  var typing = stage.querySelector('[data-typing]');
  var fills = Array.prototype.slice.call(stage.querySelectorAll('[data-ffill]'));

  var cur = -1, t = 0, last = 0, paused = false, froze = false, done = {{}};
  var m = /[?&]scene=([0-9]+)/.exec(location.search);
  var startAt = m ? Math.max(0, Math.min(scenes.length - 1, +m[1] - 1)) : 0;
  function stepOf(n, ms) {{ var k = 0; PLAN[n].steps.forEach(function (b) {{ if (ms >= b) k++; }}); return k; }}
  function sceneAnims(s) {{ return s.getAnimations ? s.getAnimations({{ subtree: true }}).filter(function (a) {{ return a instanceof CSSAnimation; }}) : []; }}
  function go(n) {{
    n = (n + scenes.length) % scenes.length;
    if (cur >= 0 && cur !== n) {{
      var old = scenes[cur]; old.classList.remove('vis');
      setTimeout(function () {{ if (scenes.indexOf(old) !== cur) old.classList.remove('on'); }}, 640);
    }}
    cur = n; t = 0; froze = false; done = {{}};
    var s = scenes[n];
    s.classList.remove('on', 'vis'); s.setAttribute('data-step', '0');
    Array.prototype.forEach.call(s.querySelectorAll('.in'), function (e) {{ e.classList.remove('in'); }});
    if (s.matches('.in')) s.classList.remove('in');
    void s.offsetWidth; s.classList.add('on'); void s.offsetWidth; s.classList.add('vis');
    root.style.setProperty('--fbg', s.getAttribute('data-bg'));
    counter.textContent = '0';
    if (typing && n === 4) {{ typing.className = 'pt'; typing.innerHTML = '<i class="cur" aria-hidden="true"></i>'; }}
    fills.forEach(function (f) {{ f.style.setProperty('--p', 0); }});
  }}
  function frame() {{
    var P = PLAN[cur], s = scenes[cur], st = String(stepOf(cur, t));
    if (s.getAttribute('data-step') !== st) s.setAttribute('data-step', st);
    P.ins.forEach(function (x, k) {{ if (t >= x[0] && !done['i' + k]) {{ done['i' + k] = 1; Array.prototype.forEach.call(s.querySelectorAll(x[1]), function (e) {{ if (x[2]) {{ e.classList.remove('in'); void e.offsetWidth; }} e.classList.add('in'); }}); }} }});
    if (P.freeze && !froze && t >= P.freeze) {{ froze = true; sceneAnims(s).forEach(function (a) {{ a.pause(); }}); }}
    if (cur === 1) {{ var p = Math.min(1, Math.max(0, (t - 300) / 1100)); p = 1 - Math.pow(1 - p, 3); counter.textContent = Math.round(target * p).toLocaleString('ko-KR'); }}
    if (P.type) {{
      var parts = P.type[1].split('|'), all = parts.join(''), n = Math.max(0, Math.min(all.length, Math.floor((t - P.type[0]) / 85)));
      if (done.typed !== n) {{ done.typed = n; var a = all.slice(0, n), b1 = a.slice(0, parts[0].length), b2 = a.slice(parts[0].length);
        typing.innerHTML = (b1 ? '<span>' + b1 + '</span>' : '') + (b2 ? '<i class="nb">' + b2 + '</i>' : '') + '<i class="cur" aria-hidden="true"></i>';
        if (n === all.length) setTimeout(function () {{ typing.classList.add('done'); }}, 300); }}
    }}
    if (P.fills) P.fills.forEach(function (at, k) {{ var p = Math.min(1, Math.max(0, (t - at - 450) / 1300)); fills[k].style.setProperty('--p', (1 - Math.pow(1 - p, 2)).toFixed(3)); }});
    window.__film = {{ scene: cur + 1, t: t }};
    if (t >= P.dur) go(cur + 1);
  }}
  function tick(now) {{
    if (!last) last = now;
    var dt = now - last; last = now;
    if (!paused) {{ t += dt; frame(); }}
    requestAnimationFrame(tick);
  }}
  // 리허설: 스페이스 = 멈춤/재생, ←/→ = 이전/다음 장면 (화면에 안내는 없음)
  addEventListener('keydown', function (e) {{
    if (e.code === 'Space') {{ e.preventDefault(); paused = !paused; sceneAnims(scenes[cur]).forEach(function (a) {{ if (paused) a.pause(); else if (!froze) a.play(); }}); }}
    else if (e.key === 'ArrowRight') go(cur + 1);
    else if (e.key === 'ArrowLeft') go(cur - 1);
  }});
  var begin = function () {{ go(startAt); requestAnimationFrame(tick); }};
  if (document.fonts && document.fonts.ready) Promise.race([document.fonts.ready, new Promise(function (r) {{ setTimeout(r, 1500); }})]).then(begin); else begin();
}})();
</script>
</body>
</html>
'''
open(R + 'film.html', 'w', encoding='utf-8').write(html)
print('ok', len(html))
