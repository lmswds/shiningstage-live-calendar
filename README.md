# 小心思的直播日程日历订阅

通过 GitHub Actions 自动抓取 [闪耀舞台 粉丝导航站](https://fionagladys.com/) 的直播日程数据，生成 ICS 日历文件，支持任意日历应用（如 Google Calendar、Apple 日历等）订阅同步。

## 订阅地址

#### 来自闪耀舞台
| 主播 | 订阅链接 |
|------|--------|
| 心宜 | `https://raw.githubusercontent.com/lmswds/shiningstage-live-calendar/main/ics_files/fiona.ics` |
| 思诺 | `https://raw.githubusercontent.com/lmswds/shiningstage-live-calendar/main/ics_files/gladys.ics` |

#### 枝江站自带
| 主播 | 订阅链接 |
|------|--------|
| 心宜 | `https://asoul.love/calendar.ics?include=fiona` |
| 思诺 | `https://asoul.love/calendar.ics?include=gladys` |
| 合并 | `https://asoul.love/calendar.ics?include=gladys,fiona` |

**使用方式**：复制对应链接，在日历应用中选择“通过 URL 添加日历”即可。

## 自动化流程

本仓库基于 GitHub Actions 每日自动运行，流程如下：
1. 从 `https://fionagladys.com/schedule` 获取最新直播安排
2. 解析并转换为标准 ICS 格式
3. 推送更新到 `ics_files/` 目录

代码由 Gemini 全权生成。

## 🙏 特别感谢

[Xlaka 老师](https://space.bilibili.com/2316873) ， [闪耀舞台 粉丝导航站](https://fionagladys.com/)以及[枝江站](https://asoul.love/calendar/latest)


**如有任何不妥，请联系我进行删除**
