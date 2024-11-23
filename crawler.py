from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# 수집한 리뷰 저장하는 리스트
reviews = []

# Idius 상품 페이지 접속
driver = webdriver.Chrome()
driver.get('https://www.idus.com/v2/product/1457a4bf-bece-4d9a-bff3-3312511c986e')
time.sleep(2)

# 리뷰 수집
def collect_reviews(num_pages):
    # 리뷰 섹션으로 스크롤
    review_section = driver.find_element(By.ID, 'REVIEW')
    driver.execute_script("arguments[0].scrollIntoView();", review_section)
    time.sleep(2)
    
    for page in range(num_pages):
        # 현재 페이지의 리뷰들이 모두 로드될 때까지 스크롤
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # 스크롤 다운
            driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(1)
            
            # 새로운 높이 적용
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        # 리뷰 수집 코드
        review_elements = driver.find_elements(By.CLASS_NAME, 'ReviewListItem__review')
        
        for review in review_elements:
            try:
                review_text = review.find_element(By.CLASS_NAME, 'whitespace-pre-line.body1-regular-medium.line-clamp-6').text
                reviews.append(review_text)
            except:
                continue
                
        # 다음 페이지 이동
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '[data-page="{}"]'.format(page + 2))
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            next_button.click()
            time.sleep(2)
        except:
            break

# 전체 페이지 수집 (페이지번호 ~846)
collect_reviews(846)

# 수집된 리뷰 확인
print(f'수집된 리뷰 수: {len(reviews)}')
for i, review in enumerate(reviews[:5]):  # 처음 5개 리뷰만 출력
    print(f'\n리뷰 {i+1}:', review)

# 종료
driver.quit()