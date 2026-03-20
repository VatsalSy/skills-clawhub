#!/usr/bin/env bash
# translator-pro — Translation and localization toolkit
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
set -euo pipefail
VERSION="4.0.0"
DATA_DIR="${TRANSLATOR_DIR:-$HOME/.translator-pro}"
DICT_FILE="$DATA_DIR/dictionary.tsv"
HISTORY="$DATA_DIR/history.log"
mkdir -p "$DATA_DIR/glossaries" "$DATA_DIR/i18n"

BOLD='\033[1m'; DIM='\033[2m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; RESET='\033[0m'

die() { echo -e "${RED}Error: $1${RESET}" >&2; exit 1; }
info() { echo -e "${GREEN}✓${RESET} $1"; }

# Built-in English-Chinese dictionary (200 common words)
_builtin_dict() {
    cat << 'DICTEOF'
hello	你好
goodbye	再见
thank	谢谢
please	请
yes	是
no	不
good	好
bad	坏
big	大
small	小
new	新
old	旧
fast	快
slow	慢
hot	热
cold	冷
water	水
food	食物
time	时间
day	天
night	夜
today	今天
tomorrow	明天
yesterday	昨天
morning	早上
afternoon	下午
evening	晚上
year	年
month	月
week	周
hour	小时
minute	分钟
name	名字
person	人
man	男人
woman	女人
child	孩子
friend	朋友
family	家庭
home	家
work	工作
school	学校
book	书
money	钱
price	价格
buy	买
sell	卖
open	打开
close	关闭
read	读
write	写
eat	吃
drink	喝
sleep	睡
walk	走
run	跑
come	来
go	去
see	看
hear	听
speak	说
think	想
know	知道
want	要
need	需要
like	喜欢
love	爱
help	帮助
give	给
take	拿
make	做
use	用
find	找
start	开始
stop	停止
wait	等
ask	问
answer	回答
learn	学习
teach	教
try	试
remember	记住
forget	忘记
understand	理解
computer	电脑
phone	手机
internet	互联网
email	电子邮件
password	密码
software	软件
hardware	硬件
network	网络
data	数据
file	文件
program	程序
code	代码
server	服务器
database	数据库
website	网站
app	应用
search	搜索
download	下载
upload	上传
login	登录
market	市场
business	商业
company	公司
product	产品
service	服务
customer	客户
project	项目
team	团队
meeting	会议
report	报告
DICTEOF
}

# === translate: translate text ===
cmd_translate() {
    local text="${1:?Usage: translator-pro translate <text> [from] [to]}"
    local from="${2:-auto}"
    local to="${3:-zh}"

    echo -e "${BOLD}Translation${RESET}"
    echo "  From: $from → To: $to"
    echo "  Input: $text"
    echo ""

    # Try LibreTranslate API first
    local api_result
    api_result=$(curl -sf --max-time 10 -X POST \
        "https://libretranslate.com/translate" \
        -H "Content-Type: application/json" \
        -d "{\"q\":\"$text\",\"source\":\"$from\",\"target\":\"$to\"}" 2>/dev/null) || api_result=""

    if [ -n "$api_result" ]; then
        local translated
        translated=$(echo "$api_result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('translatedText',''))" 2>/dev/null)
        if [ -n "$translated" ]; then
            echo -e "  ${GREEN}Result: $translated${RESET}"
            echo "  (via LibreTranslate API)"
        else
            echo -e "  ${YELLOW}API returned no result. Trying local dictionary...${RESET}"
            _dict_translate "$text" "$to"
        fi
    else
        echo -e "  ${DIM}LibreTranslate API unavailable. Using local dictionary:${RESET}"
        _dict_translate "$text" "$to"
    fi

    echo "$(date '+%Y-%m-%d %H:%M') translate $from→$to: $text" >> "$HISTORY"
}

_dict_translate() {
    local text="$1" target="$2"
    local found=false
    local lower_text
    lower_text=$(echo "$text" | tr '[:upper:]' '[:lower:]')

    # Check personal dictionary first
    if [ -f "$DICT_FILE" ]; then
        local result
        result=$(grep -i "^${lower_text}	" "$DICT_FILE" | head -1 | cut -f2)
        if [ -n "$result" ]; then
            echo -e "  ${GREEN}Result: $result${RESET} (personal dictionary)"
            return
        fi
    fi

    # Check builtin dictionary
    local result
    result=$(_builtin_dict | grep -i "^${lower_text}	" | head -1 | cut -f2)
    if [ -n "$result" ]; then
        echo -e "  ${GREEN}Result: $result${RESET} (built-in dictionary)"
    else
        echo "  Word not found in local dictionary."
        echo "  Tip: Add it with: translator-pro add \"$text\" \"<translation>\""
    fi
}

# === detect: detect language ===
cmd_detect() {
    local text="${1:?Usage: translator-pro detect <text>}"

    TEXT="$text" python3 << 'PYEOF'
import os, unicodedata
text = os.environ["TEXT"]

ranges = {
    "CJK": 0, "Latin": 0, "Cyrillic": 0, "Arabic": 0,
    "Hiragana": 0, "Katakana": 0, "Hangul": 0, "Thai": 0, "Devanagari": 0
}

for ch in text:
    name = unicodedata.name(ch, "").upper()
    if "CJK" in name:
        ranges["CJK"] += 1
    elif "LATIN" in name:
        ranges["Latin"] += 1
    elif "CYRILLIC" in name:
        ranges["Cyrillic"] += 1
    elif "ARABIC" in name:
        ranges["Arabic"] += 1
    elif "HIRAGANA" in name:
        ranges["Hiragana"] += 1
    elif "KATAKANA" in name:
        ranges["Katakana"] += 1
    elif "HANGUL" in name:
        ranges["Hangul"] += 1
    elif "THAI" in name:
        ranges["Thai"] += 1
    elif "DEVANAGARI" in name:
        ranges["Devanagari"] += 1

total = sum(ranges.values()) or 1
best = max(ranges, key=ranges.get)

lang_map = {
    "CJK": "Chinese (zh)", "Latin": "English/European (en)",
    "Cyrillic": "Russian (ru)", "Arabic": "Arabic (ar)",
    "Hiragana": "Japanese (ja)", "Katakana": "Japanese (ja)",
    "Hangul": "Korean (ko)", "Thai": "Thai (th)", "Devanagari": "Hindi (hi)"
}

print("  Detected: {}".format(lang_map.get(best, "Unknown")))
print("  Confidence: {:.0f}%".format(ranges[best] / total * 100))
print("")
for script, count in sorted(ranges.items(), key=lambda x: -x[1]):
    if count > 0:
        print("    {}: {} chars ({:.0f}%)".format(script, count, count/total*100))
PYEOF
}

# === batch: translate file line by line ===
cmd_batch() {
    local file="${1:?Usage: translator-pro batch <file> [from] [to]}"
    local from="${2:-auto}"
    local to="${3:-zh}"
    [ -f "$file" ] || die "File not found: $file"

    echo -e "${BOLD}Batch translating: $file${RESET}"
    echo "  Direction: $from → $to"
    echo ""

    local count=0 success=0
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        count=$((count + 1))
        echo "  [$count] $line"

        local result
        result=$(curl -sf --max-time 10 -X POST \
            "https://libretranslate.com/translate" \
            -H "Content-Type: application/json" \
            -d "{\"q\":\"$line\",\"source\":\"$from\",\"target\":\"$to\"}" 2>/dev/null)

        if [ -n "$result" ]; then
            local translated
            translated=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('translatedText',''))" 2>/dev/null)
            if [ -n "$translated" ]; then
                echo -e "  ${GREEN}→ $translated${RESET}"
                success=$((success + 1))
            else
                echo -e "  ${YELLOW}→ (no result)${RESET}"
            fi
        else
            echo -e "  ${DIM}→ (API unavailable)${RESET}"
        fi
        sleep 1  # Rate limit respect
    done < "$file"

    echo ""
    info "Translated $success/$count lines"
}

