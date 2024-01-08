# imports
import pandas as pd
import requests

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_stealth import stealth

from browsermobproxy import Server
# from amazoncaptcha import AmazonCaptcha


import time, os, csv, random, html, re
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

limit=10000

def scrape_infos(name, url):
    # 로그 초기화
    status_log_txt = 'status.txt'
    count_item=1
    # 시작
    next_operation = "start"
    with open(status_log_txt, 'w', encoding='utf-8') as file:
        file.write(next_operation + '\n')
        file.write(url + '\n')
    
    # csv 파일(데이터)
    csv_file_path1 = f'page_urls/{name}_page_urls.csv'  
    csv_file_path2 = f'product_urls/{name}_product_urls.csv'
    csv_file_path3 = f'product_infos/{name}_product_infos.csv'
    csv_file_path4 = f'error_urls/no_product_page_urls.csv'
    csv_file_path5 = f'error_urls/no_info_product_urls.csv'
    csv_file_path6 = f'error_urls/no_next_page_urls.csv'
    csv_file_path7 = f'error_urls/no_img_product_urls.csv'

    # 폴더 생성
    os.makedirs(f'page_urls', exist_ok=True)
    os.makedirs(f'product_urls', exist_ok=True)
    os.makedirs(f'product_infos', exist_ok=True)
    os.makedirs(f'error_urls', exist_ok=True)
    
    # csv 파일 헤더 설정
    headers_needed1 = not os.path.exists(csv_file_path1)    
    headers_needed2 = not os.path.exists(csv_file_path2)
    headers_needed3 = not os.path.exists(csv_file_path3)
    headers_needed4 = not os.path.exists(csv_file_path4)
    headers_needed5 = not os.path.exists(csv_file_path5)
    headers_needed6 = not os.path.exists(csv_file_path6)
    headers_needed7 = not os.path.exists(csv_file_path7)

    if headers_needed1:
        with open(csv_file_path1, mode='a', newline='', encoding='utf-8') as file1:
            writer1 = csv.writer(file1)
            writer1.writerow(['Page URL'])
            file1.flush()
    if headers_needed2:
        with open(csv_file_path2, mode='a', newline='', encoding='utf-8') as file2:
            writer2 = csv.writer(file2)
            writer2.writerow(['Product URL'])
            file2.flush()
    if headers_needed3:
        with open(csv_file_path3, mode='a', newline='', encoding='utf-8') as file3:
            writer3 = csv.writer(file3)
            writer3.writerow(['category' , 'name', 'price', 'grade', 'Product URL', 'Img_URL']) # ['카테고리' , '상품명', '가격', '정보', 'Product URL', 'Img_URL'] 상품 필수 정보가 그다지 유용하지 않음
            file3.flush()  
    if headers_needed4:
        with open(csv_file_path4, mode='a', newline='', encoding='utf-8') as file4:
            writer4 = csv.writer(file4)
            writer4.writerow(['Error page URLs'])
            file4.flush()  
    if headers_needed5:
        with open(csv_file_path5, mode='a', newline='', encoding='utf-8') as file5:
            writer5 = csv.writer(file5)
            writer5.writerow(['Error product URLs'])
            file5.flush()          
    if headers_needed6:
        with open(csv_file_path6, mode='a', newline='', encoding='utf-8') as file6:
            writer6 = csv.writer(file6)
            writer6.writerow(['No next page URLs'])
            file6.flush()          
    if headers_needed7:
        with open(csv_file_path7, mode='a', newline='', encoding='utf-8') as file7:
            writer7 = csv.writer(file7)
            writer7.writerow(['image get error product URLs'])
            file7.flush() 
    
    #webdriver 설정
    next_operation = 'configure driver'  
    with open(status_log_txt, 'w', encoding='utf-8') as file:
        file.write(next_operation + '\n')
        file.write(url + '\n')
    is_Configured, driver = configure_driver()
    if is_Configured == False:
        while is_Configured:
            print('Re-configuring Driver...')
            is_Configured, driver = configure_driver()  # configure driver over and over again
    
    # 페이지 열기 (주소 직접 입력)
    next_operation = "open page"
    with open(status_log_txt, 'w', encoding='utf-8') as file:
        file.write(next_operation + '\n')
        file.write(url + '\n')
    driver.get(url=url)

    is_Done=False
    while not is_Done:  
        # 1. 현재 페이지 기록
        current_page_url = driver.current_url
        with open(csv_file_path1, mode='a', newline='', encoding='utf-8') as file1:  # page_urls/{name}_page_urls.csv
            writer1 = csv.writer(file1)
            writer1.writerow([current_page_url])
            file1.flush()
        next_page_url = get_nextpage_url(driver, current_page_url)  # 다음 리스트 페이지

        # 2. 리스트 페이지에서 상품 페이지 url 추출
        next_operation = "extract products url"
        with open(status_log_txt, 'w', encoding='utf-8') as file:
            file.write(next_operation + '\n')
            file.write(current_page_url + '\n')
        product_urls = get_productpage_url(driver, current_page_url)  # returns [[url1],[url2],...]
        
        # 상품 페이지 추출 실패시
        if len(product_urls) == 0:
            with open(csv_file_path4, mode='a', newline='', encoding='utf-8') as file4:  # no_product_page_urls.csv'
                writer4 = csv.writer(file4)
                writer4.writerow([current_page_url])
                file4.flush()  
            return  # 추출 실패시 종료
        
        # 상품 페이지 기록
        with open(csv_file_path2, mode='a', newline='', encoding='utf-8') as file2:  # product_urls/{name}_product_urls.csv
            writer2 = csv.writer(file2)   
            writer2.writerows(product_urls)
            file2.flush()     
        
        # 3. 상품 페이지 이동 / 정보 기록
        for [product_url] in product_urls:
            time.sleep(random.randint(1000, 2000)/1000)  # (아마도 있을) 봇 체크 피하기 위한 텀
            
            # 상품 페이지 열기
            next_operation =  'open product page'
            with open(status_log_txt, 'w', encoding='utf-8') as file:
                file.write(next_operation + '\n')
                file.write(current_page_url + '\n')
                file.write(product_url + '\n')
            driver.get(product_url)
            # 정보 추출
            next_operation = 'get infos'
            with open(status_log_txt, 'w', encoding='utf-8') as file:
                file.write(next_operation + '\n')
                file.write(current_page_url + '\n')
                file.write(product_url + '\n')            
            product_infos = fetch_info_from_product_page(driver)  # returns [] when fails to fetch infos

            # 추출 성공시   
            if len(product_infos) != 0:
                # 정보 저장
                next_operation = 'log infos'
                with open(status_log_txt, 'w', encoding='utf-8') as file:
                    file.write(next_operation + '\n')
                    file.write(current_page_url + '\n')
                    file.write(product_url + '\n')
                with open(csv_file_path3, mode='a', newline='', encoding='utf-8') as file3:  # product_infos/{name}_product_infos.csv
                    writer3 = csv.writer(file3)
                    writer3.writerow(product_infos)
                    file3.flush() 
                # 상품 이미지 저장
                image_url =product_infos[-1]
                title=str('{0:05d}'.format(count_item)) # 파일명은 추출 순서로 지정
                print(title)
                count_item+=1
                next_operation = 'save img'
                with open(status_log_txt, 'w', encoding='utf-8') as file:
                    file.write(next_operation + '\n')
                    file.write(current_page_url + '\n')
                    file.write(image_url + '\n')
                is_ImgSaved = save_img(name, title, image_url)
                
                # 저장 실패
                if is_ImgSaved == False:
                    with open(csv_file_path7, mode='a', newline='', encoding='utf-8') as file7:  # error_urls/no_img_product_urls.csv
                        writer7 = csv.writer(file7)
                        writer7.writerow([product_url])
                        file7.flush()

            # 추출 실패
            else:
                with open(csv_file_path5, mode='a', newline='', encoding='utf-8') as file5:  # error_urls/no_info_product_urls.csv
                    writer5 = csv.writer(file5)
                    writer5.writerow([product_url])
                    file5.flush()   

        product_urls = []  # 상품 추출 후 목록 비우기
        
        # 4. 다음 리스트 페이지 이동
        
        # 리스트 페이지로 복귀 (현재 방식에선 없어도 되긴 함)
        next_operation = 'go back to page'
        driver.get(current_page_url)
        with open(status_log_txt, 'w', encoding='utf-8') as file:
            file.write(next_operation + '\n')
            file.write(current_page_url + '\n')
        
        # 다음 페이지로 이동 (주소 직접 입력)
        next_operation = 'click next page'
        with open(status_log_txt, 'w', encoding='utf-8') as file:
            file.write(next_operation + '\n')
            file.write(current_page_url + '\n')
        # 대략 5000개 정도 추출 후 해당 카테고리 종료 (정확히 5000개 추출이 아님)                
        if not count_item>limit:
            print('Trying to directly open next page')
            next_operation = 'directly open next page'
            with open(status_log_txt, 'w', encoding='utf-8') as file:
                file.write(next_operation + '\n')
                file.write(current_page_url + '\n')
            # 셀레니움 창을 껏다 켜야 할지 그냥 할지 잘 모르겠음 현재는 안끄고 계속 크롤링 하는 형태
            driver.quit()
            is_Configured, driver = configure_driver()
            if is_Configured == False:
                while is_Configured:
                    print('Re-configuring Driver...')
                    is_Configured, driver = configure_driver()  # configure driver over and over again
            driver.get(next_page_url)
        else:
            is_Done = True

    
    next_operation = 'each start url finished'
    # 카테고리 종료시 현재 상태 기록 파일 삭제
    if os.path.exists(status_log_txt):
        os.remove(status_log_txt)
    print(f'{name} done. Moving to next category')

