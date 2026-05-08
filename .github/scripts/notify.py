#!/usr/bin/env python3
"""SIE Exam Tracker — Feishu Notification Script
Usage: python notify.py <type> <supabase_key>
Types: daily-reminder | missed-checkin | weekly-report | behind-alert
"""
import sys
import json
import requests
from datetime import date, timedelta

# ── CONFIG ──────────────────────────────────────────────
SUPABASE_URL   = 'https://cupdvksfzqpjedibajus.supabase.co'
SUPABASE_KEY   = sys.argv[2] if len(sys.argv) > 2 else ''
SITE_URL       = 'https://jean-jia.github.io/sie-tracker/'
TRACKING_START = date(2026, 5, 8)
TOTAL_CHAPTERS = 20
TODAY          = date.today()
DRY_RUN        = '--dry-run' in sys.argv

USERS = {
    'jiannbinkhor': {'name':'Jiannbin Khor', 'startChapter':11, 'examDate':date(2026,6,5),  'weeklyHours':11.5, 'studyStart':date(2026,4,6)},
    'nicholasneoh': {'name':'Nicholas Neoh', 'startChapter':1,  'examDate':date(2026,7,5),  'weeklyHours':5,    'studyStart':date(2026,4,13)},
    'daisywang':    {'name':'Daisy Wang',    'startChapter':5,  'examDate':date(2026,6,25), 'weeklyHours':6,    'studyStart':date(2026,4,10)},
    'cindylin':     {'name':'Cindy Lin',     'startChapter':0,  'examDate':date(2026,7,5),  'weeklyHours':5,    'studyStart':date(2026,4,6)},
    'suqinng':      {'name':'Su Qin Ng',     'startChapter':0,  'examDate':date(2026,6,15), 'weeklyHours':9,    'studyStart':date(2026,4,20)},
    'jeremyzhang':  {'name':'Jeremy Zhang',  'startChapter':0,  'examDate':date(2026,6,15), 'weeklyHours':9,    'studyStart':date(2026,4,30)},
}

