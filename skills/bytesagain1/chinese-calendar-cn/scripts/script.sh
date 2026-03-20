#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# Chinese Calendar (中文农历日历)
# Version 3.0.0
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
# ============================================================================

VERSION="3.0.0"
BRAND="Powered by BytesAgain | bytesagain.com | hello@bytesagain.com"
DATA_DIR="${HOME}/.local/share/chinese-calendar-cn"
LOG_FILE="${DATA_DIR}/calendar.log"

mkdir -p "$DATA_DIR"

log_entry() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

show_header() {
    echo "============================================"
    echo "  🏮 中文农历日历 v${VERSION}"
    echo "  ${BRAND}"
    echo "============================================"
    echo ""
}

# ── Lookup Tables ──

# 天干
TIANGAN=("甲" "乙" "丙" "丁" "戊" "己" "庚" "辛" "壬" "癸")
# 地支
DIZHI=("子" "丑" "寅" "卯" "辰" "巳" "午" "未" "申" "酉" "戌" "亥")
# 生肖
SHENGXIAO=("鼠" "牛" "虎" "兔" "龙" "蛇" "马" "羊" "猴" "鸡" "狗" "猪")
# 农历月份
LUNAR_MONTHS=("正月" "二月" "三月" "四月" "五月" "六月" "七月" "八月" "九月" "十月" "冬月" "腊月")
# 农历日期
LUNAR_DAYS=("初一" "初二" "初三" "初四" "初五" "初六" "初七" "初八" "初九" "初十"
            "十一" "十二" "十三" "十四" "十五" "十六" "十七" "十八" "十九" "二十"
            "廿一" "廿二" "廿三" "廿四" "廿五" "廿六" "廿七" "廿八" "廿九" "三十")

# 二十四节气
SOLAR_TERMS=(
    "小寒" "大寒" "立春" "雨水" "惊蛰" "春分"
    "清明" "谷雨" "立夏" "小满" "芒种" "夏至"
    "小暑" "大暑" "立秋" "处暑" "白露" "秋分"
    "寒露" "霜降" "立冬" "小雪" "大雪" "冬至"
)

# 节气对应的大致公历日期(月-日)
SOLAR_TERM_DATES=(
    "01-06" "01-20" "02-04" "02-19" "03-06" "03-21"
    "04-05" "04-20" "05-06" "05-21" "06-06" "06-21"
    "07-07" "07-23" "08-07" "08-23" "09-08" "09-23"
    "10-08" "10-23" "11-07" "11-22" "12-07" "12-22"
)

# 传统节日
declare -A FESTIVALS
FESTIVALS=(
    ["正月初一"]="🧨 春节（Spring Festival）"
    ["正月十五"]="🏮 元宵节（Lantern Festival）"
    ["二月初二"]="🐉 龙抬头（Dragon Head Raising）"
    ["三月初三"]="🌸 上巳节（Shangsi Festival）"
    ["五月初五"]="🐲 端午节（Dragon Boat Festival）"
    ["七月初七"]="💕 七夕节（Qixi Festival）"
    ["七月十五"]="👻 中元节（Ghost Festival）"
    ["八月十五"]="🥮 中秋节（Mid-Autumn Festival）"
    ["九月初九"]="🏔️ 重阳节（Double Ninth Festival）"
    ["十月初一"]="🕯️ 寒衣节（Cold Clothes Festival）"
    ["十月十五"]="🕯️ 下元节（Xiayuan Festival）"
    ["腊月初八"]="🥣 腊八节（Laba Festival）"
    ["腊月廿三"]="🧹 小年（Little New Year）"
    ["腊月三十"]="🎆 除夕（New Year's Eve）"
)

# Calculate 天干地支 for a year
calc_tiangan_dizhi() {
    local year="$1"
    local tg_idx=$(( (year - 4) % 10 ))
    local dz_idx=$(( (year - 4) % 12 ))
    echo "${TIANGAN[$tg_idx]}${DIZHI[$dz_idx]}"
}

# Calculate zodiac for a year
calc_zodiac() {
    local year="$1"
    local idx=$(( (year - 4) % 12 ))
    echo "${SHENGXIAO[$idx]}"
}