#webdriver 초기화/설정
def configure_driver():
    try:
        # User agent 설정
        chrome_options = Options()
        chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-software-rasterizer")    
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        # 아마도 필요 없음
        # # Create custom headers (including Referer)
        # headers = {
        #     "Referer": "https://emart.ssg.com/",
        #     # Add any other custom headers you want
        # }
        # proxy.add_to_capabilities(headers)
        
        # Apply stealth settings    스텔스 셀레니움 설정
        stealth(driver,
                languages=["en-US", "en"],  # List of languages
                vendor="Jooyeon Tec.",  # Vendor name
                platform="Win64",  # Platform
                webgl_vendor="Nvidia Inc.",  # WebGL vendor
                renderer="Nvidia GTX 1050Ti",  # WebGL renderer
                fix_hairline=True,  # Fix for thin lines issue
                )
        return True, driver
    
    except Exception as e:
        print('Error Configuring Driver: ',e)
        return False, driver

# 다음 리스트 페이지 찾기 (url 수정)
def get_nextpage_url(driver, current_url):
    try:
        temp=current_url[current_url.find('page=')+5:]
        temp=int(temp)+1
        next_page_url=current_url[:current_url.find('page=')+5]+str(temp)
        return next_page_url
    except Exception as e:
        print('get_nextpage_url error: ', e)
        return None