QUOTES = [
    "The secret of getting ahead is getting started.",
    "不是因为有希望才坚持，而是坚持了才会有希望。",
    "Small daily improvements lead to staggering long-term results.",
    "你现在的努力，是在为未来的自己铺路。",
    "It does not matter how slowly you go as long as you do not stop.",
    "每天进步一点点，考试就近了一点点。",
    "Success is the sum of small efforts repeated day in and day out.",
    "坚持不是因为相信结果，而是因为相信自己。",
    "Don't watch the clock; do what it does. Keep going.",
    "今天的你，正在成为未来更好的自己。",
    "The pain you feel today will be the strength you feel tomorrow.",
    "坚持下去，不是因为路的尽头有什么，而是走着走着就成了习惯。",
    "Fall seven times, stand up eight.",
    "没有捷径，只有脚踏实地。",
    "A river cuts through rock not because of its power, but its persistence.",
    "种一棵树最好的时间是十年前，其次是现在。",
    "One step at a time is good walking.",
    "慢慢来，比较快。",
    "Perseverance is not a long race; it is many short races one after another.",
    "坚持是一种习惯，也是一种态度。",
    "The harder you work, the luckier you get.",
    "距离终点越近，越不能放慢脚步。",
    "Push yourself, because no one else is going to do it for you.",
    "考试只是一个节点，你的努力才是真正的收获。",
    "Believe you can and you're halfway there.",
    "冲刺阶段最考验意志，也最能看出差距。",
    "You didn't come this far to only come this far.",
    "最后的坚持，往往是成功的开始。",
    "Champions keep playing until they get it right.",
    "不要让昨天的懈怠，成为今天的借口。",
    "Pressure makes diamonds.",
    "压力就是动力，挑战就是机遇。",
    "The last mile is always the hardest.",
    "越到最后越要稳住，胜负就在这里。",
    "Sprint, not stumble — the finish line is close.",
    "临考前的每一天，都是你拉开差距的机会。",
    "It always seems impossible until it's done.",
    "还没到最后一刻，就不要轻言放弃。",
    "The night is darkest just before the dawn.",
    "黎明前最黑暗，坚持就是胜利。",
    "Doubt kills more dreams than failure ever will.",
    "你比你想象的更有能力。",
    "The only person you should try to be better than is who you were yesterday.",
    "成功不是偶然的，它是日积月累的结果。",
    "Wake up with determination. Go to bed with satisfaction.",
    "每一次打开书本，都是对自己的一次投资。",
    "Your future self will thank you for what you do today.",
    "现在吃的苦，都会变成你的实力。",
    "Excellence is not a destination but a continuous journey.",
    "做到了才有资格说做不到，还没做就别放弃。",
    "You are stronger than you think.",
    "你比昨天的自己更强了，这就够了。",
    "Motivation gets you started. Habit keeps you going.",
    "自律是最高级的自由。",
    "The difference between ordinary and extraordinary is that little extra.",
    "普通人和优秀的人之间，差的就是每天多做一点。",
    "Hard work beats talent when talent doesn't work hard.",
    "努力不一定成功，但放弃一定失败。",
    "Every expert was once a beginner.",
    "每个高手都曾是初学者，你也一样。",
    "Coffee in hand, notes open, let's go! ☕",
    "学习使我快乐，不学习使我更快乐，但考试使我清醒。",
    "Studying now so you can flex later. 💪",
    "考过了就可以跟朋友吹牛了，加油！",
    "Your brain has more capacity than your phone. Use it.",
    "今天学的东西，明天就是你的竞争优势。",
    "Be the person your future self is proud of.",
    "考试不可怕，可怕的是没准备好。",
    "Study hard, flex harder.",
    "刷题一时爽，过关才是真的爽——所以现在就好好学！",
    "My brain is 90% finance facts and 10% song lyrics. Priorities. 🎵",
    "学习虽苦，但通过考试的那一刻是甜的。",
    "SIE won't study itself. Unfortunately.",
    "证书不会自己长脚跑来，但努力会。",
    "Plot twist: you actually enjoy studying. 📖",
    "打卡一分钟，良心安一天。",
    "Brain cells activated. Let's go! 🧠",
    "今天不想学，那就学一点。",
    "Sleep is good. Study is better. Passing is best.",
    "睡得好不如学得好，学得好不如考得好。",
    "Invest in your knowledge — the returns are guaranteed.",
    "知识是唯一一种投资，回报率永远是正的。",
    "In the market of life, education is the best asset.",
    "学好SIE，就是给自己最好的职业投资。",
    "The best investment you can make is in yourself. — Warren Buffett",
    "你的证书，就是你最硬核的简历。",
    "Risk comes from not knowing what you're doing. — Warren Buffett",
    "考出来的不只是证书，是对自己的证明。",
    "Financial knowledge is the foundation of financial freedom.",
    "今天多学一章，未来多一份底气。",
    "In investing, what is comfortable is rarely profitable.",
    "走出舒适区，才能看到更大的市场。",
    "The stock market rewards patience, so does studying.",
    "备考就像建立投资组合：每天积累，长期复利。",
    "Know what you own, and know why you own it. — Peter Lynch",
    "搞清楚每一个知识点，就是最好的备考策略。",
    "Compound interest is the eighth wonder of the world. — Einstein",
    "学习也有复利效应：今天多学一章，明天事半功倍。",
    "The four most dangerous words: 'this time it's different.'",
    "考试没有捷径，只有扎实准备。",
]