# Simple lunar date approximation
# (True lunar calendar requires astronomical data; this uses a simplified offset)
approx_lunar_date() {
    local solar_date="$1"  # YYYY-MM-DD
    local year month day
    year=$(date -d "$solar_date" '+%Y' 2>/dev/null || echo "${solar_date:0:4}")
    month=$(date -d "$solar_date" '+%-m' 2>/dev/null || echo "${solar_date:5:2}")
    day=$(date -d "$solar_date" '+%-d' 2>/dev/null || echo "${solar_date:8:2}")

    # Simplified: approximate lunar month is roughly solar month - 1, adjusted
    local lunar_month=$(( (month + 10) % 12 ))
    local lunar_day=$(( (day + 20) % 30 ))

    if (( lunar_month < 0 )); then lunar_month=0; fi
    if (( lunar_month > 11 )); then lunar_month=11; fi
    if (( lunar_day < 0 )); then lunar_day=0; fi
    if (( lunar_day > 29 )); then lunar_day=29; fi

    echo "${LUNAR_MONTHS[$lunar_month]}${LUNAR_DAYS[$lunar_day]}"
}

cmd_today() {
    show_header
    echo "▶ 今日信息"
    echo ""

    local today
    today=$(date '+%Y-%m-%d')
    local year month day weekday
    year=$(date '+%Y')
    month=$(date '+%-m')
    day=$(date '+%-d')
    weekday=$(date '+%A')

    # 星期中文
    local -A weekday_cn=(
        [Monday]="星期一" [Tuesday]="星期二" [Wednesday]="星期三"
        [Thursday]="星期四" [Friday]="星期五" [Saturday]="星期六" [Sunday]="星期日"
    )

    echo "  ── 公历 ──"
    echo "  日期：${today} ${weekday_cn[$weekday]:-$weekday}"
    echo "  年份：${year}年"
    echo ""

    echo "  ── 农历 ──"
    local ganzhi zodiac lunar_date
    ganzhi=$(calc_tiangan_dizhi "$year")
    zodiac=$(calc_zodiac "$year")
    lunar_date=$(approx_lunar_date "$today")
    echo "  年份：${ganzhi}年（${zodiac}年）"
    echo "  日期：${lunar_date}（近似）"
    echo ""

    echo "  ── 节气 ──"
    local found_term=0
    for (( i=0; i<24; i++ )); do
        local term_date="${year}-${SOLAR_TERM_DATES[$i]}"
        local term_epoch today_epoch
        term_epoch=$(date -d "$term_date" '+%s' 2>/dev/null || echo 0)
        today_epoch=$(date '+%s')
        local diff_days=$(( (term_epoch - today_epoch) / 86400 ))
        if (( diff_days >= 0 && diff_days <= 15 )); then
            if (( diff_days == 0 )); then
                echo "  🌿 今日节气：${SOLAR_TERMS[$i]}"
            else
                echo "  🌿 即将到来：${SOLAR_TERMS[$i]}（${diff_days}天后）"
            fi
            found_term=1
            break
        fi
    done
    if (( found_term == 0 )); then
        # Find the most recent solar term
        for (( i=23; i>=0; i-- )); do
            local term_date="${year}-${SOLAR_TERM_DATES[$i]}"
            local term_epoch today_epoch
            term_epoch=$(date -d "$term_date" '+%s' 2>/dev/null || echo 0)
            today_epoch=$(date '+%s')
            if (( term_epoch <= today_epoch )); then
                echo "  🌿 当前节气：${SOLAR_TERMS[$i]}"
                break
            fi
        done
    fi
    echo ""

    # Days until next major holiday (solar calendar approximation)
    echo "  ── 倒计时 ──"
    local new_year_epoch
    new_year_epoch=$(date -d "$((year+1))-01-01" '+%s' 2>/dev/null || echo 0)
    local now_epoch
    now_epoch=$(date '+%s')
    local days_to_ny=$(( (new_year_epoch - now_epoch) / 86400 ))
    echo "  距元旦：${days_to_ny}天"

    # National Day
    local nd_date="${year}-10-01"
    local nd_epoch
    nd_epoch=$(date -d "$nd_date" '+%s' 2>/dev/null || echo 0)
    local days_to_nd=$(( (nd_epoch - now_epoch) / 86400 ))
    if (( days_to_nd >= 0 )); then
        echo "  距国庆节：${days_to_nd}天"
    fi

    log_entry "TODAY"
}