# === compare: side-by-side ===
cmd_compare() {
    local text="${1:?Usage: translator-pro compare <text> <lang1> <lang2>}"
    local lang1="${2:?Missing first language}"
    local lang2="${3:?Missing second language}"

    echo -e "${BOLD}Translation Comparison${RESET}"
    echo "  Original: $text"
    echo ""

    for lang in "$lang1" "$lang2"; do
        local result
        result=$(curl -sf --max-time 10 -X POST \
            "https://libretranslate.com/translate" \
            -H "Content-Type: application/json" \
            -d "{\"q\":\"$text\",\"source\":\"auto\",\"target\":\"$lang\"}" 2>/dev/null)

        if [ -n "$result" ]; then
            local translated
            translated=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('translatedText',''))" 2>/dev/null)
            echo "  [$lang]: ${translated:-'(no result)'}"
        else
            echo "  [$lang]: (API unavailable)"
        fi
    done
}

# === lookup: dictionary lookup ===
cmd_lookup() {
    local word="${1:?Usage: translator-pro lookup <word>}"
    local lower_word
    lower_word=$(echo "$word" | tr '[:upper:]' '[:lower:]')

    echo -e "${BOLD}Dictionary: $word${RESET}"

    # Personal dictionary
    if [ -f "$DICT_FILE" ]; then
        local result
        result=$(grep -i "^${lower_word}	\|	${word}$" "$DICT_FILE" | head -5)
        if [ -n "$result" ]; then
            echo "  Personal dictionary:"
            echo "$result" | while IFS=$'\t' read -r w t; do
                echo "    $w → $t"
            done
        fi
    fi

    # Built-in dictionary
    local builtin
    builtin=$(_builtin_dict | grep -i "^${lower_word}	\|	${word}" | head -5)
    if [ -n "$builtin" ]; then
        echo "  Built-in dictionary:"
        echo "$builtin" | while IFS=$'\t' read -r w t; do
            echo "    $w → $t"
        done
    fi

    [ -z "${result:-}" ] && [ -z "${builtin:-}" ] && echo "  Not found. Add it: translator-pro add \"$word\" \"translation\""
}