# ── SUPABASE ─────────────────────────────────────────────
def sb_get(table, params=''):
    headers = {'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}
    url = f'{SUPABASE_URL}/rest/v1/{table}'
    if params:
        url += f'?{params}'
    return requests.get(url, headers=headers).json()

# ── CALCULATIONS ─────────────────────────────────────────
def fmt_date(d):
    return f'{d.month}月{d.day}日'

def days_between(d1, d2):
    return (d2 - d1).days

def planned_chapters_today(username):
    u = USERS[username]
    total_days = days_between(u['studyStart'], u['examDate'])
    if total_days <= 0:
        return TOTAL_CHAPTERS
    elapsed = max(0, days_between(u['studyStart'], TODAY))
    return min(TOTAL_CHAPTERS, (elapsed / total_days) * TOTAL_CHAPTERS)

def get_status(gap):
    if gap is None or gap >= -0.3:
        return ('🟢', 'On Track')
    if gap >= -2:
        return ('🟡', 'At Risk')
    return ('🔴', 'Off Track')

def get_quote():
    idx = days_between(date(2026, 1, 1), TODAY)
    return QUOTES[idx % len(QUOTES)]

# ── FEISHU ───────────────────────────────────────────────
def build_card(title, color, content, btn_label, btn_url):
    return {
        'msg_type': 'interactive',
        'card': {
            'config': {'wide_screen_mode': True},
            'header': {'title': {'tag': 'plain_text', 'content': title}, 'template': color},
            'elements': [
                {'tag': 'div', 'text': {'tag': 'lark_md', 'content': content}},
                {'tag': 'action', 'actions': [{
                    'tag': 'button',
                    'text': {'tag': 'plain_text', 'content': btn_label},
                    'type': 'primary', 'url': btn_url
                }]}
            ]
        }
    }

def send_feishu(url, payload):
    import json as _json
    content = payload.get('card', {}).get('elements', [{}])[0].get('text', {}).get('content', '')
    print(f'  Message preview:\n{content}\n')
    if DRY_RUN:
        print('  [DRY RUN] Skipping Feishu send.')
        return True
    r = requests.post(url, json=payload)
    print(f'  Feishu response: {r.text}')
    return r.ok

# ── MAIN ─────────────────────────────────────────────────
def main():
    ntype = sys.argv[1] if len(sys.argv) > 1 else 'daily-reminder'
    print(f'Running: {ntype} | Today: {TODAY}')

    # Load data
    prog_data = sb_get('chapter_progress')
    ci_data   = sb_get('checkins')
    wh_data   = sb_get('webhook_config', 'id=eq.1')

    webhook_url = wh_data[0]['group_webhook'] if wh_data else ''
    if not webhook_url and not DRY_RUN:
        print('ERROR: No group webhook configured in Supabase webhook_config')
        sys.exit(1)

    # Build per-user data
    users_data = {}
    for username in USERS:
        prog = next((p for p in prog_data if p['username'] == username), None)
        completed = prog['completed_chapters'] if prog else list(range(1, USERS[username]['startChapter']+1))
        checkins = {c['date']: c for c in ci_data if c['username'] == username}
        users_data[username] = {'completed': completed, 'checkins': checkins}

    def stats(username):
        d = users_data[username]
        actual  = len(d['completed'])
        planned = planned_chapters_today(username)
        gap     = actual - planned
        left    = days_between(TODAY, USERS[username]['examDate'])
        today_ci = d['checkins'].get(str(TODAY))
        # Consecutive missed days
        missed, cursor = 0, TODAY
        while str(cursor) not in d['checkins'] and cursor >= TRACKING_START:
            missed += 1
            cursor -= timedelta(days=1)
            if missed > 30: break
        return {'actual':actual, 'gap':gap, 'left':left, 'today_ci':today_ci, 'missed':missed}

    if DRY_RUN:
        print('─── Stats ───')
        for u in USERS:
            s = stats(u)
            st_icon, st_label = get_status(s['gap'])
            print(f"  {USERS[u]['name']:20s} actual={s['actual']:2d} planned={planned_chapters_today(u):.1f} gap={s['gap']:+.1f} {st_icon}{st_label}  study_start={USERS[u]['studyStart']}")
        print('─────────────')

    quote    = get_quote()
    today_str = fmt_date(TODAY)
    medals   = ['🥇','🥈','🥉']

    # ── Daily reminder ──
    if ntype == 'daily-reminder':
        ranked = sorted(USERS.keys(), key=lambda u: stats(u)['gap'], reverse=True)
        lines = [f'"{quote}"', '', '<at id=all></at> 今日学习任务来了，冲！💪', '',
                 '━━━━━━━━━━━━━━━', '🏆 进度排行榜', '━━━━━━━━━━━━━━━']
        for i, u in enumerate(ranked):
            s = stats(u)
            st_icon, st_label = get_status(s['gap'])
            row_icon = medals[i] if st_label == 'On Track' and i < 3 else ('⚠️' if st_label == 'At Risk' else '❌')
            gap_str = f"领先{s['gap']:.1f}章" if s['gap'] >= 0 else f"落后{abs(s['gap']):.1f}章"
            lines.append(f"{row_icon} **{USERS[u]['name']}**  {s['actual']}/{TOTAL_CHAPTERS}章  {st_icon} {st_label} · {gap_str} · 剩{s['left']}天")
        lines += ['━━━━━━━━━━━━━━━', '今日目标：完成打卡 ✅']
        card = build_card(f'📚 SIE备考提醒 · {today_str}', 'blue', '\n'.join(lines), '📎 打开备考工具 →', SITE_URL)
        send_feishu(webhook_url, card)

    # ── Missed check-in ──
    elif ntype == 'missed-checkin':
        yesterday = str(TODAY - timedelta(days=1))
        missed = [u for u in USERS if yesterday not in users_data[u]['checkins']]
        if not missed:
            print('Everyone checked in yesterday ✓')
            return
        names = '、'.join(f'**{USERS[u]["name"]}**' for u in missed)
        content = f'<at id=all></at>\n\n昨天（{fmt_date(TODAY - timedelta(days=1))}）以下同学没有打卡记录：\n{names}\n\n今天记得补上学习进度！加油 💪'
        card = build_card('⚠️ 昨日未打卡提醒', 'yellow', content, '📎 去打卡 →', SITE_URL)
        send_feishu(webhook_url, card)

    # ── Weekly report ──
    elif ntype == 'weekly-report':
        ranked = sorted(USERS.keys(), key=lambda u: stats(u)['gap'], reverse=True)
        on_track  = [u for u in ranked if get_status(stats(u)['gap'])[1] == 'On Track']
        at_risk   = [u for u in ranked if get_status(stats(u)['gap'])[1] == 'At Risk']
        off_track = [u for u in ranked if get_status(stats(u)['gap'])[1] == 'Off Track']
        lines = [f'"{quote}"', '']
        def row(u, icon):
            s = stats(u)
            gap_str = f"领先{s['gap']:.1f}章" if s['gap'] >= 0 else f"落后{abs(s['gap']):.1f}章"
            return f"{icon} **{USERS[u]['name']}** · {s['actual']}/{TOTAL_CHAPTERS}章 · {gap_str} · 剩{s['left']}天"
        if on_track:
            lines.append('🟢 **On Track**')
            for i, u in enumerate(on_track): lines.append(row(u, medals[i] if i < 3 else '🟢'))
            lines.append('')
        if at_risk:
            lines.append('🟡 **At Risk**')
            for u in at_risk: lines.append(row(u, '⚠️'))
            lines.append('')
        if off_track:
            lines.append('🔴 **Off Track**')
            for u in off_track: lines.append(row(u, '❌'))
            lines.append('')
        if at_risk or off_track:
            lines.append('💡 落后的同学加油，考试不等人！')
        card = build_card(f'📊 SIE考牌项目 · 本周进度播报 · {today_str}', 'green', '\n'.join(lines), '📎 打开备考工具 →', SITE_URL)
        send_feishu(webhook_url, card)

    # ── Behind alert ──
    elif ntype == 'behind-alert':
        behind = [(u, stats(u)) for u in USERS if stats(u)['missed'] >= 3]
        if not behind:
            print('No one is 3+ days behind ✓')
            return
        blocks = []
        for u, s in behind:
            gap_str = f"落后计划{abs(s['gap']):.1f}章" if s['gap'] < 0 else "进度正常"
            blocks.append(
                f"👋 **{USERS[u]['name']}**，你已经连续 **{s['missed']}天** 没有打卡了\n"
                f"📊 当前进度：{s['actual']}/{TOTAL_CHAPTERS}章，{gap_str}\n"
                f"⏰ 距考试还有 {s['left']} 天\n"
                f"现在开始还来得及，今天学一章就是进步！"
            )
        content = '<at id=all></at>\n\n' + '\n\n─────────────────\n\n'.join(blocks)
        card = build_card('⚠️ 备考进度催促', 'red', content, '📎 打开备考工具 →', SITE_URL)
        send_feishu(webhook_url, card)

if __name__ == '__main__':
    main()