cmd_convert() {
    local input_date="${1:?用法: chinese-calendar convert <YYYY-MM-DD>}"
    show_header
    echo "▶ 日期转换：${input_date}"
    echo ""

    # Validate date
    if ! date -d "$input_date" '+%Y-%m-%d' &>/dev/null; then
        echo "❌ 无效日期：${input_date}"
        echo "   格式：YYYY-MM-DD"
        return 1
    fi

    local year
    year=$(date -d "$input_date" '+%Y')
    local formatted
    formatted=$(date -d "$input_date" '+%Y年%m月%d日 %A')

    echo "  ── 公历 ──"
    echo "  ${formatted}"
    echo ""

    echo "  ── 天干地支 ──"
    local ganzhi
    ganzhi=$(calc_tiangan_dizhi "$year")
    echo "  ${ganzhi}年"
    echo ""

    echo "  ── 生肖 ──"
    local zodiac
    zodiac=$(calc_zodiac "$year")
    echo "  ${zodiac}年 🐾"
    echo ""

    echo "  ── 农历（近似） ──"
    local lunar
    lunar=$(approx_lunar_date "$input_date")
    echo "  ${lunar}"
    echo ""

    echo "  ── 节气 ──"
    local month_num
    month_num=$(date -d "$input_date" '+%-m')
    local si=$(( (month_num - 1) * 2 ))
    if (( si >= 0 && si < 24 )); then
        echo "  本月节气：${SOLAR_TERMS[$si]}、${SOLAR_TERMS[$(( si + 1 ))]}"
    fi

    log_entry "CONVERT date=${input_date}"
}

cmd_festival() {
    local year="${1:?用法: chinese-calendar festival <year>}"
    show_header
    echo "▶ ${year}年传统节日"
    echo ""

    echo "  ── 农历节日 ──"
    for key in "正月初一" "正月十五" "二月初二" "三月初三" "五月初五" "七月初七" "七月十五" "八月十五" "九月初九" "十月初一" "腊月初八" "腊月廿三" "腊月三十"; do
        local desc="${FESTIVALS[$key]:-}"
        if [[ -n "$desc" ]]; then
            printf "  %-12s  %s\n" "$key" "$desc"
        fi
    done

    echo ""
    echo "  ── 公历节日 ──"
    echo "  01-01  🎆 元旦（New Year's Day）"
    echo "  02-14  💝 情人节（Valentine's Day）"
    echo "  03-08  🌷 妇女节（Women's Day）"
    echo "  04-01  🤡 愚人节（April Fools' Day）"
    echo "  05-01  ⚒️  劳动节（Labour Day）"
    echo "  05-04  🏃 青年节（Youth Day）"
    echo "  06-01  🧒 儿童节（Children's Day）"
    echo "  07-01  🎗️ 建党节（Party Anniversary）"
    echo "  08-01  🎖️ 建军节（Army Day）"
    echo "  09-10  📚 教师节（Teachers' Day）"
    echo "  10-01  🇨🇳 国庆节（National Day）"
    echo "  12-25  🎄 圣诞节（Christmas）"

    log_entry "FESTIVAL year=${year}"
}

cmd_zodiac() {
    local year="${1:?用法: chinese-calendar zodiac <year>}"
    show_header
    echo "▶ ${year}年生肖信息"
    echo ""

    local zodiac ganzhi
    zodiac=$(calc_zodiac "$year")
    ganzhi=$(calc_tiangan_dizhi "$year")

    echo "  年份：${year}"
    echo "  天干地支：${ganzhi}"
    echo "  生肖：${zodiac}"
    echo ""

    echo "  ── 十二生肖速查 ──"
    echo ""
    for (( i=0; i<12; i++ )); do
        local sample_year=$(( year - ( (year - 4) % 12 ) + i ))
        local emoji
        case "${SHENGXIAO[$i]}" in
            "鼠") emoji="🐭" ;; "牛") emoji="🐮" ;; "虎") emoji="🐯" ;;
            "兔") emoji="🐰" ;; "龙") emoji="🐲" ;; "蛇") emoji="🐍" ;;
            "马") emoji="🐴" ;; "羊") emoji="🐑" ;; "猴") emoji="🐵" ;;
            "鸡") emoji="🐔" ;; "狗") emoji="🐕" ;; "猪") emoji="🐷" ;;
            *) emoji="  " ;;
        esac
        local marker=""
        if [[ "${SHENGXIAO[$i]}" == "$zodiac" ]]; then
            marker=" ← ${year}年"
        fi
        printf "  %s %s  最近年份：%s、%s、%s%s\n" \
            "$emoji" "${SHENGXIAO[$i]}" \
            "$(( sample_year - 12 ))" "$sample_year" "$(( sample_year + 12 ))" \
            "$marker"
    done

    log_entry "ZODIAC year=${year}"
}