# === add: add to personal dictionary ===
cmd_add() {
    local word="${1:?Usage: translator-pro add <word> <translation>}"
    local translation="${2:?Missing translation}"
    echo -e "$word\t$translation" >> "$DICT_FILE"
    info "Added: $word → $translation"
}

# === dict: manage dictionary ===
cmd_dict() {
    local action="${1:-list}"
    case "$action" in
        list)
            if [ -f "$DICT_FILE" ]; then
                local count
                count=$(wc -l < "$DICT_FILE")
                echo -e "${BOLD}Personal Dictionary ($count entries)${RESET}"
                while IFS=$'\t' read -r w t; do
                    echo "  $w → $t"
                done < "$DICT_FILE"
            else
                echo "  Dictionary is empty. Add words with: translator-pro add <word> <translation>"
            fi
            ;;
        export)
            if [ -f "$DICT_FILE" ]; then
                echo "word,translation"
                while IFS=$'\t' read -r w t; do
                    echo "$w,$t"
                done < "$DICT_FILE"
            else
                echo "  No dictionary data."
            fi
            ;;
        *) echo "Usage: dict list | dict export" ;;
    esac
}

# === romanize: ASCII/pinyin approximation ===
cmd_romanize() {
    local text="${1:?Usage: translator-pro romanize <text>}"

    TEXT="$text" python3 << 'PYEOF'
import os, unicodedata
text = os.environ["TEXT"]
result = []
for ch in text:
    name = unicodedata.name(ch, "")
    if "CJK" in name:
        result.append("[CJK:{:04X}]".format(ord(ch)))
    elif "HIRAGANA" in name or "KATAKANA" in name:
        result.append("[JP:{:04X}]".format(ord(ch)))
    elif "HANGUL" in name:
        result.append("[KR:{:04X}]".format(ord(ch)))
    else:
        try:
            decomp = unicodedata.normalize("NFD", ch)
            ascii_ch = "".join(c for c in decomp if unicodedata.category(c) != "Mn")
            result.append(ascii_ch if ascii_ch else ch)
        except:
            result.append(ch)
print("  Input:     {}".format(text))
print("  Romanized: {}".format("".join(result)))
print("")
print("  Note: Full pinyin/romaji requires external libraries.")
print("  This provides Unicode decomposition and script tagging.")
PYEOF
}