# 상품 페이지 url 수집
def get_productpage_url(driver, current_url):
    try:
        # get the html        
        html_content = driver.page_source
        
        # Initialize BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        # 리스트 페이지에서 광고 상품(이마트 '할인 중인 상품') 제외
        ignore_div=soup.find_all('div', class_='csrch_advert')
        for div in ignore_div:
            div.decompose()
        ignore_div=soup.find_all('div', class_='csrch_type')
        for div in ignore_div:
            div.decompose()
        ignore_div=soup.find_all('div', class_='csrch_planshop')
        for div in ignore_div:
            div.decompose()
        # 상품 페이지 div 찾기 csrch_type csrch_planshop
        divs_with_data_index = soup.find_all('div', class_="mnemitem_thmb_v2")

        urls = []
        # 링크 추출
        for div in divs_with_data_index:
            a_tag = div.find('a', class_='mnemitem_thmb_link clickable')
            if a_tag and 'href' in a_tag.attrs:
                full_url = a_tag['href']
                if 'advertBidId' in full_url:
                    continue
                
                if type(full_url) == str:
                    urls.append([full_url])
        return urls
    
    except Exception as e:
        print('Get ProductPage Error: ', e)
        return []

# 상품 페이지 정보 추출    
def fetch_info_from_product_page(driver):
    try:
        # fetch whole html from url
        html_content = driver.page_source
        # html_content=html_content.encode('utf-8') # 딱히 소용이 없는 듯
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        output = []
        # Get each information    
        
        # 이마트에서 제공하는 상품 범주
        categoty_links= soup.select('a.lo_menu.lo_arr.clickable')
        category = [link.get_text().strip() for link in categoty_links]
        output.append(category)
        # 판매자가 설정한 상품 이름
        title = soup.find('title', {'class': 'notranslate'}).get_text(strip=True)
        output.append(title)

        # 가격 숫자만 수집 원화
        price_whole_part = soup.find('em', class_='ssg_price')
        re_price=re.sub(r'[^0-9]', '', price_whole_part.get_text(strip=True))
        output.append(re_price)
        
        # 상품 정보 (상품 필수 정보 / 카테고리 별로 제공되는 상품 필수 정보가 달라서 수집 후 전처리 시 주의해야 함)
        # 과일 상품의 경우 제품명에 수량 무게 다 기재가 되는 특성이 있어 과일 크롤링 시에는 필요하지 않음
        # 다른 상품 크롤링 할 경우에는 필요할 수 있음
        # product_info = {}
        # table = soup.find('table', summary="상품 필수정보 보여주는 표")
        # if table:
        #     # Loop through each row in the table
        #     for row in table.find_all('tr'):
        #         # Extract columns: key and value
        #         columns1 = row.find_all('th')
        #         columns2 = row.find_all('td')
        #         key = columns1[0].get_text(strip=True)
        #         value = columns2[0].get_text(strip=True)
        #         product_info[key] = value
        # else:
        #     # Handle the case where the table is not found
        #     product_info = {}  # or None if you prefer None
        # output.append(product_info)
        # product_url
        try:
            grade=soup.find('em', class_="cdtl_grade_total").get_text(strip=True)
        except:
            grade=0
        output.append(grade)
        product_url = driver.current_url # tlidSrch
        product_url = product_url[:product_url.find('tlidSrch')-1]
        output.append(product_url)
        
        # img_url
        selected_imgs = soup.find('img', id='mainImg')
        image_url = selected_imgs.get('src')  # Default to src if data-old-hires is not present
        output.append(image_url)
        
        # return
        return output  # output = ['카테고리' , '상품명', '가격', '정보', 'Product URL', 'Img_URL']
    except Exception as e:
        print('Fetch Info Error: ', e)        
        return []

