#!/usr/bin/env python3
import sys
import os
import argparse

# Add lib directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib"))
from naver_base import perform_search, format_output

def compact_formatter(results):
    output = []
    news = results.get("news_results")
    if news:
        output.append(f"📰 네이버 뉴스 검색 결과 ({len(news)}개)")
        output.append("=" * 30)
        for i, res in enumerate(news[:10], 1):
            news_info = res.get('news_info', {})
            source = news_info.get('press_name', res.get('source', '알 수 없음'))
            date = news_info.get('news_date', res.get('date', ''))
            
            date_info = f" | {date}" if date else ""
            output.append(f"{i}. {res.get('title')}")
            output.append(f"   📰 {source}{date_info}")
            output.append(f"   🔗 {res.get('link')}")
            output.append("")
    
    return "\n".join(output) if output else "뉴스 검색 결과가 없습니다."

def main():
    parser = argparse.ArgumentParser(description="Naver News Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("-p", "--page", type=int, default=1, help="Page number")
    parser.add_argument("-s", "--sort", default="0", choices=["0", "1", "2"], 
                        help="Sort: 0-Relevance, 1-Latest, 2-Oldest")
    parser.add_argument("-t", "--time", default="all", help="Period (all, 1h, 1d, 1w... or date range)")
    parser.add_argument("-f", "--format", default="compact", choices=["compact", "full", "json"])
    args = parser.parse_args()

    params = {
        "engine": "naver",
        "query": args.query,
        "where": "news",
        "page": args.page,
        "sort": args.sort,
        "period": args.time
    }
    
    # SerpAPI Naver News 특이사항: sort=1(최신)이 가끔 공백을 반환하면 dd로 대체 시도 고려
    results = perform_search(params)
    
    if "error" in results and "Naver hasn't returned any results" in results["error"]:
        # Fallback: 'where=news' 대신 검색어에 뉴스를 포함하여 통합에서 추출 시도
        params["where"] = "nexearch"
        params["query"] = f"{args.query} 뉴스"
        results = perform_search(params)

    print(format_output(results, args.format, compact_formatter))

if __name__ == "__main__":
    main()