# === count: text statistics ===
cmd_count() {
    local text="${1:?Usage: translator-pro count <text>}"

    TEXT="$text" python3 << 'PYEOF'
import os, re
text = os.environ["TEXT"]
chars = len(text)
chars_no_space = len(text.replace(" ", ""))
words = len(text.split())
sentences = len(re.split(r'[.!?。！？]+', text))
lines = text.count("\n") + 1
print("  Characters:     {} (no spaces: {})".format(chars, chars_no_space))
print("  Words:          {}".format(words))
print("  Sentences:      ~{}".format(max(1, sentences - 1)))
print("  Lines:          {}".format(lines))
print("  Reading time:   ~{} min".format(max(1, words // 200)))
PYEOF
}

# === diff: compare translation files ===
cmd_diff() {
    local f1="${1:?Usage: translator-pro diff <file1> <file2>}"
    local f2="${2:?Missing second file}"
    [ -f "$f1" ] || die "Not found: $f1"
    [ -f "$f2" ] || die "Not found: $f2"

    echo -e "${BOLD}Translation Diff${RESET}"
    echo "  File 1: $f1"
    echo "  File 2: $f2"
    echo ""

    if diff -u --label "$f1" --label "$f2" "$f1" "$f2"; then
        info "Files are identical"
    else
        echo ""
        echo "  Lines in file1: $(wc -l < "$f1")"
        echo "  Lines in file2: $(wc -l < "$f2")"
    fi
}

# === glossary: domain glossaries ===
cmd_glossary() {
    local domain="${1:-list}"
    case "$domain" in
        tech)
            echo -e "${BOLD}Tech Glossary${RESET}"
            cat << 'GL'
  API          应用程序接口     Application Programming Interface
  bug          缺陷            Software defect
  deploy       部署            Release to production
  framework    框架            Development framework
  repository   仓库            Code repository
  commit       提交            Version control commit
  merge        合并            Branch merge
  endpoint     端点            API endpoint
  token        令牌            Authentication token
  middleware   中间件          Processing layer
  cache        缓存            Temporary storage
  query        查询            Database query
  schema       模式            Data structure definition
  container    容器            Docker/OCI container
  pipeline     管道            CI/CD pipeline
GL
            ;;
        business)
            echo -e "${BOLD}Business Glossary${RESET}"
            cat << 'GL'
  ROI          投资回报率      Return on Investment
  KPI          关键绩效指标    Key Performance Indicator
  B2B          企业对企业      Business to Business
  B2C          企业对消费者    Business to Consumer
  MVP          最小可行产品    Minimum Viable Product
  revenue      营收            Income from operations
  margin       利润率          Profit margin
  equity       股权            Ownership stake
  valuation    估值            Company valuation
  acquisition  收购            Company purchase
  IPO          首次公开募股    Initial Public Offering
  burn rate    烧钱速度        Cash spending rate
  runway       跑道            Time before funds run out
  churn        流失率          Customer loss rate
  funnel       漏斗            Sales/conversion funnel
GL
            ;;
        medical)
            echo -e "${BOLD}Medical Glossary${RESET}"
            cat << 'GL'
  diagnosis    诊断            Medical assessment
  symptom      症状            Disease indication
  therapy      治疗            Treatment method
  prescription 处方            Medication order
  vaccine      疫苗            Immunization agent
  chronic      慢性的          Long-term condition
  acute        急性的          Sudden onset
  surgery      手术            Operative procedure
  radiology    放射科          Imaging department
  pharmacy     药房            Medication dispensary
GL
            ;;
        list|*)
            echo "Available glossaries: tech, business, medical"
            echo "Usage: translator-pro glossary <domain>"
            ;;
    esac
}

# === i18n commands ===
cmd_i18n_init() {
    local project="${1:?Usage: translator-pro i18n-init <project> <lang1,lang2,...>}"
    local langs="${2:?Missing languages (e.g. en,zh,ja)}"
    local base="$DATA_DIR/i18n/$project"
    mkdir -p "$base"
    for lang in $(echo "$langs" | tr ',' ' '); do
        mkdir -p "$base/$lang"
        [ ! -f "$base/$lang/messages.json" ] && echo '{}' > "$base/$lang/messages.json"
        info "Created $base/$lang/"
    done
    info "i18n structure ready for: $project"
}

cmd_i18n_extract() {
    local file="${1:?Usage: translator-pro i18n-extract <source-file>}"
    [ -f "$file" ] || die "Not found: $file"
    echo -e "${BOLD}Extracting translatable strings from: $file${RESET}"
    # Extract quoted strings that look like user-facing text
    grep -oE '"[A-Z][^"]{5,}"' "$file" 2>/dev/null | sort -u | while read -r str; do
        echo "  $str"
    done
    grep -oE "'[A-Z][^']{5,}'" "$file" 2>/dev/null | sort -u | while read -r str; do
        echo "  $str"
    done
    echo ""
    info "Review extracted strings and add to your i18n files"
}

