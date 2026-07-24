# -*- coding: utf-8 -*-
"""seats.json -> award_demo.html (v2: 라이트 테마 + 캘린더 히트맵, awardfares 계열)."""
import json

def _load(p):
    try: return json.load(open(p, encoding="utf-8"))
    except FileNotFoundError: return None
REGION = {"일본":"일본","중국":"중국·동북아","베트남":"동남아","미국":"미주"}
ORDER  = {"미국":0,"베트남":1,"일본":2,"중국":3}
MILES_KE = {"일본":{"e":15000,"b":22500},"중국":{"e":15000,"b":22500},"베트남":{"e":20000,"b":30000},"미국":{"e":35000,"b":62500}}
MILES_OZ = {"일본":{"e":15000,"b":27000},"중국":{"e":15000,"b":27000},"베트남":{"e":20000,"b":30000},"미국":{"e":35000,"b":62500}}
BOOK = "https://www.koreanair.com/booking/book-and-manage/award-seat-availability"
PARK = "https://xn--ob0b687b5lan1cq1ch1hexa692c.com/booking"

def _rows(data, miles, book_def):
    out=[]
    if not data: return out, ""
    for key,r in data["routes"].items():
        arr=key.split("-")[1]; bk=r.get("book_url",book_def)
        for iso,av in r["dates"].items():
            out.append({"date":iso,"arr":arr,"dest":r["dest"],"country":r["country"],
                        "region":REGION.get(r["country"],r["country"]),"e":av["e"],"b":av["b"],
                        "me":miles[r["country"]]["e"],"mb":miles[r["country"]]["b"],
                        "ord":ORDER.get(r["country"],9),"bk":bk})
    return out, (data.get("updated","")[:16].replace("T"," "))

rows_ke, updated = _rows(_load("seats.json"), MILES_KE, BOOK)
rows_oz, _upd_oz = _rows(_load("oz_seats.json"), MILES_OZ, "https://flyasiana.com/I/KR/KO/MileageSeatSearch.do")

