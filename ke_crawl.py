# -*- coding: utf-8 -*-
"""대한항공 마일리지 보너스 좌석 '날짜별 있다/없다' 미니 크롤러 (프로토타입).
좌석수 X, 그날 이코(e)/비즈(b) 가능여부만. 예약은 공홈 딥링크로.
"""
import json, time, sys, datetime as dt
from curl_cffi import requests as cr

EP = "https://www.koreanair.com/api/hmp/bonusSeatView/bonusSeatView"
BOOK = "https://www.koreanair.com/booking/book-and-manage/award-seat-availability"
HDR = {"Content-Type": "application/json", "channel": "pc", "Referer": BOOK}

# 대한항공 인천 취항지(4개국) — 유한/고정. 풀 노선.
ROUTES = {
    "일본":   {"NRT":"도쿄/나리타","HND":"도쿄/하네다","KIX":"오사카","FUK":"후쿠오카",
               "CTS":"삿포로","OKA":"오키나와","NGO":"나고야"},
    "베트남": {"SGN":"호치민","HAN":"하노이","DAD":"다낭","CXR":"나트랑","PQC":"푸꾸옥"},
    "중국":   {"PEK":"베이징","PVG":"상하이","CAN":"광저우","TAO":"칭다오","SHE":"선양","DLC":"다롄"},
    "미국":   {"LAX":"로스앤젤레스","JFK":"뉴욕","SFO":"샌프란시스코","SEA":"시애틀",
               "ATL":"애틀랜타","ORD":"시카고","DFW":"댈러스","LAS":"라스베이거스",
               "HNL":"호놀룰루","BOS":"보스턴","IAD":"워싱턴"},
}

def month_anchors(n=2):
    d = dt.date.today().replace(day=1)
    out=[]
    for _ in range(n):
        out.append(d.isoformat())
        d = (d.replace(day=28) + dt.timedelta(days=7)).replace(day=1)
    return out

def new_session():
    s = cr.Session(impersonate="chrome")
    s.get("https://www.koreanair.com/", timeout=25)
    s.get(BOOK, timeout=25)
    return s

def fetch_month(s, dep, arr, anchor):
    r = s.post(EP, data=json.dumps({"departureDate":anchor,"departureAirport":dep,"arrivalAirport":arr}),
               headers=HDR, timeout=30)
    r.raise_for_status()
    return r.json().get("flightList", [])

def main():
    s = new_session()
    anchors = month_anchors(6)  # 현재월~연말
    result = {"updated": dt.datetime.now().isoformat(timespec="seconds"),
              "note": "e=이코노미(일반석)/b=비즈니스(프레스티지) 보너스좌석 있음 여부. 실시간 최종은 공홈 확인. 대한항공 비공식.",
              "routes": {}}
    for country, dests in ROUTES.items():
        for arr, name in dests.items():
            key = f"ICN-{arr}"
            dates = {}
            for anc in anchors:
                try:
                    fl = fetch_month(s, "ICN", arr, anc)
                except Exception as e:
                    print(f"  ! {key} {anc} err {e}", file=sys.stderr); continue
                for day in fl:
                    d = day.get("departureDate")  # YYYYMMDD
                    e=b=False
                    for f in day.get("flightDetailList", []):
                        if not f.get("availableSeat"): continue
                        fc = f.get("frontBookingClass")
                        if fc=="E": e=True
                        elif fc in ("P","U","F"): b=True
                    if e or b:
                        iso=f"{d[:4]}-{d[4:6]}-{d[6:]}"
                        dates[iso]={"e":e,"b":b}
                time.sleep(2)
            ecnt=sum(1 for v in dates.values() if v["e"])
            bcnt=sum(1 for v in dates.values() if v["b"])
            result["routes"][key]={"country":country,"dest":name,
                "book_url":f"{BOOK}?dep=ICN&arr={arr}",
                "days_with_any":len(dates),"days_econ":ecnt,"days_biz":bcnt,"dates":dates}
            print(f"{country:5} {key} {name:10} : 이코 {ecnt}일 / 비즈 {bcnt}일 (조회 {len(anchors)}개월)")
    with open("seats.json","w",encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"\n-> seats.json 저장 ({len(result['routes'])} 노선)")

if __name__=="__main__":
    main()