cmd_i18n_check() {
    local dir="${1:?Usage: translator-pro i18n-check <i18n-dir>}"
    [ -d "$dir" ] || die "Not a directory: $dir"
    echo -e "${BOLD}Checking i18n completeness: $dir${RESET}"

    local base_keys=""
    local base_lang=""
    for lang_dir in "$dir"/*/; do
        local lang
        lang=$(basename "$lang_dir")
        local msg_file="$lang_dir/messages.json"
        if [ -f "$msg_file" ]; then
            local count
            count=$(python3 -c "import json; print(len(json.load(open('$msg_file'))))" 2>/dev/null || echo 0)
            echo "  $lang: $count keys"
            if [ -z "$base_lang" ]; then
                base_lang="$lang"
                base_keys="$count"
            elif [ "$count" -lt "${base_keys:-0}" ]; then
                echo -e "    ${YELLOW}⚠ Missing $(( base_keys - count )) keys compared to $base_lang${RESET}"
            fi
        fi
    done
}

cmd_i18n_merge() {
    local base="${1:?Usage: translator-pro i18n-merge <base.json> <new.json>}"
    local new="${2:?Missing new file}"
    [ -f "$base" ] || die "Not found: $base"
    [ -f "$new" ] || die "Not found: $new"

    BASE_F="$base" NEW_F="$new" python3 << 'PYEOF'
import json, os
base = json.load(open(os.environ["BASE_F"]))
new = json.load(open(os.environ["NEW_F"]))
added = 0
for k, v in new.items():
    if k not in base:
        base[k] = v
        added += 1
with open(os.environ["BASE_F"], "w") as f:
    json.dump(base, f, indent=2, ensure_ascii=False)
print("  Merged: {} new keys added ({} total)".format(added, len(base)))
PYEOF
}

show_help() {
    cat << EOF
translator-pro v$VERSION — Translation and localization toolkit

Usage: translator-pro <command> [args]

Translation:
  translate <text> [from] [to]   Translate via LibreTranslate API (fallback: local dict)
  detect <text>                  Detect language using Unicode analysis
  batch <file> [from] [to]       Translate file line by line
  compare <text> <l1> <l2>       Side-by-side translation comparison

Dictionary:
  lookup <word>                  Look up in personal + built-in dictionary
  add <word> <translation>       Add to personal dictionary
  dict list                      List personal dictionary
  dict export                    Export as CSV

Text Tools:
  romanize <text>                Unicode decomposition / script tagging
  count <text>                   Character/word/sentence statistics
  diff <file1> <file2>           Compare two translation files
  glossary <domain>              Domain glossary (tech/business/medical)

Localization:
  i18n-init <project> <langs>    Create i18n directory structure
  i18n-extract <file>            Extract translatable strings
  i18n-check <dir>               Check missing translations
  i18n-merge <base> <new>        Merge translation files

  help                           Show this help
  version                        Show version

API: LibreTranslate (free, no key required)
Offline: Built-in English-Chinese dictionary (100+ words)
Data: $DATA_DIR
EOF
}

show_version() {
    echo "translator-pro v$VERSION"
    echo "Powered by BytesAgain | bytesagain.com | hello@bytesagain.com"
}

[ $# -eq 0 ] && { show_help; exit 0; }

case "$1" in
    translate)    shift; cmd_translate "$@" ;;
    detect)       shift; cmd_detect "$@" ;;
    batch)        shift; cmd_batch "$@" ;;
    compare)      shift; cmd_compare "$@" ;;
    lookup)       shift; cmd_lookup "$@" ;;
    add)          shift; cmd_add "$@" ;;
    dict)         shift; cmd_dict "$@" ;;
    romanize)     shift; cmd_romanize "$@" ;;
    count)        shift; cmd_count "$@" ;;
    diff)         shift; cmd_diff "$@" ;;
    glossary)     shift; cmd_glossary "$@" ;;
    i18n-init)    shift; cmd_i18n_init "$@" ;;
    i18n-extract) shift; cmd_i18n_extract "$@" ;;
    i18n-check)   shift; cmd_i18n_check "$@" ;;
    i18n-merge)   shift; cmd_i18n_merge "$@" ;;
    help|-h)      show_help ;;
    version|-v)   show_version ;;
    *)            echo "Unknown: $1"; show_help; exit 1 ;;
esac
