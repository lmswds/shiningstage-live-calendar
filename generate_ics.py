import re
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from ics import Calendar, Event
import pytz

def fetch_and_generate_ics():
    url = 'https://fionagladys.com/schedule'
    
    # 使用 playwright 模拟真实浏览器，等待 JavaScript 渲染完成
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        try:
            # 等待包含月份的日历标签加载出来（最长等待15秒）
            page.wait_for_selector('#calendar-month-label', timeout=15000)
        except Exception as e:
            print("页面加载超时，未找到日历节点。这可能是网络原因或页面结构已更改。")
            browser.close()
            return
            
        html_content = page.content()
        browser.close()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 获取当前日历的年份和月份
    month_label_elem = soup.find(id='calendar-month-label')
    if not month_label_elem:
        print("未能解析到月份元素。")
        return
    
    month_label = month_label_elem.text.strip()
    match = re.search(r'(\d+)年(\d+)月', month_label)
    if not match:
        print("无法解析年月信息")
        return

    year = int(match.group(1))
    month = int(match.group(2))
    
    cal_fiona = Calendar()
    cal_gladys = Calendar()
    
    # 设定为中国标准时间
    tz = pytz.timezone('Asia/Shanghai')
    
    # 遍历所有有事件的日期单元格
    for cell in soup.select('.cal-overview.has-events'):
        day_str = cell.find(class_='cal-day').text.strip()
        if not day_str.isdigit():
            continue
        day = int(day_str)
        
        # 遍历该日期下的每一个具体直播安排
        for item in cell.select('.summary-item'):
            time_str = item.find(class_='summary-time').text.strip()
            title = item.find(class_='summary-title').text.strip()
            room = item.find(class_='summary-room').text.strip()
            
            hour, minute = map(int, time_str.split(':'))
            
            # 创建带时区信息的时间对象
            dt_start = tz.localize(datetime(year, month, day, hour, minute))
            
            event = Event()
            event.name = title
            event.begin = dt_start
            # 假设默认直播时长为 2 小时
            event.end = dt_start + timedelta(hours=2)
            
            # 根据 class 判断是哪位艺人的行程
            if 'room-fiona' in item.get('class', []):
                event.description = f"直播间: {room}\n直播间地址: https://live.bilibili.com/30849777"
                cal_fiona.events.add(event)
            elif 'room-gladys' in item.get('class', []):
                event.description = f"直播间: {room}\n直播间地址: https://live.bilibili.com/30858592"
                cal_gladys.events.add(event)
                
    # 对 Fiona 的日程事件进行排序
    cal_fiona.events = sorted(cal_fiona.events, key=lambda e: e.begin)
    # 对 Gladys 的日程事件进行排序
    cal_gladys.events = sorted(cal_gladys.events, key=lambda e: e.begin)
    # 导出为 ics 文件
    fiona_lines = list(cal_fiona.serialize_iter())
    fiona_lines.insert(1, "X-WR-CALNAME:心宜的直播日程\n")
    with open('ics_files/fiona.ics', 'w', encoding='utf-8') as f:
        f.writelines(fiona_lines)
        
    gladys_lines = list(cal_gladys.serialize_iter())
    gladys_lines.insert(1, "X-WR-CALNAME:思诺的直播日程\n")
    with open('ics_files/gladys.ics', 'w', encoding='utf-8') as f:
        f.writelines(gladys_lines)

if __name__ == '__main__':
    fetch_and_generate_ics()