# 이미지 저장 
def save_img(name, title, image_url):
    try:
        # Send a GET request to the image URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Create directory if it doesn't exist
        os.makedirs(f'imgs/{name}', exist_ok=True)
        
        # Sanitize title for filename 파일명 정규화 (지금 필요없음)
        # sanitized_title = sanitize_filename(title[:200])
        file_path = f'imgs/{name}/{title}.jpg'

        # Check if the image is already in JPEG format
        if image_url.lower().endswith('.jpg'):
            # Save image directly if it is already a JPEG
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return True  # return True when Success
        else:
            # Convert and save in JPEG format if the image is in a different format
            img = Image.open(BytesIO(response.content))
            img.convert('RGB').save(file_path, 'JPEG')
            return True  # return True when Success
            
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False  # return False when failure

# 파일명 정규식으로 특수문자 제거(상품명이 한글로 제공되어서 추출 순서로 파일을 저장하기 때문에 현재 필요없는 기능)   
# def sanitize_filename(filename):
#     # Keep only alphabets (uppercase and lowercase)
#     return re.sub(r'[^a-zA-Z]', '', filename)



#main 

crawl_data = {
    # 'Clothes_woman' : 'https://emart.ssg.com/search.ssg?target=all&query=%EC%84%A0%EB%AC%BC&ctgId=6000214476&ctgLv=2&page=1',
    # 'Clothes_man' : 'https://emart.ssg.com/search.ssg?target=all&query=%EC%84%A0%EB%AC%BC&ctgId=6000214489&ctgLv=2&page=1',
    # 'Clothes_uni' : 'https://emart.ssg.com/search.ssg?target=all&query=%EC%84%A0%EB%AC%BC&ctgId=6000214500&ctgLv=2&page=1',
    # 'Bedclothes' : 'https://emart.ssg.com/search.ssg?target=all&query=%EC%84%A0%EB%AC%BC&ctgId=6000214280&ctgLv=3&ctgLast=Y&pbaarentCtgId=6000214279&page=1',
    'Baby_toy' : 'https://emart.ssg.com/search.ssg?target=all&query=%EC%84%A0%EB%AC%BC&ctgId=6000213839&ctgLv=1&page=1',
    'Bakery' : 'https://emart.ssg.com/search.ssg?target=all&query=%EC%84%A0%EB%AC%BC&ctgId=6000213839&ctgLv=1&page=1',
    'Drinks' : 'https://emart.ssg.com/search.ssg?target=all&query=%EC%84%A0%EB%AC%BC&ctgId=6000213424&ctgLv=1&page=1',
    'Carpet' : 'https://emart.ssg.com/search.ssg?target=all&query=%EC%84%A0%EB%AC%BC&ctgId=6000214293&ctgLv=2&page=1',
    'Retort' : 'https://emart.ssg.com/search.ssg?target=all&query=%EC%84%A0%EB%AC%BC&ctgId=6000213247&ctgLv=1&page=1',
    'Shoes' : 'https://emart.ssg.com/search.ssg?target=all&query=%EC%84%A0%EB%AC%BC&ctgId=6000213816&ctgLv=2&page=1',
    'Meat' : 'https://emart.ssg.com/search.ssg?target=all&query=%EC%84%A0%EB%AC%BC&ctgId=6000215194&ctgLv=1&page=1',
    'Can_food' : 'https://emart.ssg.com/search.ssg?target=all&query=%EC%84%A0%EB%AC%BC&ctgId=6000213319&ctgLv=1&page=1',
}
dictionaries = [
    crawl_data,
]
if __name__ == "__main__":
    for each_dictionary in dictionaries:
        for name, url in each_dictionary.items():
            
            status_log_txt = 'status.txt'
            last_operation = None
            
            # Check if status file exists and read the last operation and URL
            if os.path.exists(status_log_txt):
                with open(status_log_txt, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    if len(lines) >= 2:
                        last_operation = lines[0].strip()
                        last_url = lines[1].strip()
                # last_operation = 'start', 'configure driver', "open page", "extract products url", 'open product page',
                #                   'get infos', 'log infos', 'save img', 'go back to page', 'click next page',
                #                   'each start url finished'
            
            if last_operation:  # if there is last_operation
                url = last_url
                scrape_infos(name, url)
            
            else:  # if just starting
                scrape_infos(name, url)