cmd_solar_term() {
    local month="${1:?用法: chinese-calendar solar-term <month>}"
    show_header
    echo "▶ ${month}月节气"
    echo ""

    if ! [[ "$month" =~ ^[0-9]+$ ]] || (( month < 1 || month > 12 )); then
        echo "❌ 月份无效：${month}（范围 1-12）"
        return 1
    fi

    local si=$(( (month - 1) * 2 ))
    local year
    year=$(date '+%Y')

    echo "  ── ${month}月的两个节气 ──"
    echo ""

    for offset in 0 1; do
        local idx=$(( si + offset ))
        local term="${SOLAR_TERMS[$idx]}"
        local term_date="${year}-${SOLAR_TERM_DATES[$idx]}"
        local formatted
        formatted=$(date -d "$term_date" '+%Y年%m月%d日' 2>/dev/null || echo "$term_date")

        echo "  🌿 ${term}"
        echo "     大约日期：${formatted}"
        echo ""

        # Term descriptions
        case "$term" in
            "立春") echo "     含义：春季开始" ;;
            "雨水") echo "     含义：降雨开始增多" ;;
            "惊蛰") echo "     含义：春雷惊醒蛰伏动物" ;;
            "春分") echo "     含义：昼夜等分" ;;
            "清明") echo "     含义：天清气明" ;;
            "谷雨") echo "     含义：雨生百谷" ;;
            "立夏") echo "     含义：夏季开始" ;;
            "小满") echo "     含义：麦类作物开始饱满" ;;
            "芒种") echo "     含义：有芒作物成熟" ;;
            "夏至") echo "     含义：白昼最长" ;;
            "小暑") echo "     含义：天气开始炎热" ;;
            "大暑") echo "     含义：一年最热" ;;
            "立秋") echo "     含义：秋季开始" ;;
            "处暑") echo "     含义：暑气消退" ;;
            "白露") echo "     含义：露珠凝白" ;;
            "秋分") echo "     含义：昼夜再次等分" ;;
            "寒露") echo "     含义：露水寒冷" ;;
            "霜降") echo "     含义：开始降霜" ;;
            "立冬") echo "     含义：冬季开始" ;;
            "小雪") echo "     含义：开始降雪" ;;
            "大雪") echo "     含义：大量降雪" ;;
            "冬至") echo "     含义：白昼最短" ;;
            "小寒") echo "     含义：天气渐冷" ;;
            "大寒") echo "     含义：一年最冷" ;;
        esac
        echo ""
    done

    log_entry "SOLAR-TERM month=${month}"
}

cmd_lunar() {
    local input_date="${1:?用法: chinese-calendar lunar <YYYY-MM-DD>}"
    show_header
    echo "▶ 农历信息：${input_date}"
    echo ""

    if ! date -d "$input_date" '+%Y-%m-%d' &>/dev/null; then
        echo "❌ 无效日期：${input_date}"
        return 1
    fi

    local year
    year=$(date -d "$input_date" '+%Y')
    local lunar_date ganzhi zodiac
    lunar_date=$(approx_lunar_date "$input_date")
    ganzhi=$(calc_tiangan_dizhi "$year")
    zodiac=$(calc_zodiac "$year")

    echo "  公历：$(date -d "$input_date" '+%Y年%m月%d日')"
    echo "  农历：${ganzhi}年 ${lunar_date}（近似）"
    echo "  生肖：${zodiac}"
    echo ""

    echo "  ── 干支纪年详解 ──"
    local tg_idx=$(( (year - 4) % 10 ))
    local dz_idx=$(( (year - 4) % 12 ))
    echo "  天干：${TIANGAN[$tg_idx]}（第$((tg_idx+1))位）"
    echo "  地支：${DIZHI[$dz_idx]}（第$((dz_idx+1))位）"
    echo ""

    echo "  ── 五行 ──"
    local wuxing
    case $(( tg_idx / 2 )) in
        0) wuxing="木（Wood）" ;;
        1) wuxing="火（Fire）" ;;
        2) wuxing="土（Earth）" ;;
        3) wuxing="金（Metal）" ;;
        4) wuxing="水（Water）" ;;
    esac
    echo "  五行属性：${wuxing}"

    echo ""
    echo "  注：农历日期为近似计算，精确日期需查阅历书。"

    log_entry "LUNAR date=${input_date}"
}

cmd_help() {
    show_header
    cat <<EOF
用法: chinese-calendar <command> [arguments]

命令:
  today                 今日农历信息
  convert <YYYY-MM-DD>  日期转换（公历→农历）
  festival <year>       查看年度节日列表
  zodiac <year>         查看生肖信息
  solar-term <month>    查看月份节气
  lunar <YYYY-MM-DD>    详细农历信息
  help                  显示帮助

数据目录: ${DATA_DIR}
EOF
}

main() {
    local cmd="${1:-help}"
    shift || true

    case "$cmd" in
        today)       cmd_today ;;
        convert)     cmd_convert "$@" ;;
        festival)    cmd_festival "$@" ;;
        zodiac)      cmd_zodiac "$@" ;;
        solar-term)  cmd_solar_term "$@" ;;
        lunar)       cmd_lunar "$@" ;;
        help|--help|-h) cmd_help ;;
        *)
            echo "未知命令: ${cmd}"
            cmd_help
            exit 1
            ;;
    esac
}

main "$@"