tpl = r"""<title>마일캐치 · 대한항공 마일리지 잔여석 한눈에</title>
<style>
:root{
 --bg:#EEF2F7; --surface:#FFFFFF; --surface2:#F7F9FC; --border:#E2E8F1;
 --text:#141B2B; --muted:#5A6678; --faint:#93A0B3;
 --accent:#1D6FE0; --accent-soft:#E7F0FD;
 --eco:#10B981; --eco-soft:#D6F5E8; --biz:#F59E0B; --biz-soft:#FCEBCD;
 --none:#EAEEF4; --danger:#DC5A47; --danger-soft:#FBE6E2;
 --shadow:0 1px 2px rgba(20,27,43,.05),0 4px 16px rgba(20,27,43,.05);
}
@media (prefers-color-scheme:dark){:root{
 --bg:#0C0F15; --surface:#151A22; --surface2:#1A212B; --border:#28313E;
 --text:#E9EEF5; --muted:#94A1B3; --faint:#5E6B7C;
 --accent:#4C93FF; --accent-soft:#182740;
 --eco:#2ED694; --eco-soft:#123227; --biz:#F5B54A; --biz-soft:#33280F;
 --none:#212932; --danger:#E17061; --danger-soft:#2C1714;
 --shadow:0 1px 2px rgba(0,0,0,.3),0 6px 20px rgba(0,0,0,.3);
}}
:root[data-theme=light]{--bg:#EEF2F7;--surface:#FFFFFF;--surface2:#F7F9FC;--border:#E2E8F1;--text:#141B2B;--muted:#5A6678;--faint:#93A0B3;--accent:#1D6FE0;--accent-soft:#E7F0FD;--eco:#10B981;--eco-soft:#D6F5E8;--biz:#F59E0B;--biz-soft:#FCEBCD;--none:#EAEEF4;--danger:#DC5A47;--danger-soft:#FBE6E2;}
:root[data-theme=dark]{--bg:#0C0F15;--surface:#151A22;--surface2:#1A212B;--border:#28313E;--text:#E9EEF5;--muted:#94A1B3;--faint:#5E6B7C;--accent:#4C93FF;--accent-soft:#182740;--eco:#2ED694;--eco-soft:#123227;--biz:#F5B54A;--biz-soft:#33280F;--none:#212932;--danger:#E17061;--danger-soft:#2C1714;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);
 font-family:"Pretendard","Malgun Gothic","Apple SD Gothic Neo",-apple-system,"Segoe UI",Roboto,sans-serif;
 font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:26px 18px 90px}
.top{display:flex;align-items:center;gap:10px;margin-bottom:22px}
.logo{font-weight:800;font-size:17px;letter-spacing:-.02em;display:flex;align-items:center;gap:7px}
.logo .m{color:var(--accent)}
.themebtn{margin-left:auto;background:var(--surface);border:1px solid var(--border);color:var(--muted);
 width:36px;height:36px;border-radius:9px;cursor:pointer;font-size:15px}
.hero{background:linear-gradient(135deg,var(--accent),#134fa8);border-radius:20px;padding:30px 30px 26px;color:#fff;box-shadow:var(--shadow)}
.hero h1{font-size:27px;font-weight:800;letter-spacing:-.02em;margin:0 0 6px;text-wrap:balance}
.hero p{margin:0 0 18px;opacity:.9;font-size:15px;max-width:56ch}
.hero .dday{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,.16);
 border:1px solid rgba(255,255,255,.28);padding:5px 12px;border-radius:999px;font-size:12.5px;font-weight:700;margin-bottom:16px}
.picks{display:flex;flex-wrap:wrap;gap:9px}
.pick{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);color:#fff;
 padding:9px 16px;border-radius:11px;font-size:14px;font-weight:700;cursor:pointer;transition:.12s}
.pick:hover{background:rgba(255,255,255,.26)}
.pick.on{background:#fff;color:var(--accent)}
.bizonly{margin-left:6px;display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.14);
 border:1px solid rgba(255,255,255,.28);padding:8px 14px;border-radius:11px;font-size:14px;font-weight:700;cursor:pointer;user-select:none}
.bizonly.on{background:var(--biz);border-color:var(--biz);color:#3a2600}
.bar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:20px 2px 12px}
.summary{font-size:15px;font-weight:600;color:var(--muted)}
.summary b{color:var(--text);font-weight:800}
.summary .hl{color:var(--biz)}
.spacer{flex:1}
.viewtog{display:inline-flex;background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:3px}
.viewtog button{border:none;background:transparent;color:var(--muted);font-weight:700;font-size:13.5px;padding:7px 14px;border-radius:8px;cursor:pointer}
.viewtog button.on{background:var(--accent);color:#fff}
.fbtn{background:var(--surface);border:1px solid var(--border);color:var(--muted);font-weight:700;
 font-size:13.5px;padding:8px 14px;border-radius:10px;cursor:pointer}
.fbtn.on{color:var(--accent);border-color:var(--accent)}
.filters{display:none;background:var(--surface);border:1px solid var(--border);border-radius:12px;
 padding:14px 16px;margin-bottom:12px;gap:14px;flex-wrap:wrap;align-items:center}
.filters.show{display:flex}
.filters .lab{font-size:12.5px;color:var(--muted);font-weight:700;margin-right:2px}
.chip{border:1px solid var(--border);background:var(--surface2);color:var(--muted);padding:7px 13px;
 border-radius:999px;font-size:13px;font-weight:600;cursor:pointer}
.chip.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.filters input{background:var(--surface2);border:1px solid var(--border);color:var(--text);border-radius:9px;padding:8px 12px;font-size:13.5px;outline:none;width:160px}
.legend{display:flex;gap:16px;align-items:center;margin:2px 2px 14px;font-size:12.5px;color:var(--muted);flex-wrap:wrap}
.legend .it{display:inline-flex;align-items:center;gap:6px}
.sw{width:14px;height:14px;border-radius:4px;display:inline-block}
.card{background:var(--surface);border:1px solid var(--border);border-radius:16px;box-shadow:var(--shadow);overflow:hidden}
/* calendar */
.month{padding:6px 4px 2px}
.mname{font-weight:800;font-size:15px;padding:12px 16px 8px;position:sticky;left:0}
.calwrap{overflow-x:auto}
.cal{border-collapse:separate;border-spacing:0}
.cal th,.cal td{padding:0}
.cal .corner{position:sticky;left:0;z-index:3;background:var(--surface);min-width:150px;text-align:left;
 font-size:11px;color:var(--faint);font-weight:700;padding:0 12px;height:34px;border-bottom:1px solid var(--border)}
.cal .dh{min-width:30px;height:34px;font-size:11px;color:var(--muted);font-weight:700;text-align:center;border-bottom:1px solid var(--border)}
.cal .dh.we{color:var(--danger)}
.cal .dh .dw{display:block;font-size:9px;color:var(--faint);font-weight:600}
.cal .rl{position:sticky;left:0;z-index:2;background:var(--surface);min-width:150px;padding:0 12px;height:34px;
 white-space:nowrap;border-bottom:1px solid var(--surface2);box-shadow:1px 0 0 var(--border)}
.cal .rl .nm{font-weight:700;font-size:13.5px}
.cal .rl .cd{color:var(--faint);font-size:11px;margin-left:5px}
.cal .rl .rg{font-size:10px;color:var(--muted);background:var(--surface2);border:1px solid var(--border);padding:1px 6px;border-radius:5px;margin-left:6px}
.cal td.cell{width:30px;height:34px;border-bottom:1px solid var(--surface2);border-right:1px solid var(--surface2);text-align:center;vertical-align:middle}
.dot{width:18px;height:18px;border-radius:6px;display:inline-block;background:var(--none);cursor:default}
.dot.e{background:var(--eco);cursor:pointer}
.dot.b{background:var(--biz);cursor:pointer}
.dot.eb{background:linear-gradient(135deg,var(--biz) 50%,var(--eco) 50%);cursor:pointer}
.dot:hover{outline:2px solid var(--accent);outline-offset:1px}
.mrow:hover td{background:var(--surface2)}
.mrow:hover .rl{background:var(--surface2)}
/* list */
.lwrap{overflow-x:auto;display:none}
.lwrap.show{display:block}
table.list{width:100%;border-collapse:collapse;min-width:640px}
.list th{text-align:left;color:var(--muted);font-size:11.5px;font-weight:700;padding:12px 16px;border-bottom:1px solid var(--border);text-transform:uppercase;letter-spacing:.03em}
.list th.c,.list td.c{text-align:center}.list th.r,.list td.r{text-align:right}
.list td{padding:13px 16px;border-bottom:1px solid var(--surface2);font-variant-numeric:tabular-nums}
.list tr:hover td{background:var(--surface2)}
.pill{font-size:12px;font-weight:800;padding:3px 9px;border-radius:6px}
.pill.e{background:var(--eco-soft);color:var(--eco)}.pill.b{background:var(--biz-soft);color:var(--biz)}
.pill.n{background:var(--none);color:var(--faint)}
.book{color:var(--accent);text-decoration:none;font-weight:700;font-size:12.5px;white-space:nowrap}
.book:hover{text-decoration:underline}
.calhint{display:none;color:var(--faint);font-size:12px;padding:10px 16px;border-top:1px solid var(--border)}
.calhint.show{display:block}
.cta{margin-top:20px;background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:18px 20px;
 display:flex;align-items:center;gap:16px;flex-wrap:wrap;box-shadow:var(--shadow)}
.cta .ico{font-size:26px}.cta .t{flex:1;min-width:200px}.cta .t b{font-size:15.5px}.cta .t div{color:var(--muted);font-size:13.5px;margin-top:2px}
.cta a{background:var(--accent);color:#fff;text-decoration:none;font-weight:800;padding:11px 20px;border-radius:11px;white-space:nowrap}
.foot{color:var(--faint);font-size:12px;margin-top:20px;line-height:1.75}
.foot b{color:var(--muted)}
#tip{position:fixed;pointer-events:none;background:var(--text);color:var(--surface);font-size:12px;font-weight:600;
 padding:7px 10px;border-radius:8px;opacity:0;transition:opacity .1s;z-index:50;white-space:nowrap;box-shadow:var(--shadow)}
.airtabs{display:flex;gap:6px;margin:0 0 16px;background:var(--surface);border:1px solid var(--border);border-radius:13px;padding:4px;box-shadow:var(--shadow)}
.airtabs button{flex:1;border:none;background:transparent;color:var(--muted);font-weight:800;font-size:15px;padding:12px;border-radius:10px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:7px}
.airtabs button.on{background:var(--accent);color:#fff}
.airtabs .soon{font-size:10.5px;font-weight:800;background:var(--biz);color:#3a2600;padding:2px 7px;border-radius:6px}
.airtabs button.on .soon{background:rgba(255,255,255,.92)}
.ke-content.hide{display:none}
.ozwrap{display:none;background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:44px 24px;text-align:center;box-shadow:var(--shadow)}
.ozwrap.show{display:block}
.ozwrap .big{font-size:42px;margin-bottom:12px}
.ozwrap h3{margin:0 0 8px;font-size:19px;font-weight:800}
.ozwrap p{color:var(--muted);margin:0 auto;max-width:46ch;font-size:14px}
.ozwrap .dday{display:inline-block;margin-top:16px;background:color-mix(in srgb,var(--danger) 14%,transparent);color:var(--danger);font-weight:800;font-size:13px;padding:7px 15px;border-radius:999px}
@media(max-width:640px){.hero h1{font-size:22px}.wrap{padding:18px 12px 80px}.airtabs button{font-size:13.5px;padding:11px 6px}}
</style>
<div class="wrap">
 <div class="top">
  <div class="logo">✈️ <span>Mile<span class="m">Catch</span></span></div>
  <button class="themebtn" id="theme" title="테마 전환">◐</button>
 </div>

 <div class="hero">
  <div class="dday">🅿️ 인천공항주차예약 · 무료 마일리지 좌석 조회</div>
  <h1>대한항공 마일리지로<br>지금 갈 수 있는 곳을 한눈에</h1>
  <p>인천 출발 대한항공(KE) 어워드 좌석을 매일 자동 수집. 날짜·좌석 찾느라 헤매지 말고, 색칠된 달력에서 바로 고르세요.</p>
  <div class="picks">
   <button class="pick on" data-region="all">전체</button>
   <button class="pick" data-region="미국">🇺🇸 미주</button>
   <button class="pick" data-region="베트남">🇻🇳 동남아</button>
   <button class="pick" data-region="일본">🇯🇵 일본</button>
   <button class="pick" data-region="중국">🇨🇳 중국</button>
   <span class="bizonly" id="bizonly">💺 비즈니스만</span>
  </div>
 </div>

 <div class="airtabs">
  <button class="on" data-air="ke">✈️ 대한항공</button>
  <button data-air="oz">🅾️ 아시아나 <span class="soon">연말 오픈</span></button>
 </div>

 <div class="ke-content">
 <div class="bar">
  <div class="summary" id="summary"></div>
  <div class="spacer"></div>
  <div class="viewtog"><button class="on" data-view="cal">📅 달력</button><button data-view="list">☰ 목록</button></div>
  <button class="fbtn" id="fbtn">필터 ▾</button>
 </div>

 <div class="filters" id="filters">
  <span class="lab">좌석</span>
  <button class="chip on" data-cabin="all">전체</button>
  <button class="chip" data-cabin="e">이코노미</button>
  <button class="chip" data-cabin="b">비즈니스</button>
  <span class="lab" style="margin-left:8px">도시</span>
  <input id="q" type="text" placeholder="도쿄, LAX ...">
 </div>

 <div class="legend">
  <span class="it"><span class="sw" style="background:var(--biz)"></span>비즈니스 있음</span>
  <span class="it"><span class="sw" style="background:var(--eco)"></span>이코노미 있음</span>
  <span class="it"><span class="sw" style="background:var(--none)"></span>없음</span>
  <span class="it" style="margin-left:auto">칸을 누르면 공홈 예약으로 이동</span>
 </div>

 <div class="card">
  <div id="cal"></div>
  <div class="lwrap" id="lwrap"><table class="list"><thead><tr>
   <th>날짜</th><th>노선</th><th class="c">이코</th><th class="c">비즈</th><th class="r">마일(편도)</th><th></th>
  </tr></thead><tbody id="tb"></tbody></table></div>
  <div class="calhint show" id="calhint">💡 가로로 스크롤하면 다음 날짜가 보여요. 목적지는 왼쪽 고정.</div>
 </div>

 </div><!--/ke-content-->

 <div class="ozwrap" id="ozwrap">
  <div class="big">🅾️✈️</div>
  <h3>아시아나 좌석은 연말 오픈 준비 중</h3>
  <p>아시아나(OZ)는 실시간 크롤 연동을 마무리하고 있어요. 아시아나 마일리지 잔여석도 곧 이 탭에서 함께 보여드릴게요. 지금은 대한항공 탭에서 확인하세요.</p>
  <span class="dday">⏳ 아시아나 발권 마감 2026.12.16까지</span>
 </div>

 <div class="cta">
  <div class="ico">🅿️</div>
  <div class="t"><b>좌석 잡으셨나요? 인천공항 주차도 미리 예약하세요</b>
   <div>출국일 주차는 미리 예약이 제일 쌉니다. 마일 여행, 주차까지 편하게.</div></div>
  <a href="__PARK__" target="_blank" rel="noopener">인천공항 주차 예약 →</a>
 </div>
 <p class="foot"><b>안내</b> · 좌석은 매일 1회 갱신되는 참고용 정보이며 실시간 최종 좌석은 대한항공 공식 홈페이지·앱에서 확인하세요.
  마일 공제는 평수기 편도 참고값. 본 페이지는 대한항공과 무관한 비공식 정보 서비스입니다 · 데이터 __UPDATED__ 기준.</p>
</div>
<div id="tip"></div>
<script>
const DATA_KE=__DATA_KE__, DATA_OZ=__DATA_OZ__, BOOK=__BOOK__;
let DATA=DATA_KE, activeBook=BOOK;
const DOWk=["일","월","화","수","목","금","토"];
let f={region:"all",cabin:"all",biz:false,q:"",view:"cal"};

function pass(r){
 if(f.region!=="all"&&r.country!==f.region)return false;
 if(f.q){const q=f.q.toLowerCase();if(!(r.arr.toLowerCase().includes(q)||r.dest.toLowerCase().includes(q)))return false;}
 return true;
}
function cabinShow(r){ // what to show given cabin/biz filter -> 'b','e','eb',null
 const bizWanted=f.biz||f.cabin==="b", ecoWanted=f.cabin==="e";
 let e=r.e,b=r.b;
 if(bizWanted){e=false;} if(ecoWanted){b=false;}
 if(b&&e)return"eb"; if(b)return"b"; if(e)return"e"; return null;
}
function fmtMon(ym){const[y,m]=ym.split("-");return `${y}년 ${+m}월`;}

function renderCal(){
 const rows=DATA.filter(pass);
 // dest set (ordered) & month set
 const dmap={}, months=new Set();
 rows.forEach(r=>{months.add(r.date.slice(0,7));dmap[r.arr]=r;});
 const dests=[...new Set(rows.map(r=>r.arr))].sort((a,b)=>dmap[a].ord-dmap[b].ord||dmap[a].dest.localeCompare(dmap[b].dest));
 const look={}; rows.forEach(r=>look[r.arr+"|"+r.date]={e:r.e,b:r.b});
 const ms=[...months].sort();
 let html="";
 for(const ym of ms){
  const[y,mo]=ym.split("-").map(Number);
  const nd=new Date(y,mo,0).getDate();
  html+=`<div class="month"><div class="mname">${fmtMon(ym)}</div><div class="calwrap"><table class="cal"><thead><tr><th class="corner">목적지</th>`;
  for(let day=1;day<=nd;day++){const w=new Date(y,mo-1,day).getDay();
   html+=`<th class="dh${w===0||w===6?' we':''}">${day}<span class="dw">${DOWk[w]}</span></th>`;}
  html+=`</tr></thead><tbody>`;
  for(const dcode of dests){const meta=dmap[dcode];
   html+=`<tr class="mrow"><td class="rl"><span class="nm">${meta.dest}</span><span class="cd">ICN-${dcode}</span><span class="rg">${meta.region}</span></td>`;
   for(let day=1;day<=nd;day++){
    const iso=`${y}-${String(mo).padStart(2,"0")}-${String(day).padStart(2,"0")}`;
    const av=look[dcode+"|"+iso]; let cls="dot",tip="";
    if(av){
     let e=av.e,b=av.b; const bizW=f.biz||f.cabin==="b",ecoW=f.cabin==="e";
     if(bizW)e=false; if(ecoW)b=false;
     if(b&&e){cls+=" eb";} else if(b){cls+=" b";} else if(e){cls+=" e";}
     if(b||e){tip=`${meta.dest} ${mo}/${day} · ${e?'이코 ':''}${b?'비즈':''} 있음`;}
    }
    html+=`<td class="cell">${(av&&(cls!=="dot"))?`<span class="${cls}" data-tip="${tip}" data-book="1"></span>`:`<span class="dot"></span>`}</td>`;
   }
   html+=`</tr>`;
  }
  html+=`</tbody></table></div></div>`;
 }
 if(!dests.length)html=`<div style="padding:40px;text-align:center;color:var(--muted)">조건에 맞는 좌석이 없습니다.</div>`;
 document.getElementById("cal").innerHTML=html;
}
function renderList(){
 const rows=DATA.filter(r=>{if(!pass(r))return false;const s=cabinShow(r);return s!==null;})
   .sort((a,b)=>a.date.localeCompare(b.date)||a.ord-b.ord);
 document.getElementById("tb").innerHTML=rows.map(r=>{
  const w=DOWk[new Date(r.date+"T00:00:00").getDay()];const[,m,dd]=r.date.split("-");
  return `<tr><td><b>${+m}/${+dd}</b> <span style="color:var(--faint)">(${w})</span></td>
   <td><b>인천 → ${r.dest}</b> <span style="color:var(--faint);font-size:12px">ICN-${r.arr}</span></td>
   <td class="c"><span class="pill ${r.e?'e':'n'}">${r.e?'있음':'—'}</span></td>
   <td class="c"><span class="pill ${r.b?'b':'n'}">${r.b?'있음':'—'}</span></td>
   <td class="r"><span style="color:var(--muted);font-size:12.5px">이코 ${r.me.toLocaleString()}</span> · <b style="color:var(--biz)">비즈 ${r.mb.toLocaleString()}</b></td>
   <td><a class="book" href="${r.bk||activeBook}" target="_blank" rel="noopener">공홈 예약 ↗</a></td></tr>`;
 }).join("")||`<tr><td colspan="6" style="padding:40px;text-align:center;color:var(--muted)">조건에 맞는 좌석이 없습니다.</td></tr>`;
}
function summary(){
 const rows=DATA.filter(pass);
 const bizDests=new Set(rows.filter(r=>r.b).map(r=>r.arr));
 const bizDays=rows.filter(r=>r.b).length, ecoDays=rows.filter(r=>r.e).length;
 document.getElementById("summary").innerHTML=
  `지금 <span class="hl"><b>비즈니스</b>로 갈 수 있는 곳 ${bizDests.size}곳</span> · 비즈 <b>${bizDays}</b>일 · 이코 <b>${ecoDays}</b>일`;
}
function render(){summary();if(f.view==="cal")renderCal();else renderList();}

// events
document.querySelectorAll(".pick").forEach(p=>p.onclick=()=>{
 document.querySelectorAll(".pick").forEach(x=>x.classList.remove("on"));p.classList.add("on");f.region=p.dataset.region;render();});
document.getElementById("bizonly").onclick=function(){f.biz=!f.biz;this.classList.toggle("on",f.biz);render();};
document.querySelectorAll(".viewtog button").forEach(b=>b.onclick=()=>{
 document.querySelectorAll(".viewtog button").forEach(x=>x.classList.remove("on"));b.classList.add("on");f.view=b.dataset.view;
 document.getElementById("cal").style.display=f.view==="cal"?"":"none";
 document.getElementById("lwrap").classList.toggle("show",f.view==="list");
 document.getElementById("calhint").classList.toggle("show",f.view==="cal");
 render();});
document.getElementById("fbtn").onclick=function(){const el=document.getElementById("filters");el.classList.toggle("show");this.classList.toggle("on");};
document.querySelectorAll(".chip[data-cabin]").forEach(c=>c.onclick=()=>{
 document.querySelectorAll(".chip[data-cabin]").forEach(x=>x.classList.remove("on"));c.classList.add("on");f.cabin=c.dataset.cabin;render();});
document.getElementById("q").oninput=e=>{f.q=e.target.value;render();};
// tooltip + click-to-book (delegate)
const tip=document.getElementById("tip");
document.getElementById("cal").addEventListener("mousemove",e=>{
 const t=e.target.closest("[data-tip]");if(t&&t.dataset.tip){tip.textContent=t.dataset.tip;tip.style.opacity=1;
  tip.style.left=(e.clientX+12)+"px";tip.style.top=(e.clientY+12)+"px";}else tip.style.opacity=0;});
document.getElementById("cal").addEventListener("click",e=>{if(e.target.closest("[data-book]"))window.open(activeBook,"_blank");});
// theme
const root=document.documentElement;
document.getElementById("theme").onclick=()=>{const cur=root.getAttribute("data-theme")||(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light");root.setAttribute("data-theme",cur==="dark"?"light":"dark");};
if(DATA_OZ.length){const s=document.querySelector(".airtabs .soon");if(s)s.textContent="실시간";}
document.querySelectorAll(".airtabs button").forEach(t=>t.onclick=()=>{
 const oz=t.dataset.air==="oz";
 if(oz && !DATA_OZ.length){ // 데이터 없으면 준비중 안내
   document.querySelectorAll(".airtabs button").forEach(x=>x.classList.remove("on"));t.classList.add("on");
   document.querySelector(".ke-content").classList.add("hide");
   document.getElementById("ozwrap").classList.add("show"); return; }
 document.querySelectorAll(".airtabs button").forEach(x=>x.classList.remove("on"));t.classList.add("on");
 document.querySelector(".ke-content").classList.remove("hide");
 document.getElementById("ozwrap").classList.remove("show");
 DATA = oz?DATA_OZ:DATA_KE; activeBook = oz?"https://flyasiana.com/I/KR/KO/MileageSeatSearch.do":BOOK;
 f.region="all"; f.cabin="all"; f.biz=false; f.q="";
 document.querySelectorAll('.pick').forEach((p,i)=>p.classList.toggle('on',i===0));
 document.getElementById("bizonly").classList.remove("on");
 render();
});
render();
</script>
"""
html = (tpl.replace("__DATA_KE__", json.dumps(rows_ke, ensure_ascii=False))
           .replace("__DATA_OZ__", json.dumps(rows_oz, ensure_ascii=False))
           .replace("__BOOK__", json.dumps(BOOK))
           .replace("__PARK__", PARK)
           .replace("__UPDATED__", updated))
open("award_demo.html","w",encoding="utf-8").write(html)
print(f"v2 written. KE rows:{len(rows_ke)} OZ rows:{len(rows_oz)}")
